# Implementation boundary: manifolds

Status: OPEN / UNIMPLEMENTED. This file defines navigation, not gameplay behavior or passing tests.

- [manifold-closure design](../../design/topology/manifolds/SYSTEM.md) → [data](../../data/qmo/manifolds/status.json) → [maturity](../../development/modules/manifold-closure/README.md)
- [fusion design](../../design/topology/fusion/SYSTEM.md) → [data](../../data/qmo/fusion/status.json) → [maturity](../../development/modules/fusion/README.md)
- [emergent-fields design](../../design/topology/emergent_fields/SYSTEM.md) → [data](../../data/qmo/emergent/status.json) → [maturity](../../development/modules/emergent-fields/README.md)

No downstream layer may redefine accepted design or mathematical legality.

## Accepted runtime contract — 2026-09-30

Merge preserves all FG identities and changes two independent spaces to one coupled/derived space. Pairwise emergence leaves supports distinct, consumes zero space slots, may coexist across several admitted pairs and ends on required support loss. Query preserved source relations; runtime pose/admission, merged ceiling/base accounting and split remain OPEN.

Contract only: executable Genesis/game integration remains OPEN. Specification examples are tested independently under tests/gameplay; no production runtime or grammar conformance is claimed.
