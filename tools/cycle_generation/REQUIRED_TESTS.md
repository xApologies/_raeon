# Required Validation Gates

A Cycle may not be locked until all applicable gates pass.

## Generator gates
- exactly 120 Field Generator QMOs unless Amendment changes count
- unique QMO address
- unique card ID
- valid 2×2×2 byte
- exactly 4 cradle / 4 void for Cycle-1 byte rule
- orientation class valid
- provenance present

## Base manifold gates
- exact required color distribution
- each manifold has correct Generator count
- every manifold passes closure operator
- no duplicate canonical manifold identity
- all referenced Generators exist

## Pair-space gates
For N base manifolds:
\[
\binom{N}{2}
\]
pair records must exist.

For Cycle 1, N=60 → 1770.

Every pair must have:
- fusion verdict,
- emergent verdict,
- reason/evidence.

## Derived-QMO gates
- every VALID result has a QMO
- every derived QMO points to valid supports
- every result is reproducible
- no derived address collision

## Rendering gates
- RenderSpec deterministic
- same QMO → same RenderSpec
- all topology indices valid
- projection parameters present
- Blender builder can consume schema
- Metal data structure can deserialize schema

## Provenance gates
- every rule labeled RECOVERED, GAME_CANON, PROVISIONAL, or OPEN
- every Cycle-specific change documented in Amendment
- no workshop example silently promoted to canon
