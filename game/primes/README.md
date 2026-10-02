# Relocated — Prime runtime values

Current card specification: [README.md](../cards/primes/README.md). This compatibility entry preserves historical links.

Current authority is [the charge-node contract](../../provenance/imports/raeon-pass-05/handoff/PRIME_CHARGE_NODE_CONTRACT.md), implemented in `nodes.py` under the compiled match-tempo admissions.

For immutable native magnitude r, intrinsic health H remains in 0..r. Canonical integer N and R store charge Q=N*r+R, with N>=0 and 0<=R<r. There is no game-rule node cap and no list allocation proportional to N. Completed nodes retain the Prime's native color; a nonzero remainder has its own magnitude color. Aggregate Q never creates a Black or other QMO identity.

Restore heals H first and carries all remaining magnitude into nodes. Degrade consumes Q before H. Healthy Primes can partially and repeatedly spend Q without changing H or acquiring a tap limit. Prime self-Restore is prohibited. White reactivation is exactly H1/N0/R0, preserving identity and slot.

`state.py` preserves the sealed historical bounded-C ABI for inherited conformance. Explicit adoption migrates N=C//r and R=C%r while preserving intrinsic health, Prime revision, identity, slot and history. Current matches contain no active C/C_max storage. Decomposition is checked with native INT add/equal programs; decimal wire encodings of N/Q preserve exactness without changing the Hypervisor safe-number ABI.
