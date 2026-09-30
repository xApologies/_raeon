# Implementation boundary: match

Status: OPEN / UNIMPLEMENTED. This file defines navigation, not gameplay behavior or passing tests.

- [turn-engine design](../../design/game/match/SYSTEM.md) → [data](../../data/game/match.json) → [maturity](../../development/modules/turn-engine/README.md)

No downstream layer may redefine accepted design or mathematical legality.

## Accepted runtime contract — 2026-09-30

Enforce accepted ACTIVE friendly Restore/hostile Degrade versus DEFENSE friendly Restore only. Carry READY/USED from ACTIVE into DEFENSE; no refresh on ACTIVE end. Exact refresh boundary, action/reaction scheduler, starting hand/draw/mulligan, victory/loss and targeting windows remain OPEN.

Contract only: executable Genesis/game integration remains OPEN. Specification examples are tested independently under tests/gameplay; no production runtime or grammar conformance is claimed.
