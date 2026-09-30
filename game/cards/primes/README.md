# Implementation boundary: cards/primes

Status: OPEN / UNIMPLEMENTED. This file defines navigation, not gameplay behavior or passing tests.

- [prime-fields design](../../../design/cards/cycle_01/primes/SYSTEM.md) → [data](../../../data/cycles/cycle_01/primes/status.json) → [maturity](../../../development/modules/prime-fields/README.md)

No downstream layer may redefine accepted design or mathematical legality.

## Accepted runtime contract — 2026-09-30

Normal ordinary Prime starts H=H_max,C=0. Classify healthy uncharged, healthy charged, damaged non-operational and INACTIVE. Only H=H_max with C>0 can operate under family/window/target admission. Spend partial C; repeated operations are charge-limited, not tap-limited. Preserve H-before-C Restore, C-before-H Degrade, fixed identity/slot and explicit White reactivation. Overflow remains OPEN.

Contract only: executable Genesis/game integration remains OPEN. Specification examples are tested independently under tests/gameplay; no production runtime or grammar conformance is claimed.
