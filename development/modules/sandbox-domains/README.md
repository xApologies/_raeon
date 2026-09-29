# sandbox-domains

## Purpose

Permanent/temporary Sandbox lifecycle.

## Current status

OPEN — intentionally unimplemented; validation UNTESTED. No status advancement in normalization.

## Authority

This dashboard tracks maturity, not game rules. [Current design](../../../design/topology/sandbox/SYSTEM.md) and [mathematics](../../../mathematics/README.md) govern behavior and legality.

## Inputs

[Machine data](../../../data/topology/sandbox.json) encodes upstream decisions; absent source artifacts remain SOURCE_IMPORT_REQUIRED.

## Outputs

[Implementation boundary](../../../game/sandbox/README.md) remains unimplemented.

## Dependencies

PROVISIONAL coordination dependencies: board, field-generators, fusion. Confirm interfaces before implementation.

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

See [current specification](../../../design/topology/sandbox/SYSTEM.md) and [OPEN/source-import index](../../../data/manifests/accepted-state.json). Do not duplicate unresolved rule definitions here.

## Validation requirements

[System test boundary](../../../tests/gameplay/sandbox/README.md) is UNTESTED. Repository validators check architecture and design-data consistency, not subsystem correctness. [Provenance and migration evidence](../../../provenance/checkpoints/0004-repository-normalization.md).

## Continuity evidence

[Final continuity reconciliation](../../../provenance/audits/final-continuity-import.md) adds design/source context. Current maturity and all gate statuses remain unchanged; external source PASS/CLOSED claims are not module completion evidence.


Accepted 2026-09-29 design is recorded in the [full migration manifest](../../../data/manifests/full-migration-2026-09-29.json). This resolves only its named design items; implementation and every development gate remain OPEN.
