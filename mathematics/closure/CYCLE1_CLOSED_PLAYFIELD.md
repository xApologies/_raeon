# raeon Closed Playing Field v1.0 — LOCKED

## Canonical game-law principle

**The mathematics is the permission system.**

A move is legal only when the internal raeon API returns a valid mathematical closure.
A numerically plausible combination is not sufficient.

For a manifold pair `(A,B)` the API stores explicit outcomes:

- `VALID` — the operation is mathematically admitted by the current raeon game model.
- `TERMINATES` — the operation was evaluated and fails.
- `NOT_APPLICABLE` — the catalog-level query cannot safely stand for a runtime physical-instance query.

The API does not treat missing edges as failures.

## Base playing field

60 canonical Local Manifold QMOs:

- 15 Red / 3 Generator
- 13 Orange / 4 Generator
- 11 Yellow / 5 Generator
- 9 Green / 6 Generator
- 7 Blue / 7 Generator
- 5 Violet / 8 Generator

Total unordered base-manifold pair space:

`C(60,2) = 1770`.

Every one of those 1770 pairs now has an explicit stored relation record.

## Fusion

Fusion consumes two local manifold domains and attempts to create one new Local Manifold.

The resulting Generator population must:
1. represent disjoint physical Generator instances,
2. contain 3..8 instances,
3. pass the internal chirality compatibility closure test,
4. be connected,
5. be cycle-bearing.

Only then does Generator count assign the resulting ordinary color:
3 R, 4 O, 5 Y, 6 G, 7 B, 8 V.

A valid derived fusion is a first-class `DerivedLocalManifoldQMO`.

## Emergent coupling

Coupling does **not** consume the parent manifolds.

The API evaluates the cross-interface between their constituent Generator QMOs.
A sufficiently coherent interface yields an `EmergentFieldQMO`.

Emergent fields:
- preserve their support manifolds,
- are not directly targetable,
- collapse automatically if their support relation breaks.

## Negative knowledge

Termination is stored explicitly.

The closed API therefore contains both:
- permitted paths,
- forbidden/terminating paths.

This negative space is part of the game.

## Current playfield statistics

Fusion:
{
  "TERMINATES": 825,
  "NOT_APPLICABLE": 602,
  "VALID": 343
}

Fusion results by color:
{
  "VIOLET": 169,
  "BLUE": 120,
  "GREEN": 54
}

Emergent coupling:
{
  "VALID": 1691,
  "TERMINATES": 79
}

Emergent results by color:
{
  "BLUE": 318,
  "VIOLET": 499,
  "GREEN": 362,
  "YELLOW": 237,
  "ORANGE": 214,
  "RED": 61
}

Red/Yellow pair space:
- total: 165
- valid catalog fusions: 111
- terminating catalog fusions: 9
- not-applicable due to shared Generator identity: 45

## Authority

The closed-playfield coupling/fusion operators are now **canonical for raeon game v1.0**.

They remain game mathematics. This package does not claim the operator is a new external
physical theorem or a unique consequence of the recovered AERA/Chirality research corpus.

The distinction is preserved in provenance.
