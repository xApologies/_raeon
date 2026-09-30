# Test boundary: gameplay/sandbox

Status: implementation/integration OPEN / UNTESTED. Focused specification examples are executable; they do not test a production game runtime.

- [board design](../../../design/game/board/SYSTEM.md) → [data](../../../data/board/presentation.json) → [maturity](../../../development/modules/board/README.md)
- [sandbox-domains design](../../../design/topology/sandbox/SYSTEM.md) → [data](../../../data/topology/sandbox.json) → [maturity](../../../development/modules/sandbox-domains/README.md)

No downstream layer may redefine accepted design or mathematical legality.


The 2026-09-30 `.test.mjs` files exercise accepted deterministic rule examples using the test-only `rule-model.mjs` under tests/gameplay. Admission premises are explicit; no QMO solver, turn scheduler, Genesis source, runtime integration or balance is claimed. Actual results and commands are recorded in the reconciliation decision.
