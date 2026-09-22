#!/usr/bin/env python3
"""
ACCESSTRADE Browser Explorer V1

Read-only browser mapper for an Owner-authorized ACCESSTRADE publisher account.

Security model:
- Owner performs login manually in a visible browser.
- The robot never asks for or records passwords, OTPs, cookies, localStorage,
  request headers, request bodies, or input values.
- It navigates same-origin GET pages discovered from links.
- It never clicks buttons or submits forms.
- Sensitive pages are mapped structurally but body text is suppressed by default.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from collections import Counter, deque
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

from playwright.async_api import Page, Response, async_playwright


DEFAULT_START_URL = "https://pub2.accesstrade.vn/report/overview"
DEFAULT_ALLOWED_HOSTS = {"pub2.accesstrade.vn"}

BLOCKED_URL_KEYWORDS = {
    "logout",
    "log-out",
    "signout",
    "sign-out",
    "delete",
    "remove-account",
    "close-account",
    "deactivate",
    "unsubscribe",
}

SENSITIVE_PATH_KEYWORDS = {
    "payment",
    "payout",
    "withdraw",
    "bank",
    "tax",
    "kyc",
    "profile",
    "account",
    "setting",
    "thanh-toan",
    "thue",
}

SAFE_QUERY_KEYS = {
    "id",
    "campaign_id",
    "campaignid",
    "offer_id",
    "offerid",
    "tool",
    "type",
    "tab",
    "category",
}

SENSITIVE_QUERY_KEYS = {
    "token",
    "access_token",
    "refresh_token",
    "code",
    "secret",
    "signature",
    "sig",
    "key",
    "api_key",
    "apikey",
    "session",
    "sid",
    "jwt",
    "auth",
}

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?84|0)(?:[ .-]?\d){8,10}(?!\d)")
LONG_DIGIT_RE = re.compile(r"(?<!\d)\d{9,19}(?!\d)")
TOKENISH_RE = re.compile(r"\b[A-Za-z0-9_-]{32,}\b")


@dataclass
class PageRecord:
    url: str
    title: str
    status: int | None
    sensitive: bool
    headings: list[str]
    nav_labels: list[str]
    buttons: list[str]
    forms: list[dict[str, Any]]
    internal_links: list[dict[str, str]]
    external_link_count: int
    text_excerpt: str
    discovered_at: str
    error: str | None = None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def redact_text(value: str) -> str:
    value = EMAIL_RE.sub("[REDACTED_EMAIL]", value)
    value = PHONE_RE.sub("[REDACTED_PHONE]", value)
    value = LONG_DIGIT_RE.sub("[REDACTED_NUMBER]", value)
    value = TOKENISH_RE.sub("[REDACTED_TOKEN]", value)
    return value


def clean_text(value: str, max_len: int = 300) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    return redact_text(value)[:max_len]


def sanitize_url(
    raw_url: str,
    base_url: str | None = None,
    keep_safe_query: bool = True,
) -> str | None:
    if not raw_url:
        return None

    raw_url = raw_url.strip()
    lowered = raw_url.lower()
    if lowered.startswith(("javascript:", "mailto:", "tel:", "data:", "blob:", "file:")):
        return None

    absolute = urljoin(base_url or "", raw_url)
    parts = urlsplit(absolute)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        return None

    query = ""
    if keep_safe_query and parts.query:
        safe_pairs: list[tuple[str, str]] = []
        for key, value in parse_qsl(parts.query, keep_blank_values=False):
            lk = key.lower()
            if lk in SENSITIVE_QUERY_KEYS:
                continue
            if lk in SAFE_QUERY_KEYS:
                safe_pairs.append((key, clean_text(value, 120)))
        query = urlencode(safe_pairs, doseq=True)

    fragment = parts.fragment if parts.fragment.startswith("/") else ""
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    return urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), path, query, fragment)
    )


def endpoint_url(raw_url: str) -> str:
    parts = urlsplit(raw_url)
    return urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), parts.path, "", "")
    )


def same_origin(url: str, allowed_hosts: set[str]) -> bool:
    return (urlsplit(url).hostname or "").lower() in allowed_hosts


def is_blocked_url(url: str) -> bool:
    lower = url.lower()
    return any(keyword in lower for keyword in BLOCKED_URL_KEYWORDS)


def is_sensitive_url(url: str) -> bool:
    parts = urlsplit(url)
    target = (parts.path + "?" + parts.query).lower()
    return any(keyword in target for keyword in SENSITIVE_PATH_KEYWORDS)


def route_bucket(url: str) -> str:
    parts = urlsplit(url)
    return f"{parts.netloc.lower()}{parts.path}"


async def extract_page(
    page: Page,
    status: int | None,
    allowed_hosts: set[str],
) -> tuple[PageRecord, list[str]]:
    current_url = sanitize_url(page.url, keep_safe_query=True) or page.url
    sensitive = is_sensitive_url(current_url)

    title = clean_text(await page.title(), 300)

    headings = await page.locator("h1,h2,h3,[role='heading']").all_inner_texts()
    headings = [clean_text(x, 250) for x in headings if clean_text(x, 250)][:80]

    nav_labels = await page.locator(
        "nav a, aside a, [role='navigation'] a, [role='menuitem']"
    ).all_inner_texts()
    nav_labels = [
        clean_text(x, 180) for x in nav_labels if clean_text(x, 180)
    ][:120]

    buttons = await page.locator("button,[role='button']").all_inner_texts()
    buttons = [clean_text(x, 180) for x in buttons if clean_text(x, 180)][:120]

    forms: list[dict[str, Any]] = []
    if not sensitive:
        form_data = await page.locator("form").evaluate_all(
            """forms => forms.slice(0, 40).map(form => ({
                method: (form.method || 'GET').toUpperCase(),
                action: form.action || '',
                inputs: Array.from(
                    form.querySelectorAll('input,select,textarea')
                ).slice(0, 80).map(el => ({
                    tag: el.tagName.toLowerCase(),
                    type: (el.getAttribute('type') || '').toLowerCase(),
                    name: el.getAttribute('name') || '',
                    autocomplete: el.getAttribute('autocomplete') || ''
                }))
            }))"""
        )
        for form in form_data:
            safe_action = sanitize_url(
                form.get("action", ""),
                page.url,
                keep_safe_query=False,
            )
            forms.append(
                {
                    "method": form.get("method", "GET"),
                    "action": safe_action or "",
                    "inputs": form.get("inputs", []),
                }
            )

    anchor_data = await page.locator("a[href]").evaluate_all(
        """els => els.slice(0, 1500).map(a => ({
            href: a.href || '',
            text: (
                a.innerText ||
                a.getAttribute('aria-label') ||
                a.title ||
                ''
            ).trim()
        }))"""
    )

    internal_links: list[dict[str, str]] = []
    next_urls: list[str] = []
    external_count = 0
    seen_urls: set[str] = set()

    for item in anchor_data:
        safe_url = sanitize_url(
            item.get("href", ""),
            page.url,
            keep_safe_query=True,
        )
        if not safe_url:
            continue

        if same_origin(safe_url, allowed_hosts):
            if is_blocked_url(safe_url):
                continue
            if safe_url not in seen_urls:
                seen_urls.add(safe_url)
                internal_links.append(
                    {
                        "url": safe_url,
                        "label": clean_text(item.get("text", ""), 180),
                    }
                )
                next_urls.append(safe_url)
        else:
            external_count += 1

    body_text = ""
    if not sensitive:
        try:
            body_text = await page.locator("body").inner_text(timeout=5000)
        except Exception:
            body_text = ""
        body_text = clean_text(body_text, 12000)

    record = PageRecord(
        url=current_url,
        title=title,
        status=status,
        sensitive=sensitive,
        headings=headings,
        nav_labels=nav_labels,
        buttons=buttons,
        forms=forms,
        internal_links=internal_links[:500],
        external_link_count=external_count,
        text_excerpt=body_text,
        discovered_at=now_iso(),
    )
    return record, next_urls


async def map_site(
    start_url: str,
    output_dir: Path,
    max_pages: int,
    delay_ms: int,
    max_variants_per_route: int,
    allowed_hosts: set[str],
    login_wait: bool,
    timeout_ms: int,
    profile_dir: Path | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    pages_path = output_dir / "pages.jsonl"
    endpoints_path = output_dir / "network_endpoints.json"
    site_map_path = output_dir / "site_map.json"
    summary_path = output_dir / "summary.md"

    pages: list[PageRecord] = []
    network_events: dict[tuple[str, str, int], dict[str, Any]] = {}
    route_counts: Counter[str] = Counter()
    failures: list[dict[str, str]] = []

    async with async_playwright() as p:
        browser = None

        if profile_dir:
            profile_dir.mkdir(parents=True, exist_ok=True)
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(profile_dir),
                headless=False,
                viewport={"width": 1440, "height": 1000},
            )
        else:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                viewport={"width": 1440, "height": 1000}
            )

        context.set_default_timeout(timeout_ms)
        page = context.pages[0] if context.pages else await context.new_page()

        async def on_response(response: Response) -> None:
            try:
                request = response.request
                if not same_origin(request.url, allowed_hosts):
                    return

                url = endpoint_url(request.url)
                key = (request.method, url, response.status)
                network_events[key] = {
                    "method": request.method,
                    "url": url,
                    "status": response.status,
                    "resource_type": request.resource_type,
                }
            except Exception:
                return

        page.on("response", on_response)

        print(f"[OPEN] {start_url}")
        await page.goto(start_url, wait_until="domcontentloaded")

        if login_wait:
            print("\n[OWNER ACTION REQUIRED]")
            print("1) Login normally in the opened Chromium window.")
            print("2) Complete MFA/CAPTCHA yourself if requested.")
            print("3) Navigate to the ACCESSTRADE publisher dashboard.")
            print("4) Return here and press ENTER.")
            await asyncio.to_thread(
                input,
                "\nPress ENTER after login is complete: ",
            )

        seed = (
            sanitize_url(page.url, keep_safe_query=True)
            or sanitize_url(start_url, keep_safe_query=True)
        )
        if not seed:
            raise RuntimeError(
                "Could not determine a valid seed URL after login."
            )
        if not same_origin(seed, allowed_hosts):
            raise RuntimeError(
                f"After login the browser is outside allowed hosts: {seed}"
            )

        queue: deque[str] = deque([seed])
        queued: set[str] = {seed}
        visited: set[str] = set()

        while queue and len(visited) < max_pages:
            url = queue.popleft()
            if url in visited or is_blocked_url(url):
                continue

            bucket = route_bucket(url)
            if route_counts[bucket] >= max_variants_per_route:
                continue

            print(f"[{len(visited) + 1}/{max_pages}] {url}")
            status: int | None = None

            try:
                response = await page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=timeout_ms,
                )
                status = response.status if response else None
                await page.wait_for_timeout(delay_ms)

                final_url = sanitize_url(
                    page.url,
                    keep_safe_query=True,
                ) or url

                if not same_origin(final_url, allowed_hosts):
                    print(
                        "  [SKIP] redirected outside allowed host: "
                        f"{final_url}"
                    )
                    continue

                record, discovered = await extract_page(
                    page,
                    status,
                    allowed_hosts,
                )
                pages.append(record)
                visited.add(url)
                route_counts[bucket] += 1

                with pages_path.open("a", encoding="utf-8") as fh:
                    fh.write(
                        json.dumps(
                            asdict(record),
                            ensure_ascii=False,
                        )
                        + "\n"
                    )

                for candidate in discovered:
                    if (
                        candidate not in visited
                        and candidate not in queued
                        and not is_blocked_url(candidate)
                        and route_counts[route_bucket(candidate)]
                        < max_variants_per_route
                    ):
                        queue.append(candidate)
                        queued.add(candidate)

            except Exception as exc:
                message = clean_text(str(exc), 500)
                print(f"  [ERROR] {message}")
                failures.append(
                    {
                        "url": url,
                        "error": message,
                    }
                )
                visited.add(url)

        endpoint_values = sorted(
            network_events.values(),
            key=lambda item: (
                item["url"],
                item["method"],
                item["status"],
            ),
        )

        endpoints_path.write_text(
            json.dumps(
                endpoint_values,
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        graph = {
            "schema_version": "mcme.accesstrade-site-map.v1",
            "generated_at": now_iso(),
            "start_url": sanitize_url(
                start_url,
                keep_safe_query=False,
            ),
            "allowed_hosts": sorted(allowed_hosts),
            "page_count": len(pages),
            "failure_count": len(failures),
            "network_endpoint_count": len(endpoint_values),
            "pages": [
                {
                    "url": item.url,
                    "title": item.title,
                    "status": item.status,
                    "sensitive": item.sensitive,
                    "headings": item.headings,
                    "internal_links": item.internal_links,
                }
                for item in pages
            ],
            "failures": failures,
        }

        site_map_path.write_text(
            json.dumps(
                graph,
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        title_counts = Counter(
            item.title or "(untitled)" for item in pages
        )
        sensitive_count = sum(
            1 for item in pages if item.sensitive
        )

        summary_lines = [
            "# ACCESSTRADE Browser Explorer V1 — Scan Summary",
            "",
            f"- Generated: {graph['generated_at']}",
            f"- Pages mapped: **{len(pages)}**",
            (
                "- Sensitive pages mapped structurally: "
                f"**{sensitive_count}**"
            ),
            f"- Navigation failures: **{len(failures)}**",
            (
                "- Same-origin network endpoints observed: "
                f"**{len(endpoint_values)}**"
            ),
            "",
            "## Page titles",
            "",
        ]

        for page_title, count in title_counts.most_common(100):
            summary_lines.append(
                f"- {count} × {page_title}"
            )

        summary_lines.extend(
            [
                "",
                "## Safety notes",
                "",
                (
                    "- No password/OTP/cookie/localStorage/"
                    "request-body data is intentionally recorded."
                ),
                "- No forms are submitted and no buttons are clicked.",
                (
                    "- Sensitive pages suppress body text "
                    "by default."
                ),
                (
                    "- Network endpoint logging strips query strings "
                    "and never stores headers/bodies."
                ),
                "",
                "## Next step",
                "",
                (
                    "Use this map to build narrowly-scoped read adapters "
                    "for campaigns, deeplink tools, product offers and "
                    "reporting. Write actions require a separate "
                    "Owner-authorized task."
                ),
            ]
        )

        summary_path.write_text(
            "\n".join(summary_lines) + "\n",
            encoding="utf-8",
        )

        print("\n[DONE]")
        print(f"Mapped pages: {len(pages)}")
        print(f"Output: {output_dir.resolve()}")

        await context.close()
        if browser:
            await browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only ACCESSTRADE publisher-site browser explorer."
        )
    )
    parser.add_argument(
        "--start-url",
        default=DEFAULT_START_URL,
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=180,
    )
    parser.add_argument(
        "--delay-ms",
        type=int,
        default=700,
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=20000,
    )
    parser.add_argument(
        "--max-variants-per-route",
        type=int,
        default=4,
    )
    parser.add_argument(
        "--allowed-host",
        action="append",
        dest="allowed_hosts",
        help=(
            "Allowed hostname. Repeat for more hosts. "
            "Defaults to pub2.accesstrade.vn."
        ),
    )
    parser.add_argument(
        "--no-login-wait",
        action="store_true",
        help="Do not pause for manual Owner login.",
    )
    parser.add_argument(
        "--profile-dir",
        default=None,
        help=(
            "Optional persistent Chromium profile directory. "
            "Contains auth cookies locally; never commit it."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help=(
            "Output directory. Default: "
            "runtime/accesstrade_scan_<timestamp>"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(
        args.output_dir
        or f"runtime/accesstrade_scan_{timestamp}"
    )

    allowed_hosts = {
        item.lower()
        for item in (
            args.allowed_hosts
            or DEFAULT_ALLOWED_HOSTS
        )
    }
    profile_dir = (
        Path(args.profile_dir)
        if args.profile_dir
        else None
    )

    if args.max_pages < 1 or args.max_pages > 1000:
        print(
            "--max-pages must be between 1 and 1000.",
            file=sys.stderr,
        )
        return 2

    if (
        args.max_variants_per_route < 1
        or args.max_variants_per_route > 20
    ):
        print(
            "--max-variants-per-route must be between 1 and 20.",
            file=sys.stderr,
        )
        return 2

    asyncio.run(
        map_site(
            start_url=args.start_url,
            output_dir=output_dir,
            max_pages=args.max_pages,
            delay_ms=max(args.delay_ms, 250),
            max_variants_per_route=(
                args.max_variants_per_route
            ),
            allowed_hosts=allowed_hosts,
            login_wait=not args.no_login_wait,
            timeout_ms=args.timeout_ms,
            profile_dir=profile_dir,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
