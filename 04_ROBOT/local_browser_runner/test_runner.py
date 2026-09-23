import json
import unittest

from runner import CommandValidationError, validate_command


class CommandValidationTests(unittest.TestCase):
    def valid(self):
        return {
            "schema_version": "magasin.local-browser-command.v1",
            "command_id": "MCME-049-smoke-01",
            "action": "SHOPEE_AFFILIATE_LINK_SMOKE_TEST",
            "product_url": "https://shopee.vn/product/1651109667/27495157821",
            "expected_shop_id": "1651109667",
            "expected_item_id": "27495157821",
            "created_at": "2026-09-23T22:00:00+07:00",
        }

    def test_valid_command(self):
        out = validate_command(self.valid())
        self.assertEqual(out["expected_shop_id"], "1651109667")
        self.assertEqual(out["expected_item_id"], "27495157821")

    def test_rejects_non_shopee_host(self):
        data = self.valid()
        data["product_url"] = "https://example.com/product/1651109667/27495157821"
        with self.assertRaises(CommandValidationError):
            validate_command(data)

    def test_rejects_id_mismatch(self):
        data = self.valid()
        data["expected_item_id"] = "999"
        with self.assertRaises(CommandValidationError):
            validate_command(data)

    def test_rejects_arbitrary_shell_field(self):
        data = self.valid()
        data["shell_command"] = "Remove-Item C:\\* -Recurse"
        with self.assertRaises(CommandValidationError):
            validate_command(data)

    def test_rejects_non_allowlisted_action(self):
        data = self.valid()
        data["action"] = "RUN_POWERSHELL"
        with self.assertRaises(CommandValidationError):
            validate_command(data)


if __name__ == "__main__":
    unittest.main()
