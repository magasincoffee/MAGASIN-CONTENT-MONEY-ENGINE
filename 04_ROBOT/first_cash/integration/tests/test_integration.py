from __future__ import annotations
import copy, json, sys, tempfile, unittest
from pathlib import Path

HERE=Path(__file__).resolve(); MOD=HERE.parents[1]; ROOT=HERE.parents[4]; sys.path.insert(0,str(MOD))
from integration_harness import *
from launch_gate import evaluate as evaluate_launch, NOT_READY, READY, PrivacyLeakError
from evaluator import evaluate as evaluate_gate_a
from publish_safety import MockBackend, MockReconciler, LatchStore, PublishSafetyMachine, RECON_UNKNOWN, STATE_CONFIRMED, STATE_BLOCKED_AMBIGUOUS
from cash_truth import CashTruthLedger

class IntegrationTests(unittest.TestCase):
    def test_flow_a_current_reality_stays_not_ready_l0_no_side_effect(self):
        r=current_reality_result(); self.assertEqual(r['gate_a_state'],'NOT_STARTED'); self.assertEqual(r['launch']['result'],NOT_READY); self.assertEqual(r['commercial_events_created'],0); self.assertFalse(r['publish_invoked'])

    def test_flow_b_hypothetical_gate_a_pass_maps_into_launch_without_bypass(self):
        snapshot,result=hypothetical_launch_from_gate_a(); self.assertEqual(result['state'],'PASS'); self.assertEqual(snapshot['gate_a']['state'],'PASS'); self.assertEqual(snapshot['gate_a']['merchant_public_identifier'],'EXAMPLE MERCHANT — NOT REAL'); self.assertEqual(snapshot['gate_a']['program_public_identifier'],'EXAMPLE-PROGRAM'); self.assertTrue(snapshot['gate_a']['tracking_link_capability']['value'])

    def test_flow_c_exact_three_hypothetical_mechanical_ready(self):
        snapshot,_=hypothetical_launch_from_gate_a(); self.assertEqual(evaluate_launch(snapshot)['result'],READY); two=copy.deepcopy(snapshot);two['three_pin_package']['pins']=two['three_pin_package']['pins'][:2];self.assertEqual(evaluate_launch(two)['result'],NOT_READY); four=copy.deepcopy(snapshot);p=copy.deepcopy(four['three_pin_package']['pins'][0]);p['content_id']='EXTRA';four['three_pin_package']['pins'].append(p);self.assertEqual(evaluate_launch(four)['result'],NOT_READY)

    def test_flow_d_three_mock_publish_intents_safety(self):
        snapshot,_=hypothetical_launch_from_gate_a(); intents=publish_intents(snapshot); self.assertEqual(len({i.content_id for i in intents}),3)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); store=LatchStore(root/'latches'); platform=root/'platform.json'
            # P1 happy path; repeated call zero resend
            b1=MockBackend(platform,['success']); m1=PublishSafetyMachine(store,b1,MockReconciler(b1)); r1=m1.run(intents[0]); self.assertEqual(r1['state'],STATE_CONFIRMED); sends=b1.send_count; self.assertEqual(m1.run(intents[0])['state'],STATE_CONFIRMED); self.assertEqual(b1.send_count,sends)
            # P2 timeout-after-create; restart reconciles existing mock ID, no duplicate
            b2=MockBackend(platform,['timeout_after_create']); m2=PublishSafetyMachine(store,b2,MockReconciler(b2)); first=m2.run(intents[1]); self.assertEqual(first['state'],STATE_BLOCKED_AMBIGUOUS); sends2=b2.send_count; br=MockBackend(platform,['success']); restarted=PublishSafetyMachine(store,br,MockReconciler(br)); second=restarted.run(intents[1]); self.assertEqual(second['state'],STATE_CONFIRMED); self.assertEqual(br.send_count,sends2)
            # P3 ambiguous; reconciliation UNKNOWN blocks, zero resend
            b3=MockBackend(platform,['ambiguous_no_create']); m3=PublishSafetyMachine(store,b3,MockReconciler(b3)); first3=m3.run(intents[2]); self.assertEqual(first3['state'],STATE_BLOCKED_AMBIGUOUS); key=first3['publish_key']; sends3=b3.send_count; br3=MockBackend(platform,['success']); rec=MockReconciler(br3,{key:RECON_UNKNOWN}); rr=PublishSafetyMachine(store,br3,rec).run(intents[2]); self.assertEqual(rr['state'],STATE_BLOCKED_AMBIGUOUS); self.assertEqual(br3.send_count,sends3)

    def test_flow_e_observation_to_cash_truth_preserves_no_cash_before_guard(self):
        with tempfile.TemporaryDirectory() as td:
            ledger=CashTruthLedger(Path(td)/'ledger.jsonl',CASH_SCHEMA); events=hypothetical_cash_events('MOCKPIN-EXAMPLE','MCME-FC1-FRIDGE-FIT-P01-MEASURE')
            for e in events:self.assertTrue(ledger.append(e).status.startswith('APPENDED'))
            r=ledger.replay(); self.assertEqual(r['net_settled_cash'],{}); self.assertEqual(r['inference_policy']['payout_issued_to_cash_settled'],'NEVER_INFER')

    def test_flow_e_duplicate_ingestion_does_not_double_count(self):
        with tempfile.TemporaryDirectory() as td:
            ledger=CashTruthLedger(Path(td)/'ledger.jsonl',CASH_SCHEMA); e=hypothetical_cash_events('MOCKPIN-X','CID')[4]; self.assertTrue(ledger.append(e).status.startswith('APPENDED')); dup=copy.deepcopy(e);dup['event_id']='E-PENDING-DUP'; self.assertEqual(ledger.append(dup).status,'DUPLICATE_SOURCE_EVENT'); self.assertEqual(ledger.replay()['event_count'],1)

    def test_flow_e_reversal_is_append_only_and_guarded_cash_is_test_only(self):
        with tempfile.TemporaryDirectory() as td:
            ledger=CashTruthLedger(Path(td)/'ledger.jsonl',CASH_SCHEMA); pending=hypothetical_cash_events('MOCKPIN-X','CID')[4]; ledger.append(pending); ledger.append(reversal_event()); self.assertEqual(ledger.replay()['event_count'],2); self.assertEqual(ledger.replay()['commission_current_reversed_record_count'],1); ledger.append(guarded_cash_event()); self.assertEqual(ledger.replay()['net_settled_cash']['USD'],'10.50')

    def test_flow_f_restart_replay_and_evaluators_are_deterministic(self):
        gate=load_json(GATE_FIXTURE); self.assertEqual(evaluate_gate_a(gate,GATE_SCHEMA),evaluate_gate_a(copy.deepcopy(gate),GATE_SCHEMA)); launch,_=hypothetical_launch_from_gate_a(); self.assertEqual(evaluate_launch(launch),evaluate_launch(copy.deepcopy(launch)))
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'ledger.jsonl'; l1=CashTruthLedger(path,CASH_SCHEMA); [l1.append(e) for e in hypothetical_cash_events('MOCKPIN-X','CID')[:3]]; before=l1.replay(); after=CashTruthLedger(path,CASH_SCHEMA).replay(); self.assertEqual(before,after)

    def test_flow_g_combined_sanitized_passes_and_secret_fails_closed(self):
        launch,_=hypothetical_launch_from_gate_a(); self.assertEqual(evaluate_launch(launch)['result'],READY); bad=copy.deepcopy(launch); bad['three_pin_package']['pins'][0]['destination_link_ref']='https://merchant.invalid/?token=SECRET';
        with self.assertRaises(PrivacyLeakError): evaluate_launch(bad)

    def test_cross_contract_provider_unknowns_are_explicit(self):
        m=cross_contract_mapping(); self.assertEqual(m['real_attribution_subid_method'],PROVIDER_SPECIFIC_UNKNOWN); self.assertEqual(m['real_tracking_link_generation'],PROVIDER_SPECIFIC_UNKNOWN); self.assertEqual(m['real_pinterest_reconciliation_lookup'],PROVIDER_SPECIFIC_UNKNOWN); self.assertEqual(m['real_network_source_record_semantics'],PROVIDER_SPECIFIC_UNKNOWN)

if __name__=='__main__':unittest.main()
