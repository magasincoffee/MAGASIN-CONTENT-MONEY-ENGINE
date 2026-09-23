import unittest

from money_flow_probe import (
    is_sensitive_path,
    safe_query_keys,
    schema_shape,
)


class MoneyFlowProbeSafetyTests(unittest.TestCase):
    def test_query_values_are_not_returned(self):
        keys = safe_query_keys(
            "https://pub2-api.accesstrade.vn/v1/campaign/detail"
            "?campaign_id=123&token=SECRET&utm_source=tiktok"
        )
        self.assertEqual(
            keys,
            ["campaign_id", "utm_source"],
        )

    def test_sensitive_response_path_is_detected(self):
        self.assertTrue(
            is_sensitive_path(
                "https://pub2-api.accesstrade.vn/v1/payment/cross_check"
            )
        )
        self.assertTrue(
            is_sensitive_path(
                "https://pub2-api.accesstrade.vn/v1/publisher/identity-info"
            )
        )
        self.assertFalse(
            is_sensitive_path(
                "https://pub2-api.accesstrade.vn/v2/conversion/"
            )
        )

    def test_schema_records_types_not_values(self):
        source = {
            "campaign_id": 123,
            "url": "https://example.invalid/product",
            "token": "SECRET_VALUE",
            "nested": {
                "count": 4,
                "active": True,
            },
        }
        shape = schema_shape(source)
        encoded = str(shape)
        self.assertIn("campaign_id", encoded)
        self.assertIn("integer", encoded)
        self.assertIn("REDACTED_SENSITIVE_FIELD", encoded)
        self.assertNotIn("SECRET_VALUE", encoded)
        self.assertNotIn("example.invalid/product", encoded)


if __name__ == "__main__":
    unittest.main()
