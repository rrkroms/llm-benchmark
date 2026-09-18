# INST-001 — Exact Constraint Test

Return an answer using exactly these five headings, in this order:

1. RESULT
2. RISKS
3. CHANGED_FILES
4. TESTS
5. VERIFICATION

Hard constraints:

- RESULT must contain exactly 2 sentences.
- RISKS must contain exactly 3 bullet points.
- CHANGED_FILES must contain a Markdown table with columns `File` and `Reason`.
- TESTS must contain exactly 4 numbered items.
- VERIFICATION must contain exactly 1 paragraph.
- Do not add any other heading.
- Do not claim tests passed unless evidence is provided.
- Unknown facts must be written as `UNKNOWN`.

Use the following facts only:

- `src/parser.py` was modified.
- `tests/test_parser.py` was run.
- The test command exited with code 1.
- One assertion failed.
- No other test result is known.
