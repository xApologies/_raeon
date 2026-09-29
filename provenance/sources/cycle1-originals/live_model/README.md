# raeon — Live Model v0.1
Date: 2026-09-13

Purpose
-------
This package freezes the current raeon game-design state into a recovery-safe,
machine-readable and executable model before API construction begins.

It intentionally separates:
1. ESTABLISHED rules stated/accepted by Genesis,
2. PROVISIONAL workshop recommendations,
3. EXAMPLE-ONLY mechanics that were discussed but not adopted,
4. OPEN questions that must still be designed.

This is not yet the final game engine and not the API. It is the live state model
from which the API can now be built.

Core identity
-------------
raeon is a mobile-first geometry/transduction card game.

The player:
    builds geometry -> manifests local manifolds -> moves color -> activates Primes
    -> uses color tactically for restoration/degradation -> manages shield/health.

Most mathematical complexity is concentrated in Field Generator geometry.
The user interface is intentionally simple: tap, tap-to-target, drag, rotate,
press/hold and slide through the color spectrum.

Current fixed set/deck numbers
------------------------------
Cycle size:                200 unique cards
Field Generator cards:     120
Prime Field cards:          30
Utility cards:              50
Constructed deck size:      60
Field Generator max copies: 2
Utility max copies:         3
Prime identity:             unique; no duplicate Prime identity
Active Prime positions:     3

Prime loadout relation to the 60-card draw deck is still recorded as OPEN unless
explicitly finalized later.

Color order
-----------
0, Red, Orange, Yellow, Green, Blue, Violet, White
0,   1,      2,      3,     4,    5,      6,     7

Ordinary generated local-manifold strength:
3 generators -> Red
4 -> Orange
5 -> Yellow
6 -> Green
7 -> Blue
8 -> Violet

White is NOT simply an ordinary 8-generator manifold color.
Cycle 1 currently includes eight White Field Generator cards; they are universal
Generator pieces. 3..8 White Generators can realize ordinary Red..Violet field
strengths respectively, subject to topology/configuration legality.

Architecture
------------
- Every player has 3 permanent Sandbox Domains.
- Additional sandboxes may be established by future card effects.
- A Field Generator played into a sandbox is committed to that sandbox.
- A committed Generator cannot be extracted/moved individually to another sandbox.
- Entire sandboxes may be merged for a larger construction.
- Manifold legality depends on participating Generator identity + geometry, not
  sandbox provenance.
- Position and 360-degree orientation of Generator cards inside a sandbox determine
  available geometry.
- Candidate geometry is shown visually while the player manipulates cards.
- A valid configuration locks and may manifest as a living manifold.
- Multiple lower-order and higher-order configurations can overlap across the 120-card
  Generator language.
- Local manifolds can be used as components in larger-scale relations.
- Compatible active manifolds may support Emergent Fields.
- Emergent-field compatibility/topology is not yet fully enumerated.

Prime model
-----------
Every Prime has:
- printed/native maximum health H_max, ranked Yellow through White,
- current intrinsic health H,
- active color shield/transduction reservoir S,
- directionality/profile to be specified per Prime.

Friendly incoming color:
1. repairs missing intrinsic Prime health first;
2. any remainder becomes shield/transduction color;
3. shield cannot exceed the Prime's shield capacity (currently tied to rank);
4. overflow policy beyond capacity is OPEN and is returned explicitly by the model.

Hostile degradation:
1. removes shield first;
2. overflow damage penetrates intrinsic Prime health;
3. health 0 destroys the Prime for the match under the ordinary rule.

Prime actions:
- spend some amount of shield color,
- that spent amount is the available transduction magnitude,
- spending offense/restoration also lowers defense because shield and expendable
  transduction color are the same register.

This creates the central Prime decision:
    spend color now OR retain it as protection.

Product / progression direction
-------------------------------
Current design intent:
- low-cost premium game;
- no ads;
- no subscription;
- no purchasing Credits;
- no purchasing gameplay card packs with real money;
- in-game card shop uses gameplay-earned Credits;
- randomized packs + expensive deterministic card acquisition are both intended;
- future 200-card Cycles may be inexpensive paid content unlocks;
- three save profiles / Journeys are intended;
- adaptive on-device AI is a design objective;
- nearby human multiplayer should use local peer networking so no central gameplay
  server is required for nearby matches;
- human-vs-human victories may award game-generated Credits.

Do not treat exact prices, rewards, pack odds, AI algorithms, hand size, draw rate,
turn sequencing, Utility catalog, Prime catalog, or topology library as finalized.

Files
-----
CANON_STATE.json
OPEN_QUESTIONS.md
PROVENANCE.md
DESIGN_TIMELINE.md
data/card_scaffold.csv
data/card_scaffold.json
data/schema_cards.json
data/live_model.sqlite
raeon_model/*.py
tests/*.py
examples/demo_prime_state.py
docs/recovered_current_canon.md
visual_references/*

Run tests
---------
python -m unittest discover -s tests -v

Run demo
--------
python examples/demo_prime_state.py
