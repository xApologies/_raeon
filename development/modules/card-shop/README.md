# card-shop

## Purpose

Shop product and transaction design.

## Current status

OPEN — intentionally unimplemented; validation UNTESTED.

## Authority

CANON: repository/module boundaries. GAME_CANON: only supplied [accepted rules](../../../design/game/ACCEPTED_RULES.md). Mathematical/QMO/RenderSpec definitions are SOURCE_IMPORT_REQUIRED, not defined by this README.

## Inputs

Approved economy/collection policy.

## Outputs

Shop contracts and collection changes (planned, not delivered).

## Dependencies

PROVISIONAL coordination dependencies: collection, persistence. Confirm interfaces before implementation.

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

Currencies, offerings, crafting costs, transactions?

## Validation requirements

Atomicity and approved economy rules. These are future requirements, not passing tests. Repository validation does not validate this subsystem.


## Design checkpoint 0002

Current direction does not require purchased gameplay credits and excludes player-to-player credit wagering. Game-generated PvP rewards are possible but amounts, recipes, pricing and transaction details remain OPEN. See [current rules](../../../design/game/ACCEPTED_RULES.md), [Utility design](../../../design/cards/cycle_01/UTILITIES.md), and [checkpoint](../../../provenance/checkpoints/0002-game-design.md). This adds design evidence only; subsystem gates are not accepted by these notes.


## Cumulative checkpoint 0003

Play-earned credits may feed card-shop/pack opening. No gameplay-credit bundles, wagering or subscription-dependent gameplay. Prices, pack sizes/probabilities and costs remain OPEN.

Partial evidence for gates 00 Canon, 01 Design, 03 Rules, 04 State Model and 14 Provenance: [checkpoint 0003](../../../provenance/checkpoints/0003-cumulative-recovery.md), sourced from the user-approved design session on 2026-09-28. Module status is unchanged; no complete gate acceptance, implementation or validation of runtime behavior is inferred.
