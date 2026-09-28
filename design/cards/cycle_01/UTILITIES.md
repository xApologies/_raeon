# Cycle-1 Utility structure

Authority: GAME_CANON for the structure supplied in [recovery source](../../../provenance/sources/current-state-recovery-0002.txt). Numerical working ranks identified below are PROVISIONAL — accepted current working design, not final balance. [accepted-state.json](../../../data/manifests/accepted-state.json) stores the machine-readable structure; this is its design interpretation. Concept labels are not final names or allocated runtime card IDs.

**50 / 50 structural slots accounted for: DESIGN STRUCTURE ACCEPTED.** The module remains DESIGN under the existing pipeline: FORMALIZED requires all applicable gates 00–09 accepted. No subsystem GOLD, game phase completion, or playable behavior is claimed.

## Allocation

| Family | Slots |
| --- | --- |
| Transduction | 18 |
| Activation (tempo control) | 7 |
| Sandbox Activation | 6 |
| Draw / Deck | 7 |
| Graveyard / Recovery | 6 |
| Stability / Protection | 6 |
| Total | 50 |

## Transduction — 18

Dedicated rank equals literal magnitude. Universal chooses RESTORE or DEGRADE when resolved and trades one rank of magnitude for flexibility. No Red Universal and no dedicated White Restore/Degrade belong to this ordinary family. No costs or unspecified targets are inferred.

| Family | Rank | Charge effect |
| --- | --- | --- |
| Restore | Red | +1 |
| Restore | Orange | +2 |
| Restore | Yellow | +3 |
| Restore | Green | +4 |
| Restore | Blue | +5 |
| Restore | Violet | +6 |
| Degrade | Red | -1 |
| Degrade | Orange | -2 |
| Degrade | Yellow | -3 |
| Degrade | Green | -4 |
| Degrade | Blue | -5 |
| Degrade | Violet | -6 |
| Universal Restore-or-Degrade | Orange | ±1 |
| Universal Restore-or-Degrade | Yellow | ±2 |
| Universal Restore-or-Degrade | Green | ±3 |
| Universal Restore-or-Degrade | Blue | ±4 |
| Universal Restore-or-Degrade | Violet | ±5 |
| Universal Restore-or-Degrade | White | ±6 |

## Activation — 7

| Identity rank | Accepted function | Detailed per-rank scope |
| --- | --- | --- |
| Red | Early USED → READY | OPEN |
| Orange | Early USED → READY | OPEN |
| Yellow | Early USED → READY | OPEN |
| Green | Early USED → READY | OPEN |
| Blue | Early USED → READY | OPEN |
| Violet | Early USED → READY | OPEN |
| White | Early USED → READY | OPEN |

Ordinary use changes READY → USED; normal refresh eventually returns USED → READY (exact timing OPEN). Activation returns an eligible, already-earned legal resource/object to READY early. It is temporal availability/tempo control, does not itself create color, and cannot create QMO legality. Exact eligibility, effect/scope and other per-rank behavior remain OPEN.

## Sandbox Activation — 6

| Temporary Sandbox rank | Maximum committed Field Generators |
| --- | --- |
| Red | 3 |
| Orange | 4 |
| Yellow | 5 |
| Green | 6 |
| Blue | 7 |
| Violet | 8 |

Capacity = ColorCharge + 2 for Red through Violet only. A fourth Generator cannot be committed to Red; Violet holds at most 8. Capacity is bounded configuration space, not proof of a manifold: even 8 Generators in Violet require QMO closure. Three permanent starting Sandboxes are universal and exempt from this temporary colored-capacity rule. Their permanent floor, commitment restrictions, and whole-domain merge/fusion rules remain intact. Destruction/expiry remains OPEN.

Normal Utility identity copy limit is 3; there is no color uniqueness rule. Red Sandbox, Red Sandbox, Yellow Sandbox, Blue Sandbox respects these copy limits.

## Draw / Deck — 7

This is a mixed set, not a Red–White ladder. These are accepted working ranks. Raw draw cannot exceed Draw 3 in Cycle 1 without amendment.

| Concept | Working rank | Effect |
| --- | --- | --- |
| Draw 1 | Orange | Draw 1 card |
| Draw 2 | Green | Draw 2 cards |
| Draw 3 | Violet | Draw 3 cards |
| Survey | Yellow | Look at top 3; return in any order; no direct card advantage |
| Selection | Green | Look at top 3; take 1 into hand; put remainder on deck bottom |
| Exchange | Blue | Discard any number from hand; draw that many; net hand-count change 0 for the exchange |
| Deep Survey | White | Look at top 7; take 1 into hand; shuffle remainder back into deck |

Exchange improves hand quality and intentionally interacts with Recovery. Deep Survey preserves uncertainty and is not an unrestricted exact-card tutor. Draw/Deck manipulates deck/hand flow, never Graveyard retrieval. Hand-size maximum, overflow behavior, short-deck resolution, and unspecified ordering/timing remain OPEN; no hand-size value is canonized.

## Graveyard / Recovery — 6

| Structural effect | Working rank |
| --- | --- |
| Return 1 Field Generator from Graveyard to hand | Yellow |
| Return 2 Field Generators from Graveyard to hand | Blue |
| Return 3 Field Generators from Graveyard to hand | White |
| Return 1 Utility from Graveyard to hand | Green |
| Return any 1 non-Prime from Graveyard to hand | Blue |
| Return up to 3 cards from Graveyard to deck top in chosen order | Violet |

The family-wide prohibition on Prime recovery/resurrection also applies to the sixth slot: “cards” does not authorize Prime recovery. Rank primarily expresses rarity/power, not direct charge magnitude. Recovery returns cards to circulation; it does not reconstruct a destroyed manifold. Recovered Generators must be used normally to create new topology admitted by QMO closure. Exact balance/targeting/timing remain OPEN.

## Stability / Protection — 6

Restoration replaces lost color. Stability/Protection prevents or modifies loss/persistence; its sixth slot amplifies an existing support-bound field.

| Concept | Accepted effect | Unresolved detail |
| --- | --- | --- |
| Color Guard | Reduce/absorb next incoming degradation by a fixed amount | Magnitude/rank OPEN |
| Prime Guard | Protect one Prime from its next eligible degradation event | Duration/rank/timing OPEN |
| Manifold Guard | Protect one Local Manifold from its next eligible degradation event | Duration/rank/timing OPEN |
| Shield Lock | Temporarily prevent degradation of an existing Prime shield | At least Blue; exact rank/duration OPEN |
| Structural Anchor | Next otherwise-lethal degradation leaves one already-valid Local Manifold at Red / charge 1 | Unspecified targeting/timing/duration/rank OPEN |
| Emergent Amplification | Increase an active Emergent Field by +1 charge, capped at Violet / charge 6 | Unspecified rank/target-selection/timing OPEN |

Structural Anchor preserves an already-valid structure; it never bypasses closure. Amplification allows Red → Orange → Yellow → Green → Blue → Violet. It creates no field, changes no QMO support relation, makes nothing independently targetable, and cannot preserve a field after required support loss. No behavior above the ordinary Violet cap is invented.

Emergent Fields cannot be directly attacked or destroyed. Break their required supports to remove them: if M_A + M_B → E and required M_A is destroyed, E becomes inaccessible/gone according to the relation. **Coupling Stabilizer is rejected and absent from this catalog.** Emergent Amplification fills slot six.

## Remaining work

Final names, flavor, IDs, wording, unresolved ranks, exact targeting, timing, duration, balance testing, implementation, integration, gameplay testing, applicable performance, and release validation remain OPEN/UNTESTED. Utilities cannot override mathematics. This design checkpoint supplies no executable card catalog, mathematics, QMO objects, or gameplay implementation.


## Cumulative checkpoint 0003 clarifications

The exact catalog is PARTIALLY FORMALIZED as a descriptive design status; the module remains DESIGN, with architecture GAME_CANON / STRUCTURALLY DEFINED. Balance and gameplay validation are UNTESTED; runtime is OPEN / UNIMPLEMENTED. None of the 50 slots is claimed implementation-ready. Final UT-001 through UT-050 assignment and ordering remain OPEN.

Draw/Deck groups three raw-draw effects, three information/selection effects and one hand-cycling effect. Survey changes hand count by 0 for its effect; Selection only selects among the top three. Exchange moves n from hand to Graveyard and n from deck to hand. Recover up to 3 to deck has no immediate direct card advantage and may combine with Draw 3 when the player has the required effects; this does not define new timing windows.

Prime Guard does not change Prime QMO identity. Manifold Guard protects an already-valid object and cannot close invalid geometry. Color Guard and Shield Lock timing remain OPEN. Amplification does not change closure or support identity; a Violet field does not become ordinary White/Black, and overflow behavior is OPEN.

Coupling Stabilizer was rejected because direct protection of an already non-targetable, support-dependent field conflicts with or redundantly complicates the support model. Emergent Amplification remains the sixth Stability slot. Working Black concepts belong to the separate [Black-rank design](../BLACK_RANK.md), not these 50 ordinary slots.
