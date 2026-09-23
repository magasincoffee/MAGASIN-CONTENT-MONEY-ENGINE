from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SCHEMA_VERSION = "magasin.local-browser-command.v1"
ALLOWED_ACTIONS = {"SHOPEE_AFFILIATE_LINK_SMOKE_TEST"}
ALLOWED_KEYS = {
    "schema_version",
    "command_id",
    "action",
    "product_url",
    "expected_shop_id",
    "expected_item_id",
    "created_at",
}
ALLOWED_PRODUCT_HOSTS = {"shopee.vn", "www.shopee.vn"}
CDP_URL = "http://127.0.0.1:9222"
AFFILIATE_URL = "https://affiliate.shopee.vn/offer/custom_link"

PRODUCT_PATH_RE = re.compile(r"^/product/(\d+)/(\d+)(?:/)?$")
PRODUCT_SLUG_RE = re.compile(r"-i\.(\d+)\.(\d+)(?:[/?#]|$)")
URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)


class CommandValidationError(ValueError):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _extract_product_ids(url: str) -> tuple[str, str] | None:
    parsed = urlparse(url)
    path_match = PRODUCT_PATH_RE.match(parsed.path)
    if path_match:
        return path_match.group(1), path_match.group(2)

    slug_match = PRODUCT_SLUG_RE.search(url)
    if slug_match:
        return slug_match.group(1), slug_match.group(2)

    # Some Shopee redirects preserve these IDs in query or fragment text.
    shop_match = re.search(r"(?:shopid|shop_id)[=/:%3D]+(\d+)", url, re.IGNORECASE)
    item_match = re.search(r"(?:itemid|item_id)[=/:%3D]+(\d+)", url, re.IGNORECASE)
    if shop_match and item_match:
        return shop_match.group(1), item_match.group(1)

    return None


def validate_command(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise CommandValidationError("Command must be a JSON object.")

    extra = set(data) - ALLOWED_KEYS
    if extra:
        raise CommandValidationError(
            "Unsupported command fields: " + ", ".join(sorted(extra))
        )

    if data.get("schema_version") != SCHEMA_VERSION:
        raise CommandValidationError("Unsupported schema_version.")

    action = data.get("action")
    if action not in ALLOWED_ACTIONS:
        raise CommandValidationError("Action is not allowlisted.")

    command_id = str(data.get("command_id", "")).strip()
    if not re.fullmatch(r"[A-Za-z0-9._-]{4,100}", command_id):
        raise CommandValidationError("Invalid command_id.")

    product_url = str(data.get("product_url", "")).strip()
    parsed = urlparse(product_url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_PRODUCT_HOSTS:
        raise CommandValidationError("product_url must be an HTTPS Shopee Vietnam URL.")

    ids = _extract_product_ids(product_url)
    if not ids:
        raise CommandValidationError("Could not extract shop/item IDs from product_url.")

    expected_shop_id = str(data.get("expected_shop_id", "")).strip()
    expected_item_id = str(data.get("expected_item_id", "")).strip()
    if not expected_shop_id.isdigit() or not expected_item_id.isdigit():
        raise CommandValidationError("Expected shop/item IDs must be numeric.")

    if ids != (expected_shop_id, expected_item_id):
        raise CommandValidationError(
            "Product URL IDs do not match expected_shop_id/expected_item_id."
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "command_id": command_id,
        "action": action,
        "product_url": product_url,
        "expected_shop_id": expected_shop_id,
        "expected_item_id": expected_item_id,
        "created_at": data.get("created_at"),
    }


def _safe_body_text(page: Any) -> str:
    try:
        return page.locator("body").inner_text(timeout=5000)
    except Exception:
        return ""


def _looks_logged_out(page: Any) -> bool:
    url = page.url.lower()
    if "login" in url or "signin" in url:
        return True

    body = _safe_body_text(page).lower()
    login_markers = [
        "đăng nhập",
        "login",
        "số điện thoại / tên đăng nhập / email",
        "phone number / username / email",
    ]
    affiliate_markers = [
        "custom link",
        "lấy link",
        "hoa hồng",
        "affiliate",
        "tiếp thị liên kết",
    ]
    return any(marker in body for marker in login_markers) and not any(
        marker in body for marker in affiliate_markers
    )


def _visible_first(page: Any, selectors: list[str]) -> Any | None:
    for selector in selectors:
        try:
            loc = page.locator(selector)
            count = min(loc.count(), 20)
            for index in range(count):
                item = loc.nth(index)
                if item.is_visible(timeout=500):
                    return item
        except Exception:
            continue
    return None


def _click_text_candidate(page: Any, labels: list[str]) -> bool:
    for label in labels:
        patterns = [
            f"button:has-text('{label}')",
            f"a:has-text('{label}')",
            f"[role='button']:has-text('{label}')",
            f"text={label}",
        ]
        target = _visible_first(page, patterns)
        if target is None:
            continue
        try:
            target.click(timeout=5000)
            page.wait_for_timeout(1200)
            return True
        except Exception:
            continue
    return False


def _ensure_custom_link_page(page: Any) -> None:
    page.goto(AFFILIATE_URL, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(1500)

    if _looks_logged_out(page):
        return

    input_selectors = [
        "input[placeholder*='link' i]",
        "input[placeholder*='url' i]",
        "input[placeholder*='đường dẫn' i]",
        "textarea[placeholder*='link' i]",
        "textarea[placeholder*='url' i]",
    ]
    if _visible_first(page, input_selectors) is not None:
        return

    _click_text_candidate(
        page,
        [
            "Custom Link",
            "Lấy link",
            "Tạo link",
            "Hoa hồng Sản phẩm",
            "Hoa hồng sản phẩm",
        ],
    )


def _find_product_input(page: Any) -> Any | None:
    return _visible_first(
        page,
        [
            "input[placeholder*='link sản phẩm' i]",
            "input[placeholder*='product link' i]",
            "input[placeholder*='link' i]",
            "input[placeholder*='url' i]",
            "input[placeholder*='đường dẫn' i]",
            "textarea[placeholder*='link' i]",
            "textarea[placeholder*='url' i]",
            "textarea",
        ],
    )


def _collect_urls(page: Any) -> list[str]:
    urls: list[str] = []

    for selector in ["input", "textarea"]:
        try:
            loc = page.locator(selector)
            for i in range(min(loc.count(), 100)):
                value = loc.nth(i).input_value(timeout=500)
                if value and value.startswith("http"):
                    urls.append(value.strip())
        except Exception:
            pass

    try:
        links = page.locator("a[href]")
        for i in range(min(links.count(), 200)):
            href = links.nth(i).get_attribute("href", timeout=500)
            if href and href.startswith("http"):
                urls.append(href.strip())
    except Exception:
        pass

    body = _safe_body_text(page)
    urls.extend(match.rstrip(".,);]") for match in URL_RE.findall(body))

    # Preserve order while deduplicating.
    seen: set[str] = set()
    result: list[str] = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            result.append(url)
    return result


def _affiliate_url_score(url: str, product_url: str) -> int:
    if url == product_url:
        return -1000

    host = (urlparse(url).hostname or "").lower()
    score = 0
    if host == "s.shopee.vn":
        score += 100
    elif host.endswith("shope.ee"):
        score += 95
    elif host.endswith("shopee.vn"):
        score += 60

    lowered = url.lower()
    for marker in ["affiliate", "utm_", "sub_id", "subid", "af_", "uls_trackid"]:
        if marker in lowered:
            score += 10
    return score


def _choose_affiliate_url(urls: list[str], product_url: str) -> str | None:
    ranked = sorted(
        (( _affiliate_url_score(url, product_url), url) for url in urls),
        reverse=True,
    )
    if not ranked or ranked[0][0] <= 0:
        return None
    return ranked[0][1]


def _verification_urls(page: Any) -> list[str]:
    urls = [page.url]
    for selector, attr in [
        ("link[rel='canonical']", "href"),
        ("meta[property='og:url']", "content"),
    ]:
        try:
            loc = page.locator(selector)
            if loc.count():
                value = loc.first.get_attribute(attr, timeout=1000)
                if value:
                    urls.append(value)
        except Exception:
            pass
    return urls


def execute_shopee_smoke_test(command: dict[str, Any], evidence_dir: Path) -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "Playwright is not installed. Run run_local_command.ps1."
        ) from exc

    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = evidence_dir / f"{command['command_id']}.json"

    evidence: dict[str, Any] = {
        "schema_version": "magasin.local-browser-evidence.v1",
        "command_id": command["command_id"],
        "action": command["action"],
        "status": "RUNNING",
        "product_url": command["product_url"],
        "expected_shop_id": command["expected_shop_id"],
        "expected_item_id": command["expected_item_id"],
        "generated_affiliate_link": None,
        "redirect_status": "NOT_ATTEMPTED",
        "final_product_match": False,
        "final_url_sanitized": None,
        "observed_at": _utc_now(),
        "credentials_captured": False,
        "cookies_exported": False,
        "purchase_performed": False,
        "messages_sent": False,
        "payout_kyc_tax_changed": False,
    }

    def save() -> None:
        evidence["observed_at"] = _utc_now()
        evidence_path.write_text(
            json.dumps(evidence, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        if not browser.contexts:
            evidence["status"] = "BLOCKED_NO_BROWSER_CONTEXT"
            save()
            return 20

        context = browser.contexts[0]
        pages = context.pages
        page = next(
            (x for x in pages if "affiliate.shopee.vn" in x.url),
            pages[0] if pages else context.new_page(),
        )

        _ensure_custom_link_page(page)

        if _looks_logged_out(page):
            evidence["status"] = "WAIT_OWNER_LOGIN_REQUIRED"
            evidence["reason"] = (
                "Dedicated MAGASIN Chrome profile is not authenticated to Shopee Affiliate. "
                "Owner must log in once in that profile and complete OTP/MFA/CAPTCHA personally."
            )
            save()
            return 10

        product_input = _find_product_input(page)
        if product_input is None:
            evidence["status"] = "FAIL_CUSTOM_LINK_INPUT_NOT_FOUND"
            evidence["page_url_sanitized"] = page.url
            save()
            return 20

        product_input.fill(command["product_url"])

        clicked = _click_text_candidate(
            page,
            ["Lấy link", "Tạo link", "Generate Link", "Generate", "Chuyển đổi"],
        )
        if not clicked:
            evidence["status"] = "FAIL_GENERATE_BUTTON_NOT_FOUND"
            save()
            return 20

        page.wait_for_timeout(2500)
        affiliate_url = _choose_affiliate_url(
            _collect_urls(page),
            command["product_url"],
        )
        if not affiliate_url:
            evidence["status"] = "FAIL_AFFILIATE_LINK_NOT_FOUND"
            save()
            return 20

        evidence["generated_affiliate_link"] = affiliate_url
        evidence["generation_status"] = "GENERATED"

        verify_page = context.new_page()
        try:
            response = verify_page.goto(
                affiliate_url,
                wait_until="domcontentloaded",
                timeout=45000,
            )
            verify_page.wait_for_timeout(2500)
            final_urls = _verification_urls(verify_page)
            final_url = final_urls[0] if final_urls else verify_page.url
            evidence["final_url_sanitized"] = final_url
            evidence["http_status"] = response.status if response else None

            expected = (
                command["expected_shop_id"],
                command["expected_item_id"],
            )
            match = False
            matched_source = None
            for candidate_url in final_urls:
                ids = _extract_product_ids(candidate_url)
                if ids == expected:
                    match = True
                    matched_source = candidate_url
                    break

            evidence["final_product_match"] = match
            evidence["match_source_sanitized"] = matched_source
            evidence["redirect_status"] = "VERIFIED" if match else "WRONG_OR_UNPROVEN_PRODUCT"
            evidence["status"] = "VERIFIED" if match else "FAIL_REDIRECT_MISMATCH"
            save()
            return 0 if match else 20
        finally:
            verify_page.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--command-file", required=True)
    parser.add_argument(
        "--evidence-dir",
        default="04_ROBOT/local_browser_runner/evidence",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    command_path = Path(args.command_file)
    evidence_dir = Path(args.evidence_dir)

    try:
        raw = json.loads(command_path.read_text(encoding="utf-8"))
        command = validate_command(raw)
    except (OSError, json.JSONDecodeError, CommandValidationError) as exc:
        evidence_dir.mkdir(parents=True, exist_ok=True)
        failure = {
            "schema_version": "magasin.local-browser-evidence.v1",
            "status": "BLOCKED_INVALID_COMMAND",
            "reason": str(exc),
            "observed_at": _utc_now(),
        }
        (evidence_dir / "invalid-command.json").write_text(
            json.dumps(failure, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"[BLOCKED] {exc}", file=sys.stderr)
        return 2

    if command["action"] == "SHOPEE_AFFILIATE_LINK_SMOKE_TEST":
        return execute_shopee_smoke_test(command, evidence_dir)

    print("[BLOCKED] Action not implemented.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
