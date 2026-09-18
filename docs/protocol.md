# Benchmark Protocol

## 1. Hardware and runtime

Record:

- CPU
- GPU(s)
- VRAM
- system RAM
- operating system
- inference backend and version
- quantization
- model file format
- context window configured

Run each model with the same backend class and equivalent settings when possible.

## 2. Sampling

Preferred default:

- temperature: 0
- top_p: 1
- seed: 42 when supported

If a backend ignores a setting, record that fact. Do not silently compare a deterministic model run with a highly stochastic model run.

## 3. Repetitions

Use 3 repetitions for non-deterministic models. For deterministic inference, one run can be sufficient for capability measurement, but 3 runs are still useful for latency/resource variance.

Report mean and standard deviation across runs. Do not select the best run for the final score.

## 4. Inputs

Every model receives identical benchmark task content. For repository tasks, use the exact same fixture bytes. For vision tasks, use the exact same image.

## 5. Tool-use tasks

For true agent evaluation, execute against the same tool implementation and failure-injection rules. Capture the complete chronological tool trace including arguments and results.

A text-only answer describing intended tool use is not equivalent to actual tool execution and should be labeled accordingly.

## 6. Scoring separation

Capability score is separate from speed/resource metrics.

Capability score:

`sum(parameter_score * weight / 100)`

Latency, throughput, VRAM, RAM and tokens are reported as supplemental measurements.

## 7. Human scoring

Blind the evaluator to model identity where practical. Score evidence rather than brand/model reputation. Use the same rubric for every model.

## 8. Reproducibility

Save:

- exact benchmark version
- model identifier and quantization
- runtime versions
- settings
- raw responses
- tool traces
- test outputs
- final evaluator scores

Never replace raw responses with summaries only.
