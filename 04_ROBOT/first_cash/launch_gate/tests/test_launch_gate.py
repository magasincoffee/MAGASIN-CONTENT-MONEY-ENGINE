from __future__ import annotations
import ast, copy, json, sys, unittest
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve(); MOD=HERE.parents[1]; FIX=HERE.parent/'fixtures'; sys.path.insert(0,str(MOD))
from launch_gate import READY, NOT_READY, PrivacyLeakError, evaluate, privacy_scan, default_schema_path

def load(name): return json.loads((FIX/name).read_text(encoding='utf-8'))

class LaunchGateTests(unittest.TestCase):
    def test_schema_valid(self):
        s=json.loads(default_schema_path().read_text()); Draft202012Validator.check_schema(s)
    def test_current_realistic_l0_is_not_ready(self): self.assertEqual(evaluate(load('current_realistic_l0.json'))['result'],NOT_READY)
    def test_gate_a_unknown_not_ready(self):
        x=load('hypothetical_ready.json'); x['gate_a']['tracking_link_capability']={'status':'UNKNOWN','value':None,'source_reference_sanitized':None}; self.assertEqual(evaluate(x)['result'],NOT_READY)
    def test_blocked_not_ready(self):
        x=load('hypothetical_ready.json'); x['gate_a']['payout_feasibility']={'status':'BLOCKED','value':None,'source_reference_sanitized':None}; self.assertEqual(evaluate(x)['result'],NOT_READY)
    def test_missing_merchant_permission_not_ready(self):
        x=load('hypothetical_ready.json'); x['gate_a']['pinterest_social_allowed']={'status':'VERIFIED','value':False,'source_reference_sanitized':'fixture:no'}; self.assertEqual(evaluate(x)['result'],NOT_READY)
    def test_two_pins_not_ready(self):
        x=load('hypothetical_ready.json'); x['three_pin_package']['pins']=x['three_pin_package']['pins'][:2]; self.assertEqual(evaluate(x)['result'],NOT_READY)
    def test_four_pins_not_ready(self):
        x=load('hypothetical_ready.json'); p=copy.deepcopy(x['three_pin_package']['pins'][0]); p['content_id']='EXTRA'; x['three_pin_package']['pins'].append(p); self.assertEqual(evaluate(x)['result'],NOT_READY)
    def test_duplicate_content_id_not_ready(self):
        x=load('hypothetical_ready.json'); x['three_pin_package']['pins'][1]['content_id']=x['three_pin_package']['pins'][0]['content_id']; self.assertEqual(evaluate(x)['result'],NOT_READY)
    def test_one_pin_qa_fail_not_ready(self):
        x=load('hypothetical_ready.json'); x['three_pin_package']['pins'][1]['qa']={'status':'FAIL','value':False,'source_reference_sanitized':'fixture:qa-fail'}; self.assertEqual(evaluate(x)['result'],NOT_READY)
    def test_missing_observation_window_not_ready(self):
        x=load('hypothetical_ready.json'); x['observation']['window_locked']={'status':'UNKNOWN','value':None,'source_reference_sanitized':None}; x['observation']['window_reference']=None; self.assertEqual(evaluate(x)['result'],NOT_READY)
    def test_publish_safety_missing_not_ready(self):
        x=load('hypothetical_ready.json'); x['publish_safety']['reconciliation_before_retry']={'status':'BLOCKED','value':None,'source_reference_sanitized':None}; self.assertEqual(evaluate(x)['result'],NOT_READY)
    def test_cash_truth_sink_missing_not_ready(self):
        x=load('hypothetical_ready.json'); x['cash_truth']['local_private_jsonl_ready']={'status':'FAIL','value':False,'source_reference_sanitized':'fixture:fail'}; self.assertEqual(evaluate(x)['result'],NOT_READY)
    def test_auth_browser_unknown_not_ready(self):
        x=load('hypothetical_ready.json'); x['auth_browser']['future_authorized_prerequisite']={'status':'UNKNOWN','value':None,'source_reference_sanitized':None}; self.assertEqual(evaluate(x)['result'],NOT_READY)
    def test_side_effect_authorization_false_not_ready(self):
        x=load('hypothetical_ready.json'); x['side_effect_authorization']={'status':'VERIFIED','value':False,'source_reference_sanitized':'fixture:no-auth'}; self.assertEqual(evaluate(x)['result'],NOT_READY)
    def test_fully_verified_hypothetical_is_mechanically_ready(self): self.assertEqual(evaluate(load('hypothetical_ready.json'))['result'],READY)
    def test_ready_semantics_does_not_execute_publish(self): self.assertIn('does not execute',evaluate(load('hypothetical_ready.json'))['ready_semantics'])
    def test_privacy_secret_url_query_rejected(self):
        x=load('hypothetical_ready.json'); x['three_pin_package']['pins'][0]['destination_link_ref']='https://merchant.invalid/path?token=SECRET'
        with self.assertRaises(PrivacyLeakError): evaluate(x)
    def test_privacy_browser_profile_path_rejected(self):
        x=load('hypothetical_ready.json'); x['three_pin_package']['pins'][0]['output_reference']='C:/Users/me/AppData/Local/Google/Chrome/User Data/Default'
        with self.assertRaises(PrivacyLeakError): evaluate(x)
    def test_external_private_reference_placeholder_allowed(self):
        x=load('hypothetical_ready.json'); self.assertEqual(privacy_scan(x),[])
    def test_repeated_evaluation_deterministic(self):
        x=load('hypothetical_ready.json'); self.assertEqual(evaluate(x),evaluate(copy.deepcopy(x)))
    def test_non_2_by_3_metadata_not_ready(self):
        x=load('hypothetical_ready.json'); x['three_pin_package']['pins'][0]['width_px']=1200; self.assertEqual(evaluate(x)['result'],NOT_READY)
    def test_verified_unknown_link_label_not_ready(self):
        x=load('hypothetical_ready.json'); x['gate_a']['link_method']={'status':'VERIFIED','value':'UNKNOWN','source_reference_sanitized':'fixture:bad-link-label'}; self.assertEqual(evaluate(x)['result'],NOT_READY)
    def test_verified_evidence_without_source_reference_rejected(self):
        x=load('hypothetical_ready.json'); x['gate_a']['us_allowed']['source_reference_sanitized']=None
        from launch_gate import SchemaError
        with self.assertRaises(SchemaError): evaluate(x)
    def test_no_browser_api_network_imports(self):
        source=(MOD/'launch_gate.py').read_text(); tree=ast.parse(source); banned={'requests','httpx','socket','selenium','playwright','aiohttp','boto3'}; imported=set()
        for node in ast.walk(tree):
            if isinstance(node,ast.Import): imported.update(a.name.split('.')[0] for a in node.names)
            elif isinstance(node,ast.ImportFrom) and node.module: imported.add(node.module.split('.')[0])
        self.assertFalse(imported & banned, imported & banned)

if __name__=='__main__': unittest.main()
