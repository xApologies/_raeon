# deck-construction

## Purpose

Deck composition and legality.

## Current status

OPEN — intentionally unimplemented; validation UNTESTED. No status advancement in normalization.

## Authority

This dashboard tracks maturity, not game rules. [Current design](../../../design/cards/CARD_SYSTEM.md) and [mathematics](../../../mathematics/README.md) govern behavior and legality.

## Inputs

[Machine data](../../../data/cycles/cycle_01/card-system.json) encodes upstream decisions; absent source artifacts remain SOURCE_IMPORT_REQUIRED.

## Outputs

[Implementation boundary](../../../game/deck/README.md) remains unimplemented.

## Dependencies

PROVISIONAL coordination dependencies: card-system, prime-fields, utilities, black-rank. Confirm interfaces before implementation.

## Development gates

[Pipeline](../../PIPELINE.md). Gate acceptance requires evidence, revision, reviewer/date, and justified NOT_APPLICABLE entries. Partial design evidence from [0002](../../../provenance/checkpoints/0002-game-design.md), [0003](../../../provenance/checkpoints/0003-cumulative-recovery.md) and [0004](../../../provenance/checkpoints/0004-repository-normalization.md) does not certify a whole gate.

| Gate | Status | Evidence |
| --- | --- | --- |
| 00 Canon | OPEN | Partial design/source navigation only; acceptance pending |
| 01 Design | OPEN | Partial design/source navigation only; acceptance pending |
| 02 Mathematics | OPEN | Partial design/source navigation only; acceptance pending |
| 03 Rules | OPEN | Partial design/source navigation only; acceptance pending |
| 04 State Model | OPEN | Partial design/source navigation only; acceptance pending |
| 05 Interfaces | OPEN | Partial design/source navigation only; acceptance pending |
| 06 Algorithms | OPEN | Partial design/source navigation only; acceptance pending |
| 07 Visualization | OPEN | Partial design/source navigation only; acceptance pending |
| 08 Interaction | OPEN | Partial design/source navigation only; acceptance pending |
| 09 Data & Schemas | OPEN | Partial design/source navigation only; acceptance pending |
| 10 Implementation | OPEN | Partial design/source navigation only; acceptance pending |
| 11 Testing | OPEN | Partial design/source navigation only; acceptance pending |
| 12 Integration | OPEN | Partial design/source navigation only; acceptance pending |
| 13 Performance | OPEN | Partial design/source navigation only; acceptance pending |
| 14 Provenance | OPEN | Partial design/source navigation only; acceptance pending |
| 15 Release | OPEN | Partial design/source navigation only; acceptance pending |

## OPEN questions

See [current specification](../../../design/cards/CARD_SYSTEM.md) and [OPEN/source-import index](../../../data/manifests/accepted-state.json). Do not duplicate unresolved rule definitions here.

## Validation requirements

[System test boundary](../../../tests/gameplay/cards/README.md) is UNTESTED. Repository validators check architecture and design-data consistency, not subsystem correctness. [Provenance and migration evidence](../../../provenance/checkpoints/0004-repository-normalization.md).
