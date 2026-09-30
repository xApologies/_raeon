# state implementation boundary

OPEN / UNIMPLEMENTED. Upstream: [match design](../../design/game/match/SYSTEM.md), [data](../../data/game/match.json), [mathematical authority](../../mathematics/README.md). [Tests](../../tests/integration/README.md) will verify implementation when it exists.

## Accepted runtime contract — 2026-09-30

Admitted card and board changes preserve instance identity/history and commit atomically through Nexus. Card movement changes relationships, never recreates identity. State is authoritative inside Genesis Horizon; host/Python/renderer are projections or translation boundaries. Exact field-destruction ordering remains OPEN.

Contract only: executable Genesis/game integration remains OPEN. Specification examples are tested independently under tests/gameplay; no production runtime or grammar conformance is claimed.
