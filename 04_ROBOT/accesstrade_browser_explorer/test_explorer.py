import unittest

from explorer import (
    is_accesstrade_network_host,
    is_blocked_url,
    is_sensitive_url,
    sanitize_url,
)


class ExplorerSafetyTests(unittest.TestCase):
    def test_strips_sensitive_query(self):
        url = sanitize_url(
            "https://pub2.accesstrade.vn/campaign?id=123&token=SECRET&code=SECRET2"
        )
        self.assertEqual(
            url,
            "https://pub2.accesstrade.vn/campaign?id=123",
        )

    def test_drops_unknown_query(self):
        url = sanitize_url(
            "https://pub2.accesstrade.vn/report?page=10&search=my-secret-query"
        )
        self.assertEqual(
            url,
            "https://pub2.accesstrade.vn/report",
        )

    def test_blocks_logout(self):
        self.assertTrue(
            is_blocked_url(
                "https://pub2.accesstrade.vn/logout"
            )
        )

    def test_sensitive_payment_page(self):
        self.assertTrue(
            is_sensitive_url(
                "https://pub2.accesstrade.vn/payment/profile"
            )
        )

    def test_rejects_javascript(self):
        self.assertIsNone(
            sanitize_url("javascript:void(0)")
        )

    def test_accesstrade_api_subdomain_is_observable(self):
        self.assertTrue(
            is_accesstrade_network_host(
                "https://api.accesstrade.vn/v1/campaigns"
            )
        )
        self.assertFalse(
            is_accesstrade_network_host(
                "https://example.com/v1/campaigns"
            )
        )


if __name__ == "__main__":
    unittest.main()
