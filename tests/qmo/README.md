# Test boundary: qmo

Status: OPEN / UNTESTED. This file defines navigation, not gameplay behavior or passing tests.

- [qmo-engine design](../../design/topology/manifolds/SYSTEM.md) → [data](../../data/qmo/inventory.json) → [maturity](../../development/modules/qmo-engine/README.md)
- [chirality-fabric design](../../design/topology/field_generators/SYSTEM.md) → [data](../../data/qmo/generators/status.json) → [maturity](../../development/modules/chirality-fabric/README.md)
- [propagation-engine design](../../design/topology/field_generators/SYSTEM.md) → [data](../../data/qmo/generators/status.json) → [maturity](../../development/modules/propagation-engine/README.md)

No downstream layer may redefine accepted design or mathematical legality.


[Cycle-1 source integrity](../../tools/validators/validate-cycle1-import.mjs) and [import regressions](../regression/cycle1-import.test.mjs) now verify original catalog data. These do not claim game-system implementation or theoretical proof.
