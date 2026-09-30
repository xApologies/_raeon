# Implementation boundary: cards

Status: OPEN / UNIMPLEMENTED. This file defines navigation, not gameplay behavior or passing tests.

- [card-system design](../../design/cards/CARD_SYSTEM.md) → [data](../../data/cycles/cycle_01/card-system.json) → [maturity](../../development/modules/card-system/README.md)
- [black-rank design](../../design/cards/black/SYSTEM.md) → [data](../../data/black/design.json) → [maturity](../../development/modules/black-rank/README.md)

No downstream layer may redefine accepted design or mathematical legality.

## Accepted runtime contract — 2026-09-30

Every card instance is a persistent Geometric. Typed Deck/Hand/Graveyard containers own membership/order separately from BOARD attachment roles. Normal Hand capacity is seven. Validate destination before identity-preserving atomic movement. Overflow/multi-card resolution remains OPEN.

Contract only: executable Genesis/game integration remains OPEN. Specification examples are tested independently under tests/gameplay; no production runtime or grammar conformance is claimed.
