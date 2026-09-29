# Foundational Development Backlog

## DESIGN WORK

### 1. Turn / Match State Machine --- recommended next workshop

Define match setup, starting hand, maximum hand, mulligan, normal draw,
first-player rules, turn phases, ordinary READY refresh timing, Utility
timing windows, opponent interaction windows, Sandbox merge/fusion
timing, manifold activation, Prime activation/transduction timing, turn
end, empty-deck behavior, temporary Sandbox expiry, surrender/timeout.

### 2. Victory / Loss

Explicitly decide ordinary victory/loss. Strong working direction to
discuss: destruction of all three opposing Primes as primary loss
condition. Decide deck exhaustion, timeout, surrender, etc.

### 3. Prime Catalog

Design all 30 ordinary Prime identities: rank/health distribution,
differentiation, effects, passive/active/ triggered behavior,
shield/transduction constraints, targeting, timing, rules text,
machine-readable effects.

### 4. Utility Finalization

UT-001..UT-050 ordering, names, unresolved ranks, targets, timing,
duration, balance.

### 5. Hand / Deck / Graveyard

Finalize hand maximum, draw rules, overflow, discard routing, empty-deck
behavior, setup.

### 6. Black System Later

Actual three Black Prime identities, Fourth Prime ability, Black Utility
catalog/crafting.

### 7. Collection / Economy Later

Credits, rewards, packs, crafting recipes, duplicate conversion, pacing.

## SOURCE IMPORT WORK

Genesis mathematics; Chirality Fabric; Propagation Engine; QMO
definitions/API; closure operators; transduction math/API; 120 Field
Generator QMO data; 60 base manifold package; 343 fusion-derived
package; 1,691 Emergent package; complete 2,094 atlas; Cycle Generation
Constitution; deterministic RenderSpecs; Blender-facing atlas/reference;
higher-dimensional projection mathematics.

## IMPLEMENTATION WORK --- LATER

Runtime; turn/state engine; card runtime; QMO integration; Blender
automation; GPU renderer; AI; multiplayer; persistence; collection/shop
UI; Windows build; iPad build.

## Recommended dependency order

Turn/Match -\> Victory/Loss -\> Prime Catalog -\> Utility Finalization
-\> QMO imports -\> Vertical Slice -\> Implementation.
