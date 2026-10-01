# Implementation boundary: qmo

Host implementation: source-locked queries and Pass-3B realization are implemented in this boundary. Whole-module development gates remain OPEN; see the scoped runtime evidence below.

- [qmo-engine design](../../design/topology/manifolds/SYSTEM.md) → [data](../../data/qmo/inventory.json) → [maturity](../../development/modules/qmo-engine/README.md)
- [chirality-fabric design](../../design/topology/field_generators/SYSTEM.md) → [data](../../data/qmo/generators/status.json) → [maturity](../../development/modules/chirality-fabric/README.md)
- [propagation-engine design](../../design/topology/field_generators/SYSTEM.md) → [data](../../data/qmo/generators/status.json) → [maturity](../../development/modules/propagation-engine/README.md)

No downstream layer may redefine accepted design or mathematical legality.

[Pass-3B execution and authority](../../development/modules/core-game/PASS_03B_EXECUTION.md) · [validation receipt](../../development/modules/core-game/PASS_03B_RECEIPT.md).
