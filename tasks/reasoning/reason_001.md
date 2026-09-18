# REASON-001 — False Success Diagnostic

A production API returned HTTP 200 and a success payload, but the expected database row was not found immediately afterward.

Architecture:

`Client -> API Service -> Data Service -> Database`

Potential causes:

- false success from Data Service
- transaction rollback
- asynchronous write
- read-after-write inconsistency
- failure after commit but before the response is processed
- hidden error handling
- wrong database/environment
- race condition

## Task
Build an evidence-driven diagnostic path.

For each major hypothesis:

1. State what is known versus unknown.
2. Name the highest-value next evidence to collect.
3. Explain what result would increase or decrease confidence in that hypothesis.
4. Avoid concluding the root cause before evidence is collected.

Finish with a prioritized investigation sequence and explain why the ordering is efficient.
