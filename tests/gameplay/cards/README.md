# Test boundary: gameplay/cards

Status: implementation/integration OPEN / UNTESTED. Focused specification examples are executable; they do not test a production game runtime.

- [card-system design](../../../design/cards/CARD_SYSTEM.md) → [data](../../../data/cycles/cycle_01/card-system.json) → [maturity](../../../development/modules/card-system/README.md)
- [field-generators design](../../../design/cards/cycle_01/field_generators/SYSTEM.md) → [data](../../../data/cycles/cycle_01/field_generators/status.json) → [maturity](../../../development/modules/field-generators/README.md)
- [deck-construction design](../../../design/cards/CARD_SYSTEM.md) → [data](../../../data/cycles/cycle_01/card-system.json) → [maturity](../../../development/modules/deck-construction/README.md)

No downstream layer may redefine accepted design or mathematical legality.


The 2026-09-30 `.test.mjs` files exercise accepted deterministic rule examples using the test-only `rule-model.mjs` under tests/gameplay. Admission premises are explicit; no QMO solver, turn scheduler, Genesis source, runtime integration or balance is claimed. Actual results and commands are recorded in the reconciliation decision.
