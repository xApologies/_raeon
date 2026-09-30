# Test boundary: gameplay/primes

Status: implementation/integration OPEN / UNTESTED. Focused specification examples are executable; they do not test a production game runtime.

- [prime-fields design](../../../design/cards/cycle_01/primes/SYSTEM.md) → [data](../../../data/cycles/cycle_01/primes/status.json) → [maturity](../../../development/modules/prime-fields/README.md)
- [black-rank design](../../../design/cards/black/SYSTEM.md) → [data](../../../data/black/design.json) → [maturity](../../../development/modules/black-rank/README.md)

No downstream layer may redefine accepted design or mathematical legality.


The 2026-09-30 `.test.mjs` files exercise accepted deterministic rule examples using the test-only `rule-model.mjs` under tests/gameplay. Admission premises are explicit; no QMO solver, turn scheduler, Genesis source, runtime integration or balance is claimed. Actual results and commands are recorded in the reconciliation decision.
