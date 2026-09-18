#!/usr/bin/env python3
"""Run benchmark prompts against a local OpenAI-compatible chat endpoint.

No external Python packages are required. The runner intentionally defaults to localhost.
It records raw responses and basic timing metrics; scoring is performed separately.
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TASKS = {
    "se_001": ROOT / "tasks/software_engineering/se_001.md",
    "se_002": ROOT / "tasks/software_engineering/se_002.md",
    "se_003": ROOT / "tasks/software_engineering/se_003.md",
    "agent_001": ROOT / "tasks/agentic_execution/agent_001.md",
    "inst_001": ROOT / "tasks/instruction_following/inst_001.md",
    "reason_001": ROOT / "tasks/reasoning/reason_001.md",
    "repo_001": ROOT / "tasks/repository_context/repo_001.md",
    "rel_001": ROOT / "tasks/reliability/rel_001.md",
    "math_001": ROOT / "tasks/math/math_001.md",
    "know_001": ROOT / "tasks/knowledge/know_001.md",
    "vision_001": ROOT / "tasks/vision/vision_001.md",
    "struct_001": ROOT / "tasks/structured_output/struct_001.md",
}

PARAMETERS = {
    "se_001": "software_engineering",
    "se_002": "software_engineering",
    "se_003": "software_engineering",
    "agent_001": "agentic_execution",
    "inst_001": "instruction_following",
    "reason_001": "reasoning",
    "repo_001": "repository_context",
    "rel_001": "reliability_verification",
    "math_001": "math",
    "know_001": "knowledge",
    "vision_001": "vision",
    "struct_001": "structured_output",
}

SUITES = {
    "core": [k for k in TASKS if k != "vision_001"],
    "vision": ["vision_001"],
    "all": list(TASKS),
}


def load_fixture() -> str:
    base = ROOT / "tasks/repository_context/fixture"
    chunks = []
    for path in sorted(p for p in base.rglob("*") if p.is_file()):
        if path.name.endswith(".py") or path.name in {"README.md", "requirements.txt", "BUG.md"}:
            rel = path.relative_to(base).as_posix()
            chunks.append(f"\n===== FILE: {rel} =====\n{path.read_text(encoding='utf-8')}\n")
    return "\n".join(chunks)


def encode_image(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def post_json(url: str, payload: dict, timeout: int) -> dict:
    request = urllib.request.Request(
        url.rstrip("/") + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Run local LLM benchmark tasks")
    ap.add_argument("--endpoint", default="http://127.0.0.1:11434/v1")
    ap.add_argument("--model", required=True)
    ap.add_argument("--suite", choices=sorted(SUITES), default="core")
    ap.add_argument("--task", action="append", dest="tasks")
    ap.add_argument("--output", default="results")
    ap.add_argument("--system", default=str(ROOT / "prompts/master_benchmark.md"))
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--max-output-tokens", type=int, default=8000)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--allow-remote", action="store_true", help="Allow non-localhost endpoint")
    ap.add_argument("--vision", action="store_true", help="Send VISION-001 image as multimodal input")
    args = ap.parse_args()

    if not args.allow_remote and not any(host in args.endpoint for host in ("127.0.0.1", "localhost", "::1")):
        print("Refusing non-local endpoint. Add --allow-remote explicitly.", file=sys.stderr)
        return 2

    selected = args.tasks or SUITES[args.suite]
    unknown = [x for x in selected if x not in TASKS]
    if unknown:
        print(f"Unknown task IDs: {', '.join(unknown)}", file=sys.stderr)
        return 2

    system_prompt = Path(args.system).read_text(encoding="utf-8")
    outdir = Path(args.output) / args.model.replace("/", "__") / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir.mkdir(parents=True, exist_ok=True)

    run_index = []
    for task_id in selected:
        task_text = TASKS[task_id].read_text(encoding="utf-8")
        content = [{"type": "text", "text": task_text}]

        if task_id == "repo_001":
            content.append({"type": "text", "text": "\nRepository fixture contents:\n" + load_fixture()})
        if task_id == "vision_001":
            if not args.vision:
                content[0]["text"] += "\n\nVISION_INPUT_UNSUPPORTED: image was not sent by the runner."
            else:
                image_uri = encode_image(ROOT / "tasks/vision/assets/terminal_error.png")
                content.append({"type": "image_url", "image_url": {"url": image_uri}})

        # Most compatible providers accept the text as a plain string. Multimodal-capable
        # providers accept the list-of-content format used below.
        user_content = content if (task_id == "vision_001" and args.vision) else task_text + ("\n\nRepository fixture contents:\n" + load_fixture() if task_id == "repo_001" else "")
        payload = {
            "model": args.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "temperature": args.temperature,
            "max_tokens": args.max_output_tokens,
        }

        started = time.perf_counter()
        try:
            response = post_json(args.endpoint, payload, args.timeout)
            elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
            choice = response.get("choices", [{}])[0]
            message = choice.get("message", {})
            answer = message.get("content", "")
            usage = response.get("usage", {}) or {}
            record = {
                "task_id": task_id,
                "parameter": PARAMETERS[task_id],
                "model": args.model,
                "elapsed_ms": elapsed_ms,
                "usage": usage,
                "response": answer,
                "raw_response": response,
            }
            status = "ok"
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
            record = {
                "task_id": task_id,
                "parameter": PARAMETERS[task_id],
                "model": args.model,
                "elapsed_ms": elapsed_ms,
                "error": f"{type(exc).__name__}: {exc}",
                "response": "",
            }
            status = "error"

        response_path = outdir / f"{task_id}.json"
        response_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
        run_index.append({"task_id": task_id, "status": status, "file": response_path.as_posix()})
        print(f"[{status}] {task_id}: {response_path}")

    manifest = {
        "benchmark": "Professional Local LLM Benchmark",
        "model": args.model,
        "suite": args.suite,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "settings": {
            "endpoint": args.endpoint,
            "temperature": args.temperature,
            "max_output_tokens": args.max_output_tokens,
            "vision": args.vision,
        },
        "tasks": run_index,
    }
    (outdir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nRun complete: {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
