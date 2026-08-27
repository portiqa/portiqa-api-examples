"""Dependency-free PORTIQA evaluation example for Python 3.9+."""

from __future__ import annotations

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def main() -> int:
    api_key = os.environ.get("PORTIQA_API_KEY", "").strip()
    if not api_key:
        print("Set PORTIQA_API_KEY before running this example.", file=sys.stderr)
        return 2

    payload = {
        "risk_level": "medium",
        "cash_balance": 5000,
        "positions": [
            {"ticker": "AAPL", "market_value": 25000},
            {"ticker": "MSFT", "market_value": 22000},
            {"ticker": "NVDA", "market_value": 8000},
        ],
    }
    request = Request(
        "https://portiqa.ai/evaluate",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=20) as response:
            body = json.load(response)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        print(f"PORTIQA returned HTTP {error.code}: {detail}", file=sys.stderr)
        return 1
    except (URLError, TimeoutError) as error:
        print(f"Could not reach PORTIQA: {error}", file=sys.stderr)
        return 1
    except json.JSONDecodeError:
        print("PORTIQA returned a non-JSON response.", file=sys.stderr)
        return 1

    if body.get("ok") is not True or not isinstance(body.get("evaluation"), dict):
        print(f"Unexpected response: {json.dumps(body)}", file=sys.stderr)
        return 1

    print(json.dumps(body["evaluation"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
