# Accepted raeon baseline

Authority: GAME_CANON for accepted rules/structure from the [bootstrap source](../../provenance/sources/bootstrap-request.txt) and [current-state recovery source](../../provenance/sources/current-state-recovery-0002.txt). Explicit working ranks and product/economy direction remain PROVISIONAL; unresolved details remain OPEN. [accepted-state.json](../../data/manifests/accepted-state.json) is the machine-readable accepted-state model. Structural slots are not finalized runtime card definitions.

## Mathematical authority

**THE MATHEMATICS IS THE PERMISSION SYSTEM.** The QMO is the canonical mathematical game object. Mathematical legality determines permitted relationships and gameplay operations. Authoritative mathematics/APIs are SOURCE_IMPORT_REQUIRED. Utilities manipulate legal game state but cannot override QMO closure. Rendering does not determine mathematical legality.

API outcomes: VALID, TERMINATES, NOT_APPLICABLE, OPEN, UNTESTED. TERMINATES is explicit mathematical failure; missing data is not automatically termination.

## Cycle and colors

120 Field Generators + 30 Prime Fields + 50 Utilities = 200 ordinary Cycle-1 cards. Constructed decks: 60 cards. Normal copy limits: 2 Field Generators, 3 Utilities. Prime identity: unique. Active Prime positions: 3. Copy limits apply to identity; no additional color-based uniqueness rule exists. Final card definitions remain under design.

0 = no active color magnitude. Red = 1, Orange = 2, Yellow = 3, Green = 4, Blue = 5, Violet = 6, White = 7, Black = 8. Field Generators terminate at White. **BLACK FIELD GENERATORS DO NOT EXIST.** Black rank applies to Prime Fields and Utilities. For direct color effects, charge is a literal magnitude. For many non-color Utilities, rank expresses approximate rarity/strategic power and is not necessarily a numerical resource cost.

## Sandbox Domains

Each player begins with 3 permanent universal Sandbox Domains; the permanent base cannot fall below three. Effects may create additional temporary domains. Committed Field Generators cannot be independently extracted and moved. Whole Sandbox Domains may participate in merge/fusion. Topology depends on participating Generator geometry, not Sandbox provenance.

Utility-created temporary Sandboxes have maximum committed Generator capacity: Red 3, Orange 4, Yellow 5, Green 6, Blue 7, Violet 8 (ColorCharge + 2). A fourth Generator cannot enter a Red temporary Sandbox. Permanent starting Sandboxes are exempt from this colored-capacity system; no other numerical limit is inferred. Capacity never guarantees closure or a manifold. Temporary destruction/expiry remains OPEN. Normal Utility identity copy limit 3 applies: Red Sandbox, Red Sandbox, Yellow Sandbox, Blue Sandbox is permitted with respect to these copy rules; there is no one-per-color rule.

## Closure and inventory

Only AFTER closure succeeds does Generator count determine local color: 3 → Red, 4 → Orange, 5 → Yellow, 6 → Green, 7 → Blue, 8 → Violet. **3 + 5 = 8 does not itself prove a Violet manifold.** The closure operator must admit the configuration.

Base basis: 15 Red + 13 Orange + 11 Yellow + 9 Green + 7 Blue + 5 Violet = 60 Local Manifold QMOs. This basis is not necessarily the complete recursive QMO closure.

Accepted external inventory, all SOURCE_IMPORT_REQUIRED: 60 base Local Manifold QMOs + 343 fusion-derived Local Manifold QMOs + 1,691 Emergent Field QMOs = 2,094 render-relevant field/manifold QMO objects. Counts are accepted claims; objects and correctness proofs are not imported.

## Fusion and emergence

Fusion: M_i ⊕ M_j → M*, when mathematically admitted, produces one DerivedLocalManifoldQMO.

Emergent coupling: M_i + M_j → M_i + M_j + E, when admitted. Supports remain; E depends on them and is not independently targetable. Admission rules await authoritative import. Emergent Fields cannot be directly attacked or destroyed; breaking a required support makes the field inaccessible/gone according to its support relation. Amplification does not make a field targetable or preserve it after support loss. Coupling Stabilizer is excluded from the ordinary Cycle-1 Utility catalog; Emergent Amplification occupies the sixth Stability slot.

## Utilities

All 50 ordinary Utility slots are **DESIGN STRUCTURE ACCEPTED**: 18 Transduction, 7 Activation, 6 Sandbox Activation, 7 Draw / Deck, 6 Graveyard / Recovery, 6 Stability / Protection. The former Sandbox / Geometry family is now Sandbox Activation; tempo describes Activation's strategic function. See the [50-slot design](../cards/cycle_01/UTILITIES.md) for the complete accepted structure and unresolved details.

Transduction is 6 Restore (+1 through +6, Red–Violet), 6 Degrade (−1 through −6, Red–Violet), and 6 Universal (Orange–White, ±1 through ±6, choose at resolution). No Red Universal or dedicated White Restore/Degrade belongs to this 18-card family. Activation refreshes an eligible already-earned legal object from USED to READY early; it creates neither color nor mathematical legality.

Draw/Deck stays within deck/hand flow, with raw draw capped at Draw 3; hand size/overflow remain OPEN. Recovery excludes Prime resurrection and does not reconstruct destroyed manifolds. Protection differs from replacing lost color: Structural Anchor preserves an already-valid Local Manifold at Red/charge 1 on its next otherwise-lethal degradation. Emergent Amplification adds +1 to an active supported field, capped at Violet/6.

Final names/flavor/IDs/wording, unresolved ranks, targeting/timing/duration, balance, implementation, integration, gameplay/performance tests, and release validation remain unfinished. Utility module state is DESIGN, not GOLD or whole-module FORMALIZED: applicable gates 00–09 are not yet all accepted.

## Black rank

Black = 8. Black cards are legal in ordinary decks and are extremely difficult/expensive endgame crafted cards. Exactly three Black Prime identities exist; Black Utilities exist; Black Field Generators do not.

A legal all-Black 60-card deck is 3 Black Primes + 57 Black Utilities and unlocks hidden Black Mode. While all three supporting Black Primes remain alive, FourthPrimeAvailable = true; if any dies, FourthPrimeAvailable = false and the Fourth Prime becomes inaccessible. The Fourth Prime is emergent/supported, not a fourth deck card. Detailed behavior remains OPEN. Do not invent catalog entries or copy-limit exceptions to explain the accepted composition.

## Rendering direction

QMO → deterministic RenderSpec → Blender procedural geometry → mesh → runtime GPU renderer → animated manifold. Mathematics defines the object; rendering makes it visible. RenderSpec/API packages are SOURCE_IMPORT_REQUIRED. Blender mesh generation and GPU live effects are the current direction; no engine, graphics API, mesh, or RenderSpec is fabricated.
