# Bug Report

## Symptom
An order request can receive a successful response even when the database write failed.

## Reproduction hint
Submit an order without an `id`. The repository raises a `DatabaseError`, but the API may still return HTTP 200.

## Required outcome
Database failures must not be converted into successful order responses. Preserve the error path so the API can return an error response.

## Constraints
- Keep the transaction boundary in the database layer.
- Do not remove API error handling.
- Avoid unrelated refactors.
- Add regression coverage.
