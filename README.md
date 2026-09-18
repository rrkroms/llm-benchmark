# Professional Local LLM Benchmark Pack

A reproducible benchmark for comparing local LLMs on software engineering and agentic workloads.

## 10 scored dimensions

1. Software Engineering / Coding — 20%
2. Agentic Execution / Tool Use — 20%
3. Instruction Following — 15%
4. Reasoning — 10%
5. Repository / Long-Context Understanding — 10%
6. Reliability / Verification — 8%
7. Math — 5%
8. Knowledge — 5%
9. Vision / Multimodal — 4%
10. Structured Output — 3%

Total: 100%

## Design goals

- Same prompt and same task inputs for every model.
- Evidence-based scoring; no self-assigned model scores.
- Prefer executable verification over judging prose.
- Separate capability score from speed/resource metrics.
- Capture failures, tool traces, tests, and verification claims.
- Designed for local models; the included runner defaults to localhost OpenAI-compatible endpoints.

## Quick start

```bash
python runner/run_benchmark.py --endpoint http://127.0.0.1:11434/v1 --model YOUR_MODEL --suite core
```

For Ollama, the OpenAI-compatible API is typically exposed at `http://127.0.0.1:11434/v1`.

If you already have responses, score them without rerunning the model:

```bash
python scoring/score_results.py results/model.json
```

## Important benchmark rule

Use the same:

- system prompt
- benchmark prompt
- task files
- repository fixture
- images
- tool definitions
- maximum output tokens
- temperature / sampling settings
- timeout

Do not mix models' best runs with one another. For a fair comparison, run the full suite at least 3 times when sampling is non-deterministic and report mean plus standard deviation.

## Files

- `prompts/master_benchmark.md` — complete evaluator instructions.
- `benchmark.yaml` — suite, weights, limits and scoring configuration.
- `tasks/` — individual benchmark tasks.
- `schemas/` — result and tool-trace schemas.
- `scoring/rubric.md` — detailed 0–100 scoring rubric.
- `scoring/score_results.py` — deterministic weighted scorer.
- `runner/run_benchmark.py` — local OpenAI-compatible execution runner.
- `examples/` — example result and tool trace formats.
- `docs/protocol.md` — reproducibility protocol.

## Supplementary metrics (not part of the 100-point capability score)

Record these separately:

- time to first token
- total wall-clock time
- input tokens
- output tokens
- tokens/second
- peak VRAM/RAM if available
- context length used
- number of tool calls
- failed tool calls
- retries

These metrics should not silently change the capability score.
