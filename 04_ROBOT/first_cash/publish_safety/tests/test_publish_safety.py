from __future__ import annotations

import ast
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
MODULE_DIR = HERE.parents[1]
FIXTURE = HERE.parent / "fixtures" / "intent.json"
sys.path.insert(0, str(MODULE_DIR))

from publish_safety import (
    LatchStore,
    MAX_SEND_ATTEMPTS,
    MockBackend,
    MockReconciler,
    PrivacyValidationError,
    PublishIntent,
    PublishSafetyMachine,
    RECON_CONFIRMED_ABSENT,
    RECON_UNKNOWN,
    STATE_BLOCKED_AMBIGUOUS,
    STATE_BLOCKED_AUTH,
    STATE_CONFIRMED,
    STATE_FAILED_CONFIRMED,
    STATE_PREPARED,
    STATE_SEND_STARTED,
    publish_key,
)


def intent() -> PublishIntent:
    raw = json.loads(FIXTURE.read_text(encoding="utf-8"))["intent"]
    return PublishIntent.from_dict(raw)


class PublishSafetyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.store_dir = self.root / "private" / "latches"
        self.mock_state = self.root / "mock" / "platform.json"

    def tearDown(self):
        self.tmp.cleanup()

    def machine(self, outcomes=None, overrides=None):
        backend = MockBackend(self.mock_state, outcomes or [])
        reconciler = MockReconciler(backend, overrides)
        return PublishSafetyMachine(LatchStore(self.store_dir), backend, reconciler), backend, reconciler

    def test_deterministic_key_stable_across_restart(self):
        i = intent()
        first = publish_key(i)
        second = publish_key(PublishIntent.from_dict(json.loads(json.dumps(i.__dict__))))
        self.assertEqual(first, second)

    def test_content_version_changes_key(self):
        i = intent()
        changed = PublishIntent(i.experiment_id, i.content_id, "v2", i.destination_version)
        self.assertNotEqual(publish_key(i), publish_key(changed))

    def test_destination_version_changes_key(self):
        i = intent()
        changed = PublishIntent(i.experiment_id, i.content_id, i.content_version, "destination-v2")
        self.assertNotEqual(publish_key(i), publish_key(changed))

    def test_prepared_latch_is_persisted_before_send(self):
        m, backend, _ = self.machine(["success"])
        r = m.run(intent())
        persisted = LatchStore(self.store_dir).load(r["publish_key"])
        history = [x["state"] for x in persisted["transition_history"]]
        self.assertEqual(history[0], STATE_PREPARED)
        self.assertIn(STATE_SEND_STARTED, history)
        self.assertEqual(backend.send_count, 1)

    def test_happy_path_confirms(self):
        m, backend, _ = self.machine(["success"])
        r = m.run(intent())
        self.assertEqual(r["state"], STATE_CONFIRMED)
        self.assertEqual(r["attempt_count"], 1)
        self.assertTrue(r["published_id_sanitized"].startswith("MOCKPIN-"))
        self.assertEqual(backend.send_count, 1)

    def test_second_invocation_after_confirmed_zero_additional_send(self):
        m, backend, _ = self.machine(["success"])
        self.assertEqual(m.run(intent())["state"], STATE_CONFIRMED)
        restarted = PublishSafetyMachine(LatchStore(self.store_dir), MockBackend(self.mock_state, ["success"]), MockReconciler(MockBackend(self.mock_state)))
        self.assertEqual(restarted.run(intent())["state"], STATE_CONFIRMED)
        self.assertEqual(backend.send_count, 1)

    def test_timeout_after_send_blocks_and_requires_reconcile(self):
        m, backend, reconciler = self.machine(["timeout_no_create"])
        r = m.run(intent())
        self.assertEqual(r["state"], STATE_BLOCKED_AMBIGUOUS)
        self.assertEqual(backend.send_count, 1)
        self.assertEqual(reconciler.calls, 0)
        r2 = m.run(intent())
        self.assertEqual(reconciler.calls, 1)
        self.assertEqual(r2["attempt_count"], 2)  # CONFIRMED_ABSENT unlocked exactly one retry
        self.assertEqual(backend.send_count, 2)

    def test_send_started_after_restart_reconciles_before_any_send(self):
        i = intent()
        store = LatchStore(self.store_dir)
        record = store.prepare(i)
        record = store.transition(record, STATE_SEND_STARTED, increment_attempt=True)
        key = record["publish_key"]
        backend = MockBackend(self.mock_state, ["success"])
        reconciler = MockReconciler(backend, {key: RECON_UNKNOWN})
        restarted = PublishSafetyMachine(store, backend, reconciler)
        result = restarted.run(i)
        self.assertEqual(result["state"], STATE_BLOCKED_AMBIGUOUS)
        self.assertEqual(reconciler.calls, 1)
        self.assertEqual(backend.send_count, 0)

    def test_ambiguous_reconciliation_stays_blocked_zero_resend(self):
        i = intent()
        m, backend, _ = self.machine(["ambiguous_no_create"])
        first = m.run(i)
        self.assertEqual(first["state"], STATE_BLOCKED_AMBIGUOUS)
        key = first["publish_key"]
        restarted_backend = MockBackend(self.mock_state, ["success"])
        reconciler = MockReconciler(restarted_backend, {key: RECON_UNKNOWN})
        restarted = PublishSafetyMachine(LatchStore(self.store_dir), restarted_backend, reconciler)
        second = restarted.run(i)
        self.assertEqual(second["state"], STATE_BLOCKED_AMBIGUOUS)
        self.assertEqual(restarted_backend.send_count, 1)
        self.assertEqual(reconciler.calls, 1)

    def test_confirmed_present_after_restart_confirms_without_resend(self):
        i = intent()
        m, backend, _ = self.machine(["timeout_after_create"])
        first = m.run(i)
        self.assertEqual(first["state"], STATE_BLOCKED_AMBIGUOUS)
        self.assertEqual(backend.send_count, 1)
        restarted_backend = MockBackend(self.mock_state, ["success"])
        restarted = PublishSafetyMachine(LatchStore(self.store_dir), restarted_backend, MockReconciler(restarted_backend))
        second = restarted.run(i)
        self.assertEqual(second["state"], STATE_CONFIRMED)
        self.assertEqual(restarted_backend.send_count, 1)

    def test_confirmed_absent_allows_at_most_one_bounded_retry(self):
        i = intent()
        m, backend, _ = self.machine(["timeout_no_create", "success"])
        first = m.run(i)
        self.assertEqual(first["state"], STATE_BLOCKED_AMBIGUOUS)
        second = m.run(i)
        self.assertEqual(second["state"], STATE_CONFIRMED)
        self.assertEqual(second["attempt_count"], MAX_SEND_ATTEMPTS)
        self.assertEqual(backend.send_count, 2)
        third = m.run(i)
        self.assertEqual(third["state"], STATE_CONFIRMED)
        self.assertEqual(backend.send_count, 2)

    def test_retry_exhaustion_becomes_failed_confirmed(self):
        i = intent()
        m, backend, _ = self.machine(["timeout_no_create", "timeout_no_create"])
        self.assertEqual(m.run(i)["state"], STATE_BLOCKED_AMBIGUOUS)
        self.assertEqual(m.run(i)["state"], STATE_BLOCKED_AMBIGUOUS)
        third = m.run(i)
        self.assertEqual(third["state"], STATE_FAILED_CONFIRMED)
        self.assertEqual(third["attempt_count"], MAX_SEND_ATTEMPTS)
        self.assertEqual(backend.send_count, 2)

    def test_auth_block_is_terminal_zero_retry(self):
        i = intent()
        m, backend, _ = self.machine(["auth_block", "success"])
        first = m.run(i)
        self.assertEqual(first["state"], STATE_BLOCKED_AUTH)
        second = m.run(i)
        self.assertEqual(second["state"], STATE_BLOCKED_AUTH)
        self.assertEqual(backend.send_count, 1)

    def test_repeated_restarts_do_not_duplicate_confirmed_send(self):
        i = intent()
        m, backend, _ = self.machine(["success"])
        self.assertEqual(m.run(i)["state"], STATE_CONFIRMED)
        for _ in range(5):
            b = MockBackend(self.mock_state, ["success"])
            machine = PublishSafetyMachine(LatchStore(self.store_dir), b, MockReconciler(b))
            self.assertEqual(machine.run(i)["state"], STATE_CONFIRMED)
        self.assertEqual(backend.send_count, 1)

    def test_private_intent_payload_rejected(self):
        raw = intent().__dict__.copy()
        raw["destination_version"] = "https://merchant.invalid/?token=SECRET"
        with self.assertRaises(PrivacyValidationError):
            PublishIntent.from_dict(raw)

    def test_latch_file_is_private_mode_when_supported(self):
        m, _, _ = self.machine(["success"])
        r = m.run(intent())
        path = self.store_dir / f"{r['publish_key']}.json"
        self.assertTrue(path.exists())
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

    def test_no_browser_api_network_imports(self):
        source = (MODULE_DIR / "publish_safety.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        banned = {"requests", "httpx", "urllib", "socket", "selenium", "playwright", "aiohttp", "boto3"}
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertFalse(imported & banned, imported & banned)


if __name__ == "__main__":
    unittest.main()
