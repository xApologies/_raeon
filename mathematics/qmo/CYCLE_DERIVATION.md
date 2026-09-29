# Cycle Derivation Mathematics

## 1. Closed recursive seed

A Cycle begins with a closed recursive domain:

\[
\mathcal D_0
\]

and a finite family of refinement maps:

\[
\Phi=\{\phi_i:\mathcal D_0\to\mathcal D_0\}.
\]

Cycle 1 specialized the recovered hypercubic family with eight dyadic children:

\[
\phi_\epsilon(x)=\frac{x+\epsilon}{2},
\qquad
\epsilon\in\{-1,+1\}^3.
\]

This matches the eight-site 2×2×2 chirality byte.

## 2. Chirality Byte

Let:

\[
V=\{A,B,C,D,E,F,G,H\}.
\]

Define occupancy:

\[
\omega:V\to\{0,1\}
\]

with Cycle-1 constraint:

\[
\sum_{v\in V}\omega(v)=4.
\]

Cradle:
\[
\omega(v)=1.
\]

Void:
\[
\omega(v)=0.
\]

Occupied sites may carry local state:

\[
s_v=(\rho_v,R_v,B_v,\chi_v,H_v,\ldots).
\]

## 3. Orientation

Let \(G\) be the proper rotation group of the cube.

A Generator state may be represented by:

\[
g\cdot(\omega,s),
\qquad
g\in G.
\]

Rotation changes exposed relationships without necessarily evolving the intrinsic
state.

## 4. Field Generator QMO

A canonical Generator object is:

\[
FG_i =
(\alpha_i,\omega_i,g_i,R_i,B_i,\chi_i,\partial_i,P_i)
\]

where:
- \(\alpha_i\) = recursive/fractal address,
- \(\omega_i\) = byte occupancy,
- \(g_i\) = orientation class,
- \(R_i\) = Resolution,
- \(B_i\) = Bandwidth,
- \(\chi_i\) = chirality metadata,
- \(\partial_i\) = boundary signatures,
- \(P_i\) = provenance.

## 5. Compatibility

Define a Cycle-specific operator:

\[
K(FG_i,FG_j;\theta_i,\theta_j).
\]

Its result is not presumed universally valid across all Cycles.

A valid relation yields one or more typed compatibility edges.

A failed relation yields a termination record.

Cycle-1 v1.0 uses a game-canonical boundary complement rule inherited from the
locked playfield build. If a future Cycle changes this operator, that is an Amendment.

## 6. Local closure

For a candidate Generator subset \(S\):

\[
\operatorname{Close}(S)\in\{\text{VALID},\text{TERMINATES}\}.
\]

Cycle-1 executable criterion:
- compatibility graph connected,
- induced graph cycle-bearing,
- allowed Generator count.

Only then map count to color.

## 7. Fusion

For local manifolds \(M_i,M_j\):

\[
F(M_i,M_j).
\]

If the underlying physical Generator instances are disjoint and their union closes,
produce:

\[
M_{ij}^{*}.
\]

## 8. Emergent coupling

Preserve supports and evaluate cross-interface:

\[
I_{ij}
=
\{(u,v):u\in M_i,\ v\in M_j,\ u\sim_\chi v\}.
\]

The Cycle coupling functional:

\[
\kappa(M_i,M_j)
\]

maps admissible interface structure to either:
- termination,
- or an EmergentFieldQMO with a derived color.

## 9. Closed-domain principle

Given API domain \(\mathcal A\), if

\[
x,y\in\mathcal A
\]

and an internal operator

\[
f:\mathcal A\times\mathcal A\to\mathcal A\cup\{\bot\}
\]

returns a valid object, then:

\[
f(x,y)\in\mathcal A.
\]

If it returns \(\bot\), the termination is stored as internal knowledge.

This is the recursive closure principle used by raeon.
