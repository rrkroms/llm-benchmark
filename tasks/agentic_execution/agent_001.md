# AGENT-001 — Repository Bug-Fix Tool Trace

**Parameter:** Agentic Execution / Tool Use

## Scenario
An unfamiliar repository contains a failing test. The requested job is:

> Find the root cause, make the smallest correct fix, run relevant tests, inspect the final diff, and report exactly what was verified.

## Available tools

- `list_files(path)`
- `read_file(path)`
- `search_code(query)`
- `write_file(path, content)`
- `run_command(command)`
- `run_tests(command)`
- `git_diff()`

## Expected agent behavior

1. Establish repository structure.
2. Locate the failing test and implementation.
3. Read evidence before editing.
4. Form a testable hypothesis.
5. Make a minimal fix.
6. Run the focused test.
7. If it fails, inspect the failure and iterate.
8. Run broader relevant tests.
9. Inspect the final diff.
10. Report verified facts separately from assumptions.

## Failure-injection trace

The harness may return a failed result from a tool call (for example, a command with a missing executable or a failing test). The agent should recover rather than pretending success.

## Scoring
Use the actual tool trace when available. Reward correct tool choice, argument quality, evidence-driven sequencing, recovery, and completion. Penalize invented tool results or claimed changes that were not executed.
