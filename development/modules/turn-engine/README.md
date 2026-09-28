# turn-engine

## Purpose

Turn sequencing and permitted actions.

## Current status

OPEN — intentionally unimplemented; validation UNTESTED.

## Authority

CANON: repository/module boundaries. GAME_CANON: only supplied [accepted rules](../../../design/game/ACCEPTED_RULES.md). Mathematical/QMO/RenderSpec definitions are SOURCE_IMPORT_REQUIRED, not defined by this README.

## Inputs

Approved timing rules and match state.

## Outputs

Turn/action contracts (planned, not delivered).

## Dependencies

PROVISIONAL coordination dependencies: core-game, qmo-engine. Confirm interfaces before implementation.

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

Phases, priorities, and interruption rules?

## Validation requirements

Legal/illegal ordering and boundary transitions. These are future requirements, not passing tests. Repository validation does not validate this subsystem.


## Cumulative checkpoint 0003

READY/USED and effect concepts do not set turn sequencing. Starting/maximum hand, mulligan, draw rate, phases, refresh, first player and timing windows remain OPEN.

Partial evidence for gates 00 Canon, 01 Design, 03 Rules, 04 State Model and 14 Provenance: [checkpoint 0003](../../../provenance/checkpoints/0003-cumulative-recovery.md), sourced from the user-approved design session on 2026-09-28. Module status is unchanged; no complete gate acceptance, implementation or validation of runtime behavior is inferred.
