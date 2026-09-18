# STRUCT-001 — Strict JSON

Return exactly one JSON object with these fields:

```text
model_task_status: string
confidence: number from 0 to 1
verified: boolean
tests_run: array of strings
tests_passed: array of strings
tests_failed: array of strings
files_changed: array of strings
known_limitations: array of strings
claims_requiring_verification: array of strings
```

Use this evidence only:

- No test was executed.
- No file was changed.
- Repository contents were not provided.
- You may not claim verification.

Output JSON only. No Markdown fences. No explanation outside the JSON object.
