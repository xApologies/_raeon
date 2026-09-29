# raeon Constitution

## Article I — Mathematical Authority

1. The QMO is the canonical game object.
2. Rendered images, meshes, animations, and UI are representations of a QMO.
3. A render may fail to represent a QMO accurately; the QMO does not change because
   of a render failure.
4. Legal gameplay relations must be derivable from internal API mathematics.
5. Generator count alone never proves a closure.
6. A numerical color result is assigned only after mathematical closure succeeds.
7. Failed closures are first-class knowledge and must be stored explicitly.

## Article II — Source Authority Order

When sources conflict, resolve in this order:

1. Explicit Genesis canonical correction in the current development record.
2. Current Cycle Constitution / Canon Lock.
3. Recovered Chirality Fabric definitions.
4. Recovered Genesis Field definitions.
5. Recovered Propagation Engine definitions.
6. Earlier raeon checkpoint.
7. Workshop proposals.
8. Examples.

Never silently merge contradictory versions.

## Article III — Chirality Byte

A game-facing Chirality Byte is a 2×2×2 object with eight fixed sites.

Cycle-1 canonical interpretation:
- four occupied sites = cradle,
- four unoccupied sites = void,
- occupied sites may carry local energetic/chromatic state,
- orientation changes the presented local relation,
- orientation and state evolution are distinct operations.

The six four-site face views are derived restrictions of the intrinsic byte.

The user-supplied face `A,C,E,G` is canonical as one explicit face view.

## Article IV — Field Generator QMO

Each Field Generator card is one first-class QMO.

A FieldGeneratorQMO must expose at least:
- canonical QMO address,
- Cycle ID,
- intrinsic chirality-byte state,
- cradle sites,
- void sites,
- orientation class,
- recursive/fractal address,
- chirality metadata,
- Resolution metadata,
- Bandwidth metadata,
- boundary/face signatures,
- compatibility edges,
- manifold memberships,
- provenance status.

Field Generator identity must not be defined solely by artwork.

## Article V — Base Local Manifold

A LocalManifoldQMO is a mathematically closed configuration of Generator QMOs.

For Cycle 1:
- 3 generators → Red
- 4 → Orange
- 5 → Yellow
- 6 → Green
- 7 → Blue
- 8 → Violet

This ladder assigns field strength after closure.
It is not itself the closure rule.

## Article VI — Fusion

Fusion:
- consumes/commits the participating local manifold domains into one derived Local Manifold,
- must use disjoint physical Generator instances at runtime,
- must satisfy internal closure,
- may terminate,
- produces a first-class DerivedLocalManifoldQMO when valid.

Fusion is not the same operation as emergent coupling.

## Article VII — Emergent Coupling

Emergent coupling:
- preserves the support manifolds,
- creates an additional supported field if the coupling operator admits it,
- produces an EmergentFieldQMO,
- is not directly targetable,
- collapses if its supporting relation breaks.

The color of an Emergent Field is derived from its coupling relation, not from simple
Generator-count arithmetic.

## Article VIII — Termination

A failed mathematical relation is not absence of data.

Store:
- TERMINATES,
- reason,
- operator used,
- supports tested,
- evidence/metrics sufficient to reproduce the decision.

Distinguish:
- VALID
- TERMINATES
- NOT_APPLICABLE
- OPEN / UNTESTED where appropriate

## Article IX — Recursive Closure

The base manifold catalog is a basis, not necessarily the full closure.

The API may derive new QMOs from existing internal QMOs and internal operators.

If:
- all operands are internal,
- the operator is internal,
- the derivation succeeds,
then the result becomes an internal derived QMO.

No external mathematical object may be introduced silently.

## Article X — Rendering

The required production chain is:

QMO → deterministic RenderSpec → Blender mesh → Metal runtime

The QMO carries mathematical identity.
RenderSpec carries geometric realization instructions.
Blender builds the mesh.
Metal performs runtime animation and state visualization.

A higher-dimensional QMO is visualized through an explicit projection/embedding.
Blender may not substitute unrelated geometry.

## Article XI — Reproducibility

Every Cycle build must emit:
- machine-readable state,
- SQLite QMO database,
- JSON exports,
- typed edge graph,
- derivation records,
- termination records,
- RenderSpecs,
- tests,
- manifest,
- SHA-256 hashes,
- Cycle-specific amendment file.

## Article XII — Amendments

Changing any of the following requires an explicit amendment:
- fractal seed family,
- chirality-byte rule,
- compatibility operator,
- closure operator,
- color ladder,
- number of Field Generator cards,
- base manifold distribution,
- fusion semantics,
- emergent coupling semantics,
- QMO identity schema.

Art direction does not require a mathematical amendment unless it changes the
mathematical object or its projection law.
