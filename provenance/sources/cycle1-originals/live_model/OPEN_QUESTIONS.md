# OPEN QUESTIONS

These are intentionally unresolved. Do not infer answers in future recovery.

## Core turn structure
- Final starting hand size: 5, 6, 7, or another value?
- Cards drawn per turn?
- Exact turn phases?
- When do used Local Manifolds refresh/reactivate?
- When do used Primes refresh, if ever, without an explicit reactivation action?
- Can a player act during the opponent's turn?

## Deck / Prime loadout
- Do the three selected Prime cards live outside the 60-card draw deck, or count inside it?
- Exact Prime uniqueness rule in deck construction vs active board state.
- Is there a minimum/maximum number of Utilities or Generators? Current direction favors no forced ratio.

## Sandbox
- Exact semantics of temporary sandbox expiration/removal.
- What happens to cards/manifold occupying an extra sandbox if its support expires?
- Exact timing and costs for sandbox merge/fusion.
- Can a fused construction later split? Current commitment logic suggests no free extraction, but final rule is open.
- Exact maximum practical/allowed sandbox count. Developer target discussed around ~5 active local manifolds, not a hard ceiling.

## Generator topology
- Full connection signature vocabulary for 120 Generator cards.
- Exact geometric/manifold matching algorithm.
- Exact topology families.
- Exact number of canonical topology/manifold classes.
- Exact per-card compatibility/incidence landscape.
- Exact meaning of chirality, resolution, bandwidth, portals, corridors, Rainbow Road, fusion, inheritance in game abstraction.
- How White universal Generators participate with non-White Generators.
- Whether/how a White Generated Field exists.

## Local and emergent fields
- Exact rule for internal color manipulation by Local Manifolds.
- Exact rule for Emergent Field creation.
- Exact color of each Emergent Field relation.
- Whether Emergent Fields directly transduce to both friendly and enemy targets or route through Primes.
- Exact relationship between sandbox fusion and manifold coupling.

## Prime Fields
- Full 30-Prime catalog.
- Exact restore/degrade/hybrid magnitude profiles.
- Exact shield capacity rule (currently modeled as printed rank).
- Overflow behavior when friendly color exceeds missing health + shield capacity.
- Prime activation timing and used/ready state timing.
- Exact special set bonuses for compatible sets of three Primes.
- Number and behavior of White Prime cards per Cycle.
- Whether rare Prime revival Utility exists.

## Utilities
- Full 50-card catalog.
- Exact immediate vs duration Utility rules.
- Exact duration color-degradation semantics.
- Sandbox-grant Utilities.
- Restoration, reactivation, recovery, graveyard, emergent-field boost effects.
- Whether Utilities have their own printed color/rank and what that rank means.

## Rarity / collection
- Full Red/Orange/Yellow/Green/Blue/Violet/White rarity distribution across 200 cards.
- Relationship between rarity color and mechanical color (must remain explicitly separated where needed).
- Pack size and card distribution.
- Duplicate handling and resale value.
- Direct card purchase prices in gameplay Credits.
- Credit earning rates.
- Completion pacing.

## AI / multiplayer
- Adaptive AI algorithm.
- Difficulty ladder and names.
- What information AI may use; design intent is legal-information-only, no cheating.
- Nearby multiplayer transport implementation.
- Reward amount for AI vs nearby-human wins.
- Whether losing nearby-human games earns Credits.

## Product
- Exact base price and Cycle price.
- Cycle format vs Open format details.
- Whether collections are independent per Journey or there is a master collection.
