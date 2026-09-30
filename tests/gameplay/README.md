# Test boundary: gameplay

Status: implementation/integration OPEN / UNTESTED. Focused specification examples are executable; they do not test a production game runtime.

- [turn-engine design](../../design/game/match/SYSTEM.md) → [data](../../data/game/match.json) → [maturity](../../development/modules/turn-engine/README.md)
- [ai design](../../design/ai/README.md) → [data](../../data/ai/direction.json) → [maturity](../../development/modules/ai/README.md)
- [ui-ux design](../../design/ui_ux/SYSTEM.md) → [data](../../data/board/presentation.json) → [maturity](../../development/modules/ui-ux/README.md)

No downstream layer may redefine accepted design or mathematical legality.


The 2026-09-30 `.test.mjs` files exercise accepted deterministic rule examples using the test-only `rule-model.mjs` under tests/gameplay. Admission premises are explicit; no QMO solver, turn scheduler, Genesis source, runtime integration or balance is claimed. Actual results and commands are recorded in the reconciliation decision.
