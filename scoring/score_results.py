#!/usr/bin/env python3
"""Score evaluator-annotated benchmark result JSON files and aggregate repeats."""
from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

WEIGHTS = {
    "software_engineering": 20,
    "agentic_execution": 20,
    "instruction_following": 15,
    "reasoning": 10,
    "repository_context": 10,
    "reliability_verification": 8,
    "math": 5,
    "knowledge": 5,
    "vision": 4,
    "structured_output": 3,
}


def one_run(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    tasks = data.get("tasks", [])
    by_param = defaultdict(list)
    errors = []
    for task in tasks:
        p = task.get("parameter")
        s = task.get("score")
        if p not in WEIGHTS:
            errors.append(f"Unknown parameter: {p}")
            continue
        if not isinstance(s, (int, float)) or isinstance(s, bool) or not 0 <= s <= 100:
            errors.append(f"Invalid score for {task.get('task_id')}: {s}")
            continue
        by_param[p].append(float(s))

    parameter_scores = {
        p: round(sum(vals) / len(vals), 2) if vals else 0.0
        for p, vals in ((p, by_param.get(p, [])) for p in WEIGHTS)
    }
    final = sum(parameter_scores[p] * WEIGHTS[p] / 100 for p in WEIGHTS)
    return {
        "model": data.get("model", path.stem),
        "source": str(path),
        "parameter_scores": parameter_scores,
        "final_score": round(final, 2),
        "weights": WEIGHTS,
        "validation_errors": errors,
    }


def aggregate(rows: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["model"]].append(row)

    output = []
    for model, runs in grouped.items():
        parameter_mean = {}
        parameter_sd = {}
        for p in WEIGHTS:
            vals = [r["parameter_scores"][p] for r in runs]
            parameter_mean[p] = round(statistics.mean(vals), 2)
            parameter_sd[p] = round(statistics.stdev(vals), 2) if len(vals) > 1 else 0.0
        finals = [r["final_score"] for r in runs]
        output.append({
            "model": model,
            "runs": len(runs),
            "parameter_mean": parameter_mean,
            "parameter_sd": parameter_sd,
            "final_mean": round(statistics.mean(finals), 2),
            "final_sd": round(statistics.stdev(finals), 2) if len(finals) > 1 else 0.0,
            "raw_runs": runs,
        })
    return output


def main() -> int:
    ap = argparse.ArgumentParser(description="Score and aggregate benchmark result JSON files")
    ap.add_argument("results", nargs="+", help="One or more evaluator-annotated result JSON files")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = [one_run(Path(p)) for p in args.results]
    agg = aggregate(rows)

    if args.json:
        print(json.dumps(agg, indent=2))
        return 0

    headers = ["Model"] + list(WEIGHTS) + ["Final"]
    print(" | ".join(headers))
    print(" | ".join(["---"] * len(headers)))
    for row in agg:
        cells = [row["model"]]
        for p in WEIGHTS:
            cells.append(f"{row['parameter_mean'][p]:.2f} ± {row['parameter_sd'][p]:.2f}")
        cells.append(f"{row['final_mean']:.2f} ± {row['final_sd']:.2f}")
        print(" | ".join(cells))
        for run in row["raw_runs"]:
            for err in run["validation_errors"]:
                print(f"WARNING [{run['source']}]: {err}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
