# Scoring Rubric

All parameter and task scores are 0–100. Score evidence, not confidence or writing style.

## 1. Software Engineering / Coding — 20%

- 90–100: Correct, production-quality implementation; appropriate edge cases; tests; minimal unrelated change; strong explanation.
- 75–89: Correct implementation with minor omissions or non-critical quality issues.
- 50–74: Partially correct; important edge cases, tests, or design details missing.
- 25–49: Significant defects; only part of the task works.
- 0–24: Fundamentally incorrect, unusable, or fabricated execution.

When executable tests exist, test evidence outranks prose claims.

## 2. Agentic Execution / Tool Use — 20%

Assess tool choice, argument correctness, sequence, efficiency, recovery from failures, use of returned evidence, and completion.

100 requires a complete, coherent trace with correct recovery and verification.

## 3. Instruction Following — 15%

Count hard-constraint violations. Exact formatting requirements matter. Ignoring a requirement is a substantive error even if the content is otherwise good.

## 4. Reasoning — 10%

Score the correctness of the conclusion, evidence chain, treatment of alternatives, and avoidance of unsupported leaps.

## 5. Repository / Long-Context Understanding — 10%

Score cross-file consistency, dependency tracing, architecture understanding, precise symbol references, and avoidance of filename-only assumptions.

## 6. Reliability / Verification — 8%

Reward evidence-based verification, regression checks, honest uncertainty, and correct detection of failed attempts. Penalize hallucinated success claims heavily.

## 7. Math — 5%

Score final numerical correctness and reasoning. Do not give full credit for a correct answer produced by invalid reasoning when the task explicitly requests reasoning.

## 8. Knowledge — 5%

Score technical accuracy and appropriate qualification of context-dependent claims.

## 9. Vision / Multimodal — 4%

Score accurate extraction, interpretation, anomaly detection, and clear separation of visible facts from inference. Missing vision input is not a model failure when the benchmark environment did not provide an image.

## 10. Structured Output — 3%

Validate the output mechanically. Invalid JSON, missing required keys, wrong types, or extra non-JSON text should materially reduce the score.

## Recommended evidence hierarchy

1. Executed tests / validators
2. Tool trace and actual tool results
3. File diffs
4. Structured output validation
5. Human review of reasoning and explanation

## Prohibited scoring shortcuts

Do not score based on model reputation, benchmark leaderboard reputation, prose confidence, or which answer sounds more sophisticated.
