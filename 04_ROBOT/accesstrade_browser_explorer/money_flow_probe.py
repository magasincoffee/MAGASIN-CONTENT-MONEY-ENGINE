#!/usr/bin/env python3
"""
ACCESSTRADE Money-Flow Schema Probe V1

Purpose:
Observe the Owner's normal ACCESSTRADE browser actions and record only
structural request/response schemas needed to build precise read/action
adapters later.

Important:
- The Owner performs all clicks/forms manually.
- This probe does not click, submit, create links, register campaigns,
  mutate profile/payment data, or send requests itself.
- It never records cookies, Authorization headers, OTPs, passwords, raw
  request bodies, raw response bodies, or parameter values.
- It records only endpoint paths, safe parameter NAMES, and JSON SHAPES.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlsplit, urlunsplit

from playwright.async_api import Request, Response, async_playwright


SENSITIVE_KEYS = {
    "authorization",
    "token",
    "access_token",
    "refresh_token",
    "secret",
    "password",
    "passwd",
    "otp",
    "mfa",
    "code",
    "cookie",
    "session",
    "sid",
    "jwt",
    "api_key",
    "apikey",
    "signature",
    "sig",
    "bank",
    "account_number",
    "tax_id",
    "identity",
    "id_number",
    "phone",
    "email",
}

SENSITIVE_PATH_KEYWORDS = {
    "identity",
    "profile",
    "e-contract",
    "payment",
    "payout",
    "withdraw",
    "bank",
    "tax",
    "kyc",
}

MAX_SCHEMA_DEPTH = 4
MAX_KEYS_PER_OBJECT = 80
MAX_ARRAY_ITEMS_TO_INSPECT = 2


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_accesstrade_host(url: str) -> bool:
    host = (urlsplit(url).hostname or "").lower()
    return host == "accesstrade.vn" or host.endswith(".accesstrade.vn")


def endpoint_url(raw_url: str) -> str:
    parts = urlsplit(raw_url)
    return urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), parts.path, "", "")
    )


def sanitize_page_url(raw_url: str) -> str:
    parts = urlsplit(raw_url)
    return urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), parts.path, "", "")
    )


def is_sensitive_path(raw_url: str) -> bool:
    path = urlsplit(raw_url).path.lower()
    return any(keyword in path for keyword in SENSITIVE_PATH_KEYWORDS)


def safe_query_keys(raw_url: str) -> list[str]:
    parts = urlsplit(raw_url)
    keys: list[str] = []
    for key, _value in parse_qsl(parts.query, keep_blank_values=True):
        lower = key.lower()
        if any(sensitive in lower for sensitive in SENSITIVE_KEYS):
            continue
        if key not in keys:
            keys.append(key)
    return sorted(keys)[:MAX_KEYS_PER_OBJECT]


def scalar_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    return type(value).__name__


def schema_shape(value: Any, depth: int = 0) -> Any:
    if depth >= MAX_SCHEMA_DEPTH:
        if isinstance(value, dict):
            return {"type": "object", "truncated": True}
        if isinstance(value, list):
            return {"type": "array", "truncated": True}
        return {"type": scalar_type(value)}

    if isinstance(value, dict):
        properties: dict[str, Any] = {}
        for key in sorted(value.keys())[:MAX_KEYS_PER_OBJECT]:
            lower = str(key).lower()
            if any(sensitive in lower for sensitive in SENSITIVE_KEYS):
                properties[str(key)] = {
                    "type": "REDACTED_SENSITIVE_FIELD"
                }
                continue
            properties[str(key)] = schema_shape(
                value[key],
                depth + 1,
            )
        return {
            "type": "object",
            "keys": properties,
            "key_count": len(value),
        }

    if isinstance(value, list):
        sample = [
            schema_shape(item, depth + 1)
            for item in value[:MAX_ARRAY_ITEMS_TO_INSPECT]
        ]
        return {
            "type": "array",
            "sample_item_shapes": sample,
            "observed_length": len(value),
        }

    return {"type": scalar_type(value)}


def parse_request_body_schema(request: Request) -> dict[str, Any] | None:
    if request.method.upper() in {"GET", "HEAD", "OPTIONS"}:
        return None

    try:
        raw = request.post_data
    except Exception:
        raw = None

    if not raw:
        return {"body_present": False}

    try:
        parsed = json.loads(raw)
        return {
            "body_present": True,
            "encoding": "json",
            "shape": schema_shape(parsed),
        }
    except Exception:
        pass

    try:
        pairs = parse_qsl(raw, keep_blank_values=True)
        if pairs:
            keys = []
            for key, _value in pairs:
                lower = key.lower()
                if any(sensitive in lower for sensitive in SENSITIVE_KEYS):
                    continue
                if key not in keys:
                    keys.append(key)
            return {
                "body_present": True,
                "encoding": "form_urlencoded_or_querylike",
                "keys": sorted(keys)[:MAX_KEYS_PER_OBJECT],
            }
    except Exception:
        pass

    return {
        "body_present": True,
        "encoding": "opaque",
        "raw_body_recorded": False,
    }


async def response_schema(
    response: Response,
) -> dict[str, Any] | None:
    request = response.request

    if request.resource_type not in {"xhr", "fetch"}:
        return None
    if is_sensitive_path(request.url):
        return {
            "skipped": True,
            "reason": "sensitive_path",
        }

    try:
        content_type = await response.header_value("content-type")
    except Exception:
        content_type = None

    if not content_type or "json" not in content_type.lower():
        return {
            "content_type": content_type or "unknown",
            "json_shape": None,
        }

    try:
        payload = await response.json()
    except Exception:
        return {
            "content_type": content_type,
            "json_shape": "UNAVAILABLE",
        }

    return {
        "content_type": content_type,
        "json_shape": schema_shape(payload),
    }


async def run_probe(
    cdp_url: str,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    events_path = output_dir / "money_flow_schema.jsonl"
    summary_path = output_dir / "summary.md"

    pending_tasks: set[asyncio.Task[Any]] = set()
    seen: set[str] = set()
    event_count = 0

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp_url)

        if not browser.contexts:
            raise RuntimeError(
                "Connected Chrome has no browser context."
            )

        context = browser.contexts[0]

        async def handle_response(response: Response) -> None:
            nonlocal event_count

            request = response.request
            if not is_accesstrade_host(request.url):
                return
            if request.resource_type not in {"xhr", "fetch"}:
                return

            endpoint = endpoint_url(request.url)
            request_body = parse_request_body_schema(request)

            page_url = ""
            try:
                frame = request.frame
                if frame and frame.page:
                    page_url = sanitize_page_url(frame.page.url)
            except Exception:
                page_url = ""

            record = {
                "observed_at": now_iso(),
                "method": request.method,
                "endpoint": endpoint,
                "status": response.status,
                "resource_type": request.resource_type,
                "page_url": page_url,
                "query_keys": safe_query_keys(request.url),
                "request_body_schema": request_body,
                "response_schema": await response_schema(response),
            }

            fingerprint = json.dumps(
                {
                    "method": record["method"],
                    "endpoint": record["endpoint"],
                    "query_keys": record["query_keys"],
                    "request_body_schema": record["request_body_schema"],
                    "response_schema": record["response_schema"],
                },
                ensure_ascii=False,
                sort_keys=True,
            )

            if fingerprint in seen:
                return
            seen.add(fingerprint)

            with events_path.open("a", encoding="utf-8") as fh:
                fh.write(
                    json.dumps(
                        record,
                        ensure_ascii=False,
                    )
                    + "\n"
                )

            event_count += 1
            print(
                f"[OBSERVED] {record['method']} "
                f"{record['endpoint']} -> {record['status']}"
            )

        def on_response(response: Response) -> None:
            task = asyncio.create_task(handle_response(response))
            pending_tasks.add(task)
            task.add_done_callback(
                lambda done: pending_tasks.discard(done)
            )

        for page in context.pages:
            page.on("response", on_response)

        context.on(
            "page",
            lambda page: page.on("response", on_response),
        )

        print("[ATTACHED] ACCESSTRADE Money-Flow Schema Probe")
        print("")
        print("Perform the normal Owner actions you want the Robot to learn.")
        print("Recommended demonstration:")
        print("1) Open Shopee Smartlink campaign.")
        print("2) Open the Create Link / Product Link tool.")
        print(
            "3) If you choose to, manually create ONE ordinary "
            "affiliate link."
        )
        print("4) Open Click - Traffic report.")
        print("5) Open Order / Conversion report.")
        print("6) Open Campaign report.")
        print("")
        print(
            "The probe records endpoint/query/body/response SHAPES only. "
            "It does not record values, cookies or auth headers."
        )
        print("")

        await asyncio.to_thread(
            input,
            "Press ENTER here when the manual demonstration is finished: ",
        )

        await asyncio.sleep(1.5)
        if pending_tasks:
            await asyncio.gather(
                *list(pending_tasks),
                return_exceptions=True,
            )

        summary = [
            "# ACCESSTRADE Money-Flow Schema Probe — Summary",
            "",
            f"- Generated: {now_iso()}",
            f"- Unique API interaction shapes: **{event_count}**",
            "",
            "## Safety",
            "",
            "- Owner performed all browser actions manually.",
            "- Probe did not click, submit, create links or mutate account state.",
            "- No raw request/response body values are stored.",
            "- No cookies, auth headers, passwords, OTPs or tokens are stored.",
            "- Sensitive payment/profile/identity response schemas are skipped.",
            "",
            "## Output",
            "",
            "- money_flow_schema.jsonl",
            "",
            "Use the observed schemas to implement narrow adapters only after Brain review.",
        ]
        summary_path.write_text(
            "\n".join(summary) + "\n",
            encoding="utf-8",
        )

        print("")
        print("[DONE]")
        print(f"Unique API shapes: {event_count}")
        print(f"Output: {output_dir.resolve()}")
        print("[INFO] Chrome remains open.")

        # Do not close the Owner's attached Chrome.


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Observe sanitized ACCESSTRADE API schemas while "
            "the Owner performs normal browser actions."
        )
    )
    parser.add_argument(
        "--cdp-url",
        default="http://127.0.0.1:9222",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(
        args.output_dir
        or f"runtime/accesstrade_money_probe_{timestamp}"
    )
    asyncio.run(
        run_probe(
            cdp_url=args.cdp_url,
            output_dir=output_dir,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
