# Implementation boundary: cards/generators

Status: OPEN / UNIMPLEMENTED. This file defines navigation, not gameplay behavior or passing tests.

- [field-generators design](../../../design/cards/cycle_01/field_generators/SYSTEM.md) → [data](../../../data/cycles/cycle_01/field_generators/status.json) → [maturity](../../../development/modules/field-generators/README.md)

No downstream layer may redefine accepted design or mathematical legality.

## Accepted runtime contract — 2026-09-30

FG runtime instances reference immutable source definitions and preserve card instance identity through deployment. XY position plus 3D orientation feed both membership and admitted-configuration gates. Query the existing QMO corpus without generating definitions or replacement face/color mathematics.

Contract only: executable Genesis/game integration remains OPEN. Specification examples are tested independently under tests/gameplay; no production runtime or grammar conformance is claimed.
