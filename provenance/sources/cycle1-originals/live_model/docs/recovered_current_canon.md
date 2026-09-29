# raeon — recovered current canon

Recovery date: 2026-09-13. Source: MK147 Book v2.3, Checkpoint 4 (2026-09-01).

These are the original current API objects and their 74 metadata entries, not newly invented game rules. The original archive and historical PDF are preserved separately. See PROVENANCE_AND_CONFLICTS.json for version reconciliation.

## raeon
Address: `@sfo/raeon`
Type: `card_game`; status: `active`

Mage-glass topology-building strategy card game centered on constructing fields and moving color.

### casing
Canonical spelling is 'raeon'. It is a word, not an acronym; use lowercase in ordinary prose.
Source label in original API: Current MK-147 raeon canon

### pronunciation
Pronounced approximately 'ray-on'.
Source label in original API: Current MK-147 raeon canon

### core_rule
raeon is fundamentally a game of building valid topology and moving color around the play field.
Source label in original API: Current MK-147 raeon canon

### math_culture
The game reinforces mathematics socially because Genesis-field structure is described and understood mathematically throughout civilization.
Source label in original API: Current MK-147 raeon canon

### material_culture
Cards and markers are mage glass so the game pieces can participate in bounded Genesis-field interactions.
Source label in original API: Current MK-147 raeon canon

## raeon Cards
Address: `@sfo/raeon/cards`
Type: `game_component_domain`; status: `active`

Mage-glass cards used in raeon; distinct from collectible Genesis Cards.

## Cycles
Address: `@sfo/raeon/cycles`
Type: `release_system`; status: `active`

Recurring proprietary card-set releases derived from protected topology/math families.

### definition
Each yearly/current release family is a Cycle.
Source label in original API: Current MK-147 raeon canon

### math_origin
A Cycle is derived from a proprietary mathematical/topological family controlled by the manufacturer.
Source label in original API: Current MK-147 raeon canon

### new_content
Cycles can introduce new Primes, Field Generators, Utilities, Shapings, marker interactions, and topology families.
Source label in original API: Current MK-147 raeon canon

### visual_identity
Each Cycle has a recognizable topological visual language in the mage-glass card presentation.
Source label in original API: Current MK-147 raeon canon

### cycle_mark
Cards can carry a small topological/glyph marker identifying the Cycle/set.
Source label in original API: Current MK-147 raeon canon

### discovery
Players experiment with new Cycles, map compatibility, and can eventually 'crack' hidden topology relationships.
Source label in original API: Current MK-147 raeon canon

### legacy
Later Cycles may unexpectedly interact with older cards, reviving old strategies and market value.
Source label in original API: Current MK-147 raeon canon

## Field Generator Cards
Address: `@sfo/raeon/field_generators`
Type: `card_class`; status: `active`

Cards arranged into valid topological closure to create colored generated fields.

### closure_requirement
Card count alone does not create a field. Field Generator cards must be arranged into a valid closed topological configuration.
Source label in original API: Current MK-147 raeon canon

### red
3 compatible generators in valid closure resolve a Red field.
Source label in original API: Current MK-147 raeon canon

### orange
4 compatible generators in valid closure resolve an Orange field.
Source label in original API: Current MK-147 raeon canon

### yellow
5 compatible generators in valid closure resolve a Yellow field.
Source label in original API: Current MK-147 raeon canon

### green
6 compatible generators in valid closure resolve a Green field.
Source label in original API: Current MK-147 raeon canon

### blue
7 compatible generators in valid closure resolve a Blue field.
Source label in original API: Current MK-147 raeon canon

### violet
8 compatible generators in valid closure resolve a Violet field.
Source label in original API: Current MK-147 raeon canon

### exhaustion
Once a generated field is used to charge an activation marker/Prime during a turn, it is exhausted/committed for that turn and cannot be used again until refreshed.
Source label in original API: Current MK-147 raeon canon

### strategy
Decks can favor many fast low-card Red closures or slower higher-card closures that generate larger color states.
Source label in original API: Current MK-147 raeon canon

## Play Formats
Address: `@sfo/raeon/formats`
Type: `competition_system`; status: `active`

Sanctioned current-Cycle and open/legacy formats.

### sanctioned_current
Sanctioned local-card-shop/tournament play uses only the current Cycle's legal card pool.
Source label in original API: Current MK-147 raeon canon

### rotation_reason
Rotation limits the available topology pool and drives ongoing purchase/trading of current releases.
Source label in original API: Current MK-147 raeon canon

### open
Open/Legacy play allows cards from historical Cycles and supports powerful or unusual cross-cycle topology decks.
Source label in original API: Current MK-147 raeon canon

### casual
Local shops can run casual/open events where older collections and hybrid builds are legal.
Source label in original API: Current MK-147 raeon canon

## raeon Manufacturing
Address: `@sfo/raeon/manufacturing`
Type: `industry_system`; status: `active`

Exclusive patent-controlled production using proprietary mathematics/topologies and mage-glass manufacture.

### exclusive
The raeon manufacturer owns the game rights and relevant mathematical/topological patents, preventing unauthorized commercial reproduction.
Source label in original API: Current MK-147 raeon canon

### patents
Production depends on protected math/topology families.
Source label in original API: Current MK-147 raeon canon

### mage_glass
Cards and physical markers are manufactured in mage glass to enable bounded Genesis-field interaction.
Source label in original API: Current MK-147 raeon canon

## Mage-Glass Markers
Address: `@sfo/raeon/markers`
Type: `game_component_domain`; status: `active`

Mage-glass marker pieces used to carry activation and color charge.

## Pyramid Color-Charge Marker
Address: `@sfo/raeon/markers/pyramid_color_charge`
Type: `marker_type`; status: `active`

Carries quantified color charge produced by an active Prime.

### meaning
Pyramid markers carry color charge.
Source label in original API: Current MK-147 raeon canon

### source
Active Prime Resolution Fields charge pyramid markers.
Source label in original API: Current MK-147 raeon canon

### cost
Each pyramid charged consumes one color step from the source Prime.
Source label in original API: Current MK-147 raeon canon

### targets
A charged pyramid may be applied to generated fields, Prime Resolution Fields, or the player field according to card/effect legality.
Source label in original API: Current MK-147 raeon canon

### destabilize
Applied offensively, pyramid color subtracts/destabilizes target color/coherence.
Source label in original API: Current MK-147 raeon canon

### stabilize
Where an effect permits, pyramid color may stabilize/restore a friendly field or player state.
Source label in original API: Current MK-147 raeon canon

### material
Pyramid markers are mage glass.
Source label in original API: Current MK-147 raeon canon

## Square Activation Marker
Address: `@sfo/raeon/markers/square_activation`
Type: `marker_type`; status: `active`

Carries activation from a resolved generated field into a Prime Resolution Field.

### meaning
Square markers carry activation, not damage or currency.
Source label in original API: Current MK-147 raeon canon

### source
A valid generated field charges the square marker at that field's current color.
Source label in original API: Current MK-147 raeon canon

### destination
The charged square is applied to a compatible Prime Resolution Field to activate or increase the Prime's current charge.
Source label in original API: Current MK-147 raeon canon

### material
Square markers are mage glass.
Source label in original API: Current MK-147 raeon canon

## raeon Market
Address: `@sfo/raeon/market`
Type: `economic_system`; status: `active`

Booster, singles, legacy-card, tournament, collector, and secondary-market economy.

### boosters
Players buy current-Cycle packs/boosters seeking useful generators, Primes, utilities, shapings, and rare topologies.
Source label in original API: Current MK-147 raeon canon

### secondary
Card shops, collectors, brokers, and players support a singles/secondary market.
Source label in original API: Current MK-147 raeon canon

### price_dynamics
A historically cheap card may spike in value if a later Cycle reveals strong cross-cycle compatibility.
Source label in original API: Current MK-147 raeon canon

### collector_plus_play
Cards may have collector value, strategic play value, or both.
Source label in original API: Current MK-147 raeon canon

## Open raeon Design
Address: `@sfo/raeon/open_design`
Type: `open_questions`; status: `active`

Detailed Utility, Shaping, Prime-family, topology-family, deck-size, and balance rules still to be designed.

### utility_cards
Exact utility-card effects remain open.
Source label in original API: Current MK-147 raeon canon

### shaping_cards
Exact shaping-card catalog/effects remain open.
Source label in original API: Current MK-147 raeon canon

### generator_topologies
Exact legal Field Generator topology families remain open.
Source label in original API: Current MK-147 raeon canon

### prime_families
Exact Prime Resolution Field families, compatibility rules, and special behaviors remain open.
Source label in original API: Current MK-147 raeon canon

### deck_size
Exact main-deck size remains open.
Source label in original API: Current MK-147 raeon canon

### balance
Exact tournament balance, refresh timing, draw rules, marker reserve, and turn sequencing remain open.
Source label in original API: Current MK-147 raeon canon

### health_points
The ~40-point player-field scale is provisional.
Source label in original API: Current MK-147 raeon canon

## Player Field
Address: `@sfo/raeon/player_field`
Type: `game_system`; status: `active`

Player health/coherence card: begins White and decays continuously toward zero.

### start
The player field begins at White/full coherence.
Source label in original API: Current MK-147 raeon canon

### continuity
Player health is continuous rather than discrete color-step health.
Source label in original API: Current MK-147 raeon canon

### visual
As coherence decays, the player field continuously moves through White→Violet→Blue→Green→Yellow→Orange→Red→zero, including intermediate densities.
Source label in original API: Current MK-147 raeon canon

### working_scale
Rough working design: approximately 40 total destabilization points from White to elimination; exact value remains provisional.
Source label in original API: Current MK-147 raeon canon

### elimination
When the player's field reaches zero/dissipates, the player loses.
Source label in original API: Current MK-147 raeon canon

### repair
Stabilization can restore the player continuously rather than forcing whole-color jumps.
Source label in original API: Current MK-147 raeon canon

## Prime Resolution Fields
Address: `@sfo/raeon/prime_resolution_fields`
Type: `card_class`; status: `active`

Three persistent Prime cards outside the deck; each has a color-capacity ceiling and must be activated/charged through generated fields.

### count
Current working rule: each player uses three Prime Resolution Field cards outside the main deck.
Source label in original API: Current MK-147 raeon canon

### inactive_start
Prime Resolution Fields begin inactive.
Source label in original API: Current MK-147 raeon canon

### capacity
The printed Prime color is its maximum color capacity/Bandwidth ceiling.
Source label in original API: Current MK-147 raeon canon

### scale
Red=1, Orange=2, Yellow=3, Green=4, Blue=5, Violet=6.
Source label in original API: Current MK-147 raeon canon

### activation
A square activation marker charged by a resolved generated field is committed to a Prime, activating/charging that Prime by the field's color value up to the Prime's printed ceiling.
Source label in original API: Current MK-147 raeon canon

### incremental_charge
A Prime may be charged over multiple turns; repeated lower-color activations accumulate until the Prime reaches its printed maximum.
Source label in original API: Current MK-147 raeon canon

### example_orange
An Orange Prime charged first by Red becomes active at Red; a later Red activation raises it to Orange; further charge cannot exceed Orange.
Source label in original API: Current MK-147 raeon canon

### example_green
A Green Prime charged by Yellow rises to Yellow; a second Yellow activation caps it at Green.
Source label in original API: Current MK-147 raeon canon

### spend
Each pyramid color-charge generated from an active Prime consumes one color step from the Prime.
Source label in original API: Current MK-147 raeon canon

### deactivation
After Red is spent, the Prime becomes inactive.
Source label in original API: Current MK-147 raeon canon

### attackability
Opponents may destabilize an active Prime to reduce its stored color and future pyramid output; dropping it below Red deactivates it.
Source label in original API: Current MK-147 raeon canon

### strategic_role
Primes are color reservoirs/engines and a distinct attack vector alongside generated fields and the player field.
Source label in original API: Current MK-147 raeon canon

## Card Scarcity
Address: `@sfo/raeon/scarcity`
Type: `collector_system`; status: `active`

Controlled print scarcity across all card classes, weighted toward lower-color/common structures.

### all_cards
Scarcity applies across Prime, Generator, Utility, and Shaping cards.
Source label in original API: Current MK-147 raeon canon

### distribution
Print availability is biased toward lower-color/common structures; higher-color/high-capacity cards are produced in smaller quantities.
Source label in original API: Current MK-147 raeon canon

### prime_example
A Cycle's Prime print run may contain many Red Primes and very few Violet Primes; exact percentages remain open.
Source label in original API: Current MK-147 raeon canon

### violet_value
Violet Primes are especially valuable because they provide the largest color-capacity ceiling and are scarce.
Source label in original API: Current MK-147 raeon canon

### legacy_value
Older out-of-print cards may become highly valuable due to age, scarcity, topology compatibility, nostalgia, collector demand, or Open/Legacy utility.
Source label in original API: Current MK-147 raeon canon

### not_auto_win
Scarcity/value expands strategic options but does not by itself guarantee victory.
Source label in original API: Current MK-147 raeon canon

## Shaping Cards
Address: `@sfo/raeon/shaping_cards`
Type: `card_class`; status: `active`

Prestructured game effects; detailed current functions remain open.

## Utility Cards
Address: `@sfo/raeon/utility_cards`
Type: `card_class`; status: `active`

Support/control/tempo cards; detailed current functions remain open.

## Scoped graph edges

- `@sfo/raeon` — HAS_COMPONENT → `@sfo/raeon/cards`
- `@sfo/raeon` — HAS_COMPONENT → `@sfo/raeon/markers`
- `@sfo/raeon` — HAS_FORMATS → `@sfo/raeon/formats`
- `@sfo/raeon` — HAS_MANUFACTURING → `@sfo/raeon/manufacturing`
- `@sfo/raeon` — HAS_MARKET → `@sfo/raeon/market`
- `@sfo/raeon` — HAS_PLAYER_FIELD → `@sfo/raeon/player_field`
- `@sfo/raeon` — HAS_RELEASE_SYSTEM → `@sfo/raeon/cycles`
- `@sfo/raeon` — HAS_SCARCITY → `@sfo/raeon/scarcity`
- `@sfo/raeon` — USES_MATERIAL → `@sfo/genesis_cards/mage_glass`
- `@sfo/raeon/cards` — HAS_CLASS → `@sfo/raeon/field_generators`
- `@sfo/raeon/cards` — HAS_CLASS → `@sfo/raeon/prime_resolution_fields`
- `@sfo/raeon/cards` — HAS_CLASS → `@sfo/raeon/shaping_cards`
- `@sfo/raeon/cards` — HAS_CLASS → `@sfo/raeon/utility_cards`
- `@sfo/raeon/field_generators` — CHARGES → `@sfo/raeon/markers/square_activation`
- `@sfo/raeon/manufacturing` — USES → `@sfo/math/patents/topology`
- `@sfo/raeon/markers` — HAS_TYPE → `@sfo/raeon/markers/pyramid_color_charge`
- `@sfo/raeon/markers` — HAS_TYPE → `@sfo/raeon/markers/square_activation`
- `@sfo/raeon/markers/square_activation` — ACTIVATES → `@sfo/raeon/prime_resolution_fields`
- `@sfo/raeon/prime_resolution_fields` — CHARGES → `@sfo/raeon/markers/pyramid_color_charge`

External target payloads are included in the JSON export and external_references table, not silently counted as raeon objects.
