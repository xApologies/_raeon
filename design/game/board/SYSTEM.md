# Genesis Horizon board

Current Pass-05 authority: [match tempo and charge-node rules](../../../data/game/pass-05-runtime.json). The named supersessions in that contract govern current matches. The earlier text below remains the sealed design/conformance record; its superseded capacities, bounded charge, and OPEN timing entries do not govern an adopted Pass-05 match. Whole-game PREPRODUCTION and unaccepted module gates remain unchanged.


<!-- raeon:current-spec board -->

Authority: GAME_CANON for the explicitly recovered board objects, zone exclusions, identity and state relationships. Detailed configuration camera/control constitution is accepted; exact board geometry, animation realization and gesture tuning remain OPEN.

Each side has a bounded infrastructure band: Deck, Hand, Graveyard. There is no discard pile or exile zone. The opponent occupies the reflected upper side and their hand is hidden. “Discard” names an action, not a new zone. Existing Exchange sends cards to Graveyard; preserve that accepted destination. Unspecified timing and other routing questions remain OPEN.

Immediately above each infrastructure band are three fixed Prime positions. They may animate, activate, shield, degrade and transduce; their screen positions are spatially invariant. The central divider is the Genesis Horizon. The dynamic Configuration Field lies between each Prime band and the Horizon.

Permanent universal Configuration Spaces A/B/C start centered. Sandbox Activation adds temporary spaces such as S1. Spaces redistribute as the population changes and close ranks when a temporary space disappears; its expiry rule is still OPEN. Space identity persists while screen coordinates change. Coordinates are presentation state, never game identity.

Strategic view shows compact EMPTY/CONFIGURING/RESOLVED spaces, unresolved fields, Local Manifolds, relations, Primes and the Horizon. Selecting a space enters detailed configuration view exposing committed Generators and admitted mathematical manipulation. Returning preserves the same state. The views are two projections of one state, never duplicate game state.

[Configuration Space states](../../topology/sandbox/SYSTEM.md), [Generator interaction](../../topology/field_generators/SYSTEM.md), [fusion](../../topology/fusion/SYSTEM.md), [emergence](../../topology/emergent_fields/SYSTEM.md), [UI realization](../../ui_ux/SYSTEM.md), [board data](../../../data/board/genesis-horizon.json).


INACTIVE ordinary Primes remain in their fixed positions at H=C=0 and may be reactivated by White Restore Prime to (1,0). Configuration views use fixed top-down XY placement plus 3D orientation; strategic and detailed views share one state. Spaces are persistent mutable containers, with admitted merge trading two independent spaces for one.

## State ownership and card containers

BOARD is one stable identity-bearing Geometric per player/match in Genesis State. It is a dynamic relational framework with five typed attachment roles: Deck, Hand, Graveyard, Prime Region and Configuration Region. A port/attachment role is distinct from its attached child; container and card identities do not become BOARD identity.

Every card instance is a persistent Geometric (FG, Prime or Utility). Deck, Hand and Graveyard contain cards only. Deck is ordered/shuffleable, with size supplied by the format (currently 60), and normal draw accesses the top/next card. Hand normal capacity is 7. Graveyard is ordered; arbitrary access requires an accepted effect. All card moves preserve identity/history and validate destination/admission before an atomic relationship change; failed admission leaves source membership intact. This does not finalize multi-card overflow or destruction transaction ordering.

Configuration Region starts with permanent universal A/B/C and no expansion spaces. Admitted Sandbox Activation effects can add up to six spaces; **maximum active spaces per player is 9**. Layout is independent of identity. Merge's two-to-one independent-space cost remains accepted; permanent-base accounting after merge remains OPEN.

Authoritative changes are staged successor-State transformations mediated through Nexus, with no partial commit on failed admission. Host input/rendering cannot directly mutate State. Existing Rainbow Road carries admitted card/color transport. The visible center-divider name does not restrict the Genesis Horizon VM to a screen line; [runtime architecture](../GAME_DESIGN_DOCUMENT.md) defines the machine boundary.
