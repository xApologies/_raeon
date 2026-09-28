# board

## Purpose

Board representation and domain placement.

## Current status

OPEN — intentionally unimplemented; validation UNTESTED.

## Authority

CANON: repository/module boundaries. GAME_CANON: only supplied [accepted rules](../../../design/game/ACCEPTED_RULES.md). Mathematical/QMO/RenderSpec definitions are SOURCE_IMPORT_REQUIRED, not defined by this README.

## Inputs

Approved board design and domain state.

## Outputs

Board/placement contracts (planned, not delivered).

## Dependencies

PROVISIONAL coordination dependencies: sandbox-domains, rendering, ui-ux. Confirm interfaces before implementation.

## Development gates

Follow [PIPELINE.md](../../PIPELINE.md). Acceptance requires evidence, revision, reviewer, date; NOT_APPLICABLE needs rationale.

| Gate | Status | Evidence |
| --- | --- | --- |
| 00 Canon | OPEN | None — bootstrap only |
| 01 Design | OPEN | None — bootstrap only |
| 02 Mathematics | OPEN | None — bootstrap only |
| 03 Rules | OPEN | None — bootstrap only |
| 04 State Model | OPEN | None — bootstrap only |
| 05 Interfaces | OPEN | None — bootstrap only |
| 06 Algorithms | OPEN | None — bootstrap only |
| 07 Visualization | OPEN | None — bootstrap only |
| 08 Interaction | OPEN | None — bootstrap only |
| 09 Data & Schemas | OPEN | None — bootstrap only |
| 10 Implementation | OPEN | None — bootstrap only |
| 11 Testing | OPEN | None — bootstrap only |
| 12 Integration | OPEN | None — bootstrap only |
| 13 Performance | OPEN | None — bootstrap only |
| 14 Provenance | OPEN | None — bootstrap only |
| 15 Release | OPEN | None — bootstrap only |

## OPEN questions

Spatial constraints and coordinate model?

## Validation requirements

Placement legality, identity, domain representation. These are future requirements, not passing tests. Repository validation does not validate this subsystem.


## Cumulative checkpoint 0003

Board-scale configuration positions may expand to detailed Sandbox construction view and return to a compact coherent field. Exact presentation contracts remain OPEN.

Partial evidence for gates 00 Canon, 01 Design, 03 Rules, 04 State Model and 14 Provenance: [checkpoint 0003](../../../provenance/checkpoints/0003-cumulative-recovery.md), sourced from the user-approved design session on 2026-09-28. Module status is unchanged; no complete gate acceptance, implementation or validation of runtime behavior is inferred.
