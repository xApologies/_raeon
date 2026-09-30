# Implementation boundary: board

Status: OPEN / UNIMPLEMENTED. This file defines navigation, not gameplay behavior or passing tests.

- [board design](../../design/game/board/SYSTEM.md) → [data](../../data/board/presentation.json) → [maturity](../../development/modules/board/README.md)

No downstream layer may redefine accepted design or mathematical legality.

## Accepted runtime contract — 2026-09-30

BOARD is a State Geometric with five typed child attachments; ports, containers and card identities are distinct. Stage atomic, identity/history-preserving successor-State changes through Nexus. Enforce card-only zones, Hand 7 and at most nine active Configuration Spaces (six additional). Preserve source membership on failed admission. Use existing Rainbow Road transport; renderer/host never owns State.

Contract only: executable Genesis/game integration remains OPEN. Specification examples are tested independently under tests/gameplay; no production runtime or grammar conformance is claimed.
