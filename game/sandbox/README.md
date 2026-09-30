# Implementation boundary: sandbox

Status: OPEN / UNIMPLEMENTED. This file defines navigation, not gameplay behavior or passing tests.

- [sandbox-domains design](../../design/topology/sandbox/SYSTEM.md) → [data](../../data/topology/sandbox.json) → [maturity](../../development/modules/sandbox-domains/README.md)

No downstream layer may redefine accepted design or mathematical legality.

## Accepted runtime contract — 2026-09-30

Configuration Space is live State workspace, outside the QMO corpus. Enforce nine active/six additional limits; resolve only when source membership and admitted XY/3D pose both pass. Current field color is mutable independently of topology. Zero-color destruction routes supporting FG identities to Graveyard; transaction ordering remains OPEN. READY generation uses current color once, marks USED and retains topology.

Contract only: executable Genesis/game integration remains OPEN. Specification examples are tested independently under tests/gameplay; no production runtime or grammar conformance is claimed.
