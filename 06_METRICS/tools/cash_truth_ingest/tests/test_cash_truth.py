from __future__ import annotations
import copy, json, sys, tempfile, unittest
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve(); MOD=HERE.parents[1]; METRICS=HERE.parents[3]; SCHEMA=METRICS/'mcme_cash_truth_v1.schema.json'; FIX=HERE.parent/'fixtures'/'example_events.json'; sys.path.insert(0,str(MOD))
from cash_truth import CashTruthLedger, IdempotencyConflictError, PrivacyValidationError, SchemaValidationError, SemanticValidationError, load_schema, validate_event

def base(): return json.loads(FIX.read_text(encoding='utf-8'))['base_event']
def event(kind,eid,amount='10.50'):
    e=copy.deepcopy(base()); e['event_id']=eid; e['event_type']=kind; e['source']['source_reference_sanitized']='fixture:'+eid; e['source']['provider_state_label_sanitized']=kind; e['idempotency']['provider_effective_at']='2026-09-20T00:00:01+07:00'; e['canonical_money_state']={'COMMISSION_PENDING':'PENDING','COMMISSION_VALIDATED':'VALIDATED','COMMISSION_REVERSED':'REVERSED','COMMISSION_PAYABLE':'PAYABLE','PAYOUT_ISSUED':'PAYOUT_ISSUED','CASH_SETTLED':'CASH_SETTLED'}.get(kind); e['money']={'amount_decimal':amount,'currency':'USD'}; return e
def settled(eid='EXAMPLE-CASH',amount='10.50'):
    e=event('CASH_SETTLED',eid,amount); e['network']=None; e['source']['source_system']='OWNER_PAYOUT_RAIL'; e['source']['source_record_id_sanitized']='SETTLEMENT-'+eid; e['settlement']={'funds_actually_received':True,'owner_authorized_payout_rail':True,'reconciled_to_payout':True,'payout_source_record_id_sanitized':'PAYOUT-EXAMPLE'}; return e
def cost():
    e=copy.deepcopy(base()); e.update(event_id='EXAMPLE-COST',event_type='COST_RECORDED',network=None,merchant=None,program_id_sanitized=None,canonical_money_state=None); e['source'].update(source_system='COST_LEDGER',source_type='RECEIPT_INVOICE',source_record_id_sanitized='COST-1'); e['money']={'amount_decimal':'2.25','currency':'USD'}; e['cost']={'category':'DIRECT_CREATIVE_COST','attributable':True}; return e
def time_event():
    e=copy.deepcopy(base()); e.update(event_id='EXAMPLE-TIME',event_type='TIME_RECORDED',network=None,merchant=None,program_id_sanitized=None,canonical_money_state=None); e['source'].update(source_system='TIME_LEDGER',source_type='TIMER_LOG',source_record_id_sanitized='TIME-1'); e.pop('money'); e['time']={'category':'PRODUCTION_MINUTES','minutes':7}; return e

class T(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory(); self.path=Path(self.tmp.name)/'private'/'ledger.jsonl'; self.l=CashTruthLedger(self.path,SCHEMA)
    def tearDown(self): self.tmp.cleanup()
    def test_schema_valid_and_decimal_money_is_supported(self): Draft202012Validator.check_schema(load_schema(SCHEMA)); validate_event(cost(),SCHEMA)
    def test_valid_fictitious_event_writes(self): self.assertEqual(self.l.append(base()).status,'APPENDED'); self.assertEqual(self.l.replay()['event_count'],1)
    def test_duplicate_same_stable_source_is_not_double_counted(self):
        a=base(); b=copy.deepcopy(a); b['event_id']='REPOLL'; self.assertEqual(self.l.append(a).status,'APPENDED'); self.assertEqual(self.l.append(b).status,'DUPLICATE_SOURCE_EVENT'); self.assertEqual(self.l.replay()['event_count'],1)
    def test_repeated_polling_network_click_does_not_double_count(self):
        e=copy.deepcopy(base()); e.update(event_id='CLICK1',event_type='NETWORK_CLICK_OBSERVED',canonical_money_state=None); e.pop('money'); e['metric']={'name':'NETWORK_CLICKS','value':1,'aggregation_mode':'INDIVIDUAL_EVENT'}; e['source']['source_record_id_sanitized']='CLICK-1'; e['idempotency']['strategy']='PROVIDER_STABLE_ID'; e['idempotency']['provider_effective_at']=None; self.assertEqual(self.l.append(e).status,'APPENDED'); x=copy.deepcopy(e); x['event_id']='CLICK2'; self.assertEqual(self.l.append(x).status,'DUPLICATE_SOURCE_EVENT')
    def test_pending_does_not_auto_promote_to_validated(self): self.l.append(base()); r=self.l.replay(); self.assertEqual(r['commission_current_amounts']['pending']['USD'],'10.50'); self.assertEqual(r['commission_current_amounts']['validated'],{})
    def test_explicit_validated_event_replaces_current_pending_state_not_double_revenue(self): self.l.append(base()); self.l.append(event('COMMISSION_VALIDATED','VALID')); r=self.l.replay(); self.assertEqual(r['commission_current_amounts']['pending'],{}); self.assertEqual(r['commission_current_amounts']['validated']['USD'],'10.50')
    def test_payout_issued_does_not_auto_become_cash_settled(self): self.l.append(event('PAYOUT_ISSUED','PAYOUT')); self.assertEqual(self.l.replay()['net_settled_cash'],{})
    def test_malformed_cash_settled_missing_guard_is_rejected(self):
        e=settled(); e['settlement']['funds_actually_received']=False
        with self.assertRaises((SchemaValidationError,SemanticValidationError)): self.l.append(e)
    def test_cash_settled_requires_owner_authorized_payout_rail_source(self):
        e=settled(); e['source']['source_system']='PAYOUT_PROVIDER'
        with self.assertRaises(SemanticValidationError): self.l.append(e)
    def test_valid_fictitious_cash_settled_writes_only_with_guards(self): self.assertEqual(self.l.append(settled()).status,'APPENDED'); self.assertEqual(self.l.replay()['net_settled_cash']['USD'],'10.50')
    def test_reversal_is_appended_and_historical_pending_remains(self): self.l.append(base()); self.l.append(event('COMMISSION_REVERSED','REV','-10.50')); r=self.l.replay(); self.assertEqual(r['event_count'],2); self.assertEqual(r['commission_current_reversed_record_count'],1)
    def test_negative_adjustment_is_visible_but_not_inferred_as_cash_debit(self):
        self.l.append(settled()); e=event('NEGATIVE_ADJUSTMENT_RECORDED','ADJ','-1.00'); e['adjustment']={'scope':'PAYOUT','reason_category':'CLAWBACK','related_source_record_id_sanitized':'PAYOUT-EXAMPLE'}; e['canonical_money_state']=None; self.l.append(e); self.assertEqual(self.l.replay()['net_settled_cash']['USD'],'10.50'); self.l.append(settled('DEBIT','-1.00')); self.assertEqual(self.l.replay()['net_settled_cash']['USD'],'9.50')
    def test_conservative_no_stable_id_duplicate_requires_reconciliation(self):
        e=base(); e['event_id']='C1'; e['source']['source_record_id_sanitized']=None; e['idempotency']['strategy']='CONSERVATIVE_RECONCILIATION'; self.assertEqual(self.l.append(e).status,'APPENDED_CONSERVATIVE'); x=copy.deepcopy(e); x['event_id']='C2'; self.assertEqual(self.l.append(x).status,'REQUIRES_RECONCILIATION'); self.assertEqual(self.l.replay()['event_count'],1)
    def test_privacy_scan_rejects_obvious_secret_like_value(self):
        e=base(); e['source']['source_reference_sanitized']='token=SHOULD_NOT_EXIST'
        with self.assertRaises(PrivacyValidationError): self.l.append(e)
    def test_jsonl_replay_is_deterministic_across_restart(self): self.l.append(base()); self.l.append(settled()); self.assertEqual(self.l.replay(),CashTruthLedger(self.path,SCHEMA).replay())
    def test_cost_and_time_are_separate_and_no_labor_rate_is_inferred(self): self.l.append(settled()); self.l.append(cost()); self.l.append(time_event()); r=self.l.replay(); self.assertEqual(r['net_cash_contribution']['USD'],'8.25'); self.assertEqual(r['time_minutes_total'],7); self.assertEqual(r['inference_policy']['time_to_cash_conversion'],'NEVER_INFER')
    def test_same_event_id_with_different_payload_is_rejected(self): self.l.append(base()); x=base(); x['money']['amount_decimal']='11.00';
    def test_same_source_identity_with_changed_money_requires_reconciliation(self):
        self.l.append(base()); x=base(); x['event_id']='CHANGED'; x['money']['amount_decimal']='11.00'; self.assertEqual(self.l.append(x).status,'REQUIRES_RECONCILIATION')
    def test_same_provider_record_id_on_different_networks_does_not_false_dedupe(self):
        self.l.append(base()); x=base(); x['event_id']='IMPACT'; x['network']='impact.com'; self.assertEqual(self.l.append(x).status,'APPENDED')

# complete the different-payload assertion without duplicating fixture boilerplate
def _patch_conflict_test():
    def test(self):
        self.l.append(base()); x=base(); x['money']['amount_decimal']='11.00'
        with self.assertRaises(IdempotencyConflictError): self.l.append(x)
    T.test_same_event_id_with_different_payload_is_rejected=test
_patch_conflict_test()

if __name__=='__main__': unittest.main()
