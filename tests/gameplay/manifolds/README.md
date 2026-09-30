# Test boundary: gameplay/manifolds

Status: implementation/integration OPEN / UNTESTED. Focused specification examples are executable; they do not test a production game runtime.

- [manifold-closure design](../../../design/topology/manifolds/SYSTEM.md) → [data](../../../data/qmo/manifolds/status.json) → [maturity](../../../development/modules/manifold-closure/README.md)
- [fusion design](../../../design/topology/fusion/SYSTEM.md) → [data](../../../data/qmo/fusion/status.json) → [maturity](../../../development/modules/fusion/README.md)
- [emergent-fields design](../../../design/topology/emergent_fields/SYSTEM.md) → [data](../../../data/qmo/emergent/status.json) → [maturity](../../../development/modules/emergent-fields/README.md)

No downstream layer may redefine accepted design or mathematical legality.


The 2026-09-30 `.test.mjs` files exercise accepted deterministic rule examples using the test-only `rule-model.mjs` under tests/gameplay. Admission premises are explicit; no QMO solver, turn scheduler, Genesis source, runtime integration or balance is claimed. Actual results and commands are recorded in the reconciliation decision.
