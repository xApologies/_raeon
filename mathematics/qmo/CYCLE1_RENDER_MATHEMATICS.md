# raeon Render Mathematics v0.3

## Purpose

This layer converts a closed mathematical manifold QMO into deterministic render geometry
for Blender authoring and Apple Metal runtime rendering.

It does **not** claim that the render mesh is a literal physical embedding of AERA.
The render mesh is a faithful game-domain visualization of the QMO topology and state.

---

## 1. QMO state

A Field Generator QMO carries

\[
G_i = (\mathcal B_i,\chi_i,R_i,B_i,\alpha_i)
\]

where:

- \(\mathcal B_i\) is the local \(2\times2\times2\) chirality byte,
- \(\chi_i\) is chirality/orientation metadata,
- \(R_i\) is Resolution,
- \(B_i\) is Bandwidth,
- \(\alpha_i\) is the recursive fractal address.

A chirality byte has eight labeled sites \(A,\ldots,H\), with exactly four cradle/occupied
sites and four void/unoccupied sites.

A Local Manifold QMO is

\[
M = (V,E,\mathcal G,C,\Xi)
\]

where:

- \(V\) are manifold control nodes,
- \(E\) are topological connections,
- \(\mathcal G\) is the participating Generator set,
- \(C\in\{R,O,Y,G,B,V\}\) is native field color,
- \(\Xi\) stores rendering/state invariants.

---

## 2. Generator embedding

Each participating Generator is assigned a deterministic anchor in \(\mathbb R^3\):

\[
a_i=(x_i,y_i,z_i).
\]

For a manifold with \(n\) Generators, anchors are placed on a closed carrier curve

\[
a_i =
\begin{pmatrix}
\rho(\theta_i)\cos \theta_i\\
\rho(\theta_i)\sin \theta_i\\
\zeta \sin(k\theta_i+\phi_i)
\end{pmatrix},
\qquad
\theta_i=\frac{2\pi i}{n}.
\]

The radial modulation is

\[
\rho(\theta)=r_0+r_1\cos(m\theta+\psi).
\]

The integers \(k,m\) and phases \(\phi_i,\psi\) are derived deterministically from the
QMO's chirality parity, fractal address, and compatibility degree.

This creates repeatable geometry: the same QMO always produces the same base manifold.

---

## 3. Edge curves

For every topological edge \((i,j)\in E\), render a cubic Bézier curve

\[
\gamma_{ij}(t)
=
(1-t)^3P_0
+3(1-t)^2tP_1
+3(1-t)t^2P_2
+t^3P_3,
\quad t\in[0,1],
\]

with

\[
P_0=a_i,\qquad P_3=a_j.
\]

The internal controls use the manifold normal and chirality sign:

\[
P_1=P_0+\lambda\,n_{ij}+\eta\,u_{ij},
\]

\[
P_2=P_3+\lambda\,n_{ij}-\eta\,u_{ij},
\]

where \(u_{ij}\) is the unit vector along \(a_j-a_i\), \(n_{ij}\) is a deterministic
normal, and

\[
\lambda = \lambda_0(1+\beta_R R),
\qquad
\eta = \eta_0\,\operatorname{sgn}(\chi).
\]

Thus chirality changes winding without changing graph identity.

---

## 4. Tube / filament surface

Each edge curve is converted to a tube using a parallel-transport frame.
Let \(T(s)\) be the tangent and \((N_1(s),N_2(s))\) an orthonormal transported frame.

The tube surface is

\[
X(s,\varphi)
=
\gamma(s)
+
r(s)\left[
N_1(s)\cos\varphi + N_2(s)\sin\varphi
\right].
\]

Tube radius is driven by Bandwidth:

\[
r(s)=r_0\left(1+\beta_B\,\widehat B\right)
\left(1+\epsilon\sin(\omega s+\phi)\right).
\]

Bandwidth therefore affects visible transport capacity, not topological identity.

---

## 5. Resolution

Resolution controls discretization/detail rather than overall scale.

Let \(R\) be the normalized Resolution state. Then:

\[
N_{\text{curve}} = N_0 + \lfloor k_R R\rfloor
\]

samples each curve, while

\[
N_{\text{ring}} = N_{r0}+\lfloor q_R R\rfloor
\]

samples each tube ring.

Increasing Resolution adds distinguishable internal structure without widening the
manifold footprint.

---

## 6. Field shell

The active manifold can expose an optional translucent field shell.

We construct an implicit scalar field

\[
F(x)
=
\sum_i w_i K(\|x-a_i\|)
+
\sum_{(i,j)\in E} w_{ij}K(d(x,\gamma_{ij})),
\]

using a compact kernel such as

\[
K(r)=e^{-r^2/\sigma^2}.
\]

The visible shell is an isosurface

\[
F(x)=\tau.
\]

Blender may generate this with volume-to-mesh/metaball techniques.
Metal may approximate it procedurally or render only filaments for performance.

---

## 7. Active energy phase

Animation does not require changing QMO topology.

Define phase

\[
\Phi(s,t)
=
ks-\omega t+\phi_0.
\]

Shader emissive intensity may use

\[
I(s,t)
=
I_0
+
A\left(\frac{1+\cos \Phi(s,t)}{2}\right)^p.
\]

This creates moving energy along a fixed manifold.

A tap at time \(t_0\) injects a transient activation pulse

\[
P(t)
=
A_p e^{-\lambda(t-t_0)}
\]

for \(t\ge t_0\), modulating emission, displacement, particle rate, or bloom.

---

## 8. Five-dimensional state, three-dimensional render

raeon's gameplay may carry a conceptual \(3+1+1\) state:

\[
q=(x,y,z,\tau,\chi).
\]

Metal renders a 3D projection:

\[
\Pi:
\mathbb R^{3+1+1}\rightarrow\mathbb R^3.
\]

A practical game projection is

\[
\Pi(x,y,z,\tau,\chi)
=
\begin{pmatrix}
x+\alpha\sin(\tau+\chi)\\
y+\alpha\cos(\tau-\chi)\\
z+\beta\sin(\tau)\cos(\chi)
\end{pmatrix}.
\]

The extra coordinates therefore modulate visible deformation/phase rather than being
misrepresented as literal screen dimensions.

---

## 9. Color state

The field color ladder is discrete:

\[
R=1,\ O=2,\ Y=3,\ G=4,\ B=5,\ V=6,\ W=7.
\]

The render API exports the integer state plus a semantic color name.
Actual RGB/linear-light values belong to the renderer's palette table, not the QMO.

---

## 10. Determinism

Every renderable QMO must have a deterministic seed:

\[
s=\operatorname{SHA256}(\text{canonical QMO address}).
\]

Any procedural phases, anchor perturbations, or decorative particles derive from \(s\),
ensuring Blender and Metal reproduce the same object family.

---

## 11. Rendering contract

The mathematical QMO is canonical.

`RenderSpec` is a downstream adapter containing:

- control nodes,
- topological edges,
- sampled spline controls,
- tube parameters,
- Resolution/Bandwidth parameters,
- chirality sign,
- native/current color,
- deterministic seed,
- animation constants,
- optional implicit-shell constants.

Blender consumes `RenderSpec` to build/edit/export a mesh.
Metal consumes `RenderSpec` and/or exported mesh buffers to animate the field.
