# R85 — RESOLUTION-SEPARATION INVARIANCE

## Problem

Changing Resolution depth must not itself move the objects.

Resolution is distinguishable organization, not propagation.

Let a relational state be `r in Rel_D`.

Let:
`delta(r)` be its underlying separation datum.

Let:
`q_R(r)` be the readout at Resolution `R`.

A **pure Resolution change** changes only the readout/filter:

`q_Ri(r) -> q_Rj(r)`

while preserving the underlying relational state `r`.

Therefore:

`delta(r)` is invariant under pure Resolution refinement/coarsening.

Formally, for a Resolution-only transition `eta_(i,j)`:

`eta_(i,j) : (r,R_i) -> (r,R_j)`

we require:

`delta(pi_rel(eta_(i,j))) = delta(r)`.

## Important distinction

The readout of distance can become more or less precise:

`rho_R(delta)`

but the underlying separation has not changed merely because Resolution changed.

Only a non-identity propagation corridor:

`gamma : r_0 -> r_1`

can change the relational state and therefore potentially change separation:

`delta(r_1) != delta(r_0)`.

## Verdict

**CLOSED.**

This formalizes the original constraint:
**recursive depth may change while distance between the objects remains unchanged.**

Next:
`@qmo/relational_motion_beyond_distance`.
