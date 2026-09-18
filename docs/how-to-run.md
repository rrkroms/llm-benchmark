# How to Run the Benchmark

## A. Run a local OpenAI-compatible model

Start your local inference server, then:

```bash
python runner/run_benchmark.py --endpoint http://127.0.0.1:11434/v1 --model YOUR_MODEL --suite all --vision
```

The runner writes raw per-task responses under:

`results/<model>/<timestamp>/`

## B. Use a non-vision model

Run `--suite core` or omit `--vision`. VISION-001 will be marked unsupported rather than fabricated.

## C. Evaluate a model

Copy `scoring/evaluator_template.json` and fill in one 0–100 score per task using `scoring/rubric.md` and `scoring/answer_key.md`.

Preserve the raw model response files and attach evidence paths in the evaluator JSON.

## D. Repeat runs

For stochastic models, produce 3 evaluator JSON files with different `run` values. Do not pick the highest run.

## E. Aggregate

```bash
python scoring/score_results.py run1.json run2.json run3.json
```

The scorer outputs mean and standard deviation per parameter and for the final weighted score.

## F. Structured-output automatic validation

```bash
python scoring/validate_structured_json.py path/to/struct_001_response.txt
```

This is a mechanical validator for STRUCT-001 and can be combined with human review for the other tasks.
