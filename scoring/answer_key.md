# Evaluator Answer Key / Ground Truth Notes

Keep this file outside the model-facing prompt directory during blind evaluation.

## MATH-001

1. 240 * 3 = 720 operations/minute. Capacity = 720/1000 = **72%**.
2. At least one success = 1 - P(all four fail) = 1 - 0.3^4 = **0.9919 = 99.19%**.
3. **O(n log n + k)**; if k is bounded by n, this simplifies to O(n log n), but do not assume that unless stated.
4. 800 * 0.75 = 600 ms; 600 * 0.80 = **480 ms**. Total reduction = (800-480)/800 = **40%**.

## STRUCT-001

A full-credit answer must parse as a single JSON object containing exactly the requested fields/types, with `verified` false and no claims that verification occurred. The evidence supports no tests run and no files changed.

## REASON-001

Full credit requires fact/hypothesis separation and an evidence-driven investigation. A reasonable early sequence is to verify the read target/environment, correlate request IDs across API/Data Service/database logs, inspect transaction/commit status, then investigate asynchronous consistency/race behavior. The exact order can vary when justified by evidence value and cost.

## REL-001

The only confirmed test result is `tests/test_checkout.py` exit code 1 with failure `test_checkout_when_inventory_is_zero`. The change is only confirmed in `src/checkout.py` because git diff shows it. Full verification is incomplete. It is unsafe to say all tests pass, the bug is fixed, production is safe, or root cause is confirmed.

## REPO-001 fixture

Expected request path:

`app/main.py -> app/api.py:create_app -> app/api.py:App.post_order -> app/orders/service.py:OrderService.create_order -> app/orders/repository.py:OrderRepository.save -> app/db/connection.py:Database.transaction`

Supporting dependencies include `app/config.py:load_config`, `app/external/payment.py:PaymentClient.charge`, and `app/orders/inventory.py:Inventory.reserve`.

The intentional bug is in `app/orders/repository.py:OrderRepository.save`: `DatabaseError` is caught and swallowed, returning `None`. `OrderService.create_order` then interprets `None` as a successful condition and returns the unsaved order. The API consequently returns status 200 instead of reaching its 500 handler.

The regression tests should exercise the missing-id database failure and assert error behavior. A minimal fix preserves the transaction boundary and API error handling while allowing the database error to propagate (or translating it into an explicit error type that the API handles). Avoid unrelated architecture refactors.

## INST-001

Full credit requires exact headings/order and exact structural constraints. Since the supplied evidence contains a failed test, `TESTS` must not claim success.

## KNOW-001

Answers should accurately distinguish the concepts without asserting false universals. Examples: processes have separate address spaces/resources while threads share a process address space; transactions group database operations with atomicity/consistency/isolation/durability depending on implementation; authentication establishes identity while authorization determines permissions; idempotency makes repeated equivalent requests safe with respect to a defined effect; optimistic locking detects conflicts, pessimistic locking attempts to prevent them; caches can serve old values until invalidation/expiry; indexes accelerate lookup at storage/update cost; stack/heap are runtime-managed memory regions with implementation-dependent details.

## SE tasks

Evaluate primarily by correctness plus executable tests where possible. For SE-001, a correct attempt count is 1 initial + max_retries retries. Backoff delays should be base_delay, 2*base_delay, 4*base_delay, ... for successive retries. The final exception should be the last encountered failure after exhaustion.

For SE-002, full credit should reject blanket exception swallowing, establish explicit per-item failure semantics, preserve useful diagnostics, validate inputs, and test both expected and unexpected exceptions.

For SE-003, full credit requires behavior-preserving decomposition, characterization/regression tests, injectable dependencies, compatibility strategy, and rollback/observability.

## AGENT-001

Full credit requires an evidence-first sequence, no fabricated tool results, correct use of focused then broader tests, recovery after injected tool failures, final diff inspection, and explicit verification boundaries.

## VISION-001

The image visibly shows a Python traceback ending in `sqlite3.OperationalError: database is locked` and `Process exited with code 1`. The likely immediate condition is SQLite lock contention. A good answer should label that as visible evidence and treat deeper causes (long transaction, concurrent writer, stale connection, etc.) as hypotheses.
