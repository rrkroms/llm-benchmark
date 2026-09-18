#!/usr/bin/env python3
"""Validate the STRUCT-001 response mechanically."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = {
    "model_task_status": str,
    "confidence": (int, float),
    "verified": bool,
    "tests_run": list,
    "tests_passed": list,
    "tests_failed": list,
    "files_changed": list,
    "known_limitations": list,
    "claims_requiring_verification": list,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("response")
    args = ap.parse_args()
    raw = Path(args.response).read_text(encoding="utf-8").strip()
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(json.dumps({"valid": False, "score": 0, "reason": f"invalid JSON: {exc}"}, indent=2))
        return 1

    problems = []
    if not isinstance(obj, dict):
        problems.append("top level is not an object")
    else:
        if set(obj) != set(REQUIRED):
            problems.append("keys do not exactly match required schema")
        for key, typ in REQUIRED.items():
            if key in obj and not isinstance(obj[key], typ):
                problems.append(f"wrong type for {key}")
        c = obj.get("confidence")
        if isinstance(c, (int, float)) and not isinstance(c, bool) and not 0 <= c <= 1:
            problems.append("confidence outside 0..1")
        if obj.get("verified") is not False:
            problems.append("verified must be false for supplied evidence")
        if obj.get("tests_run") != []:
            problems.append("tests_run must be []")
        if obj.get("tests_passed") != []:
            problems.append("tests_passed must be []")
        if obj.get("files_changed") != []:
            problems.append("files_changed must be []")

    valid = not problems
    print(json.dumps({"valid": valid, "score": 100 if valid else 0, "problems": problems}, indent=2))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
