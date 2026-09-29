# Genesis Horizon Board --- Current Design

The board is divided into static infrastructure bands and a dynamic
central Configuration Field.

## Player infrastructure

Closest to the local player: - Deck - Hand - Graveyard

There is NO discard zone and NO exile zone in the current game. Do not
add conventional card-game zones without an actual raeon mechanic
requiring them.

Immediately above the player's resource interface sit three fixed Prime
positions. Prime positions are spatially invariant. They may animate,
shield, degrade, activate, and transduce, but do not move around the
board.

The opponent is the reflected upper side. The opponent's hand is hidden.

## Genesis Horizon

The center divider is named the **Genesis Horizon**.

Each player's dynamic Configuration Field lies between their Prime band
and the Genesis Horizon.

## Configuration Spaces

Use **Configuration Space** as the general board term.

The three permanent universal starting spaces are: - Field /
Configuration Space A - Field / Configuration Space B - Field /
Configuration Space C

Historically these were also called Sandboxes. A Sandbox Activation
Utility creates an additional temporary Configuration Space. Thus
"Sandbox" can remain the card/mechanic language while "Configuration
Space" is the general board object.

Configuration Space positions are elastic/dynamic. With only A/B/C,
three spaces center themselves. Add a temporary Sandbox and the board
recomputes to four centered spaces; add another and it recomputes again.
If a temporary space disappears, remaining spaces close ranks.

Sandbox identity persists while screen position changes. Screen
coordinates are presentation state, not identity.

## Configuration-space visual states

At minimum: 1. EMPTY --- available space, no committed Generator. 2.
CONFIGURING --- one or more Field Generators committed, closure not yet
resolved. 3. RESOLVED --- QMO closure succeeded and the Local Manifold
is represented at board scale.

A CONFIGURING space must still have an active visual/animation; it is
unresolved topology, not a blank slot.

## Entering a Configuration Space

Tap/select a Configuration Space to transition from strategic board view
into detailed configuration view. There the player can inspect, commit,
and manipulate Field Generator configuration/orientation. Exit/back
returns to strategic board view, preserving the current configuration
state.

## Dynamic central topology

The Configuration Field is the primary moving/animated region: - spaces
redistribute elastically; - spaces may connect; - fusion can move two
spaces together and collapse them into one derived configuration
space; - emergence leaves supports distinct and creates a relational
field between/around them; - unresolved fields animate; - resolved
manifolds animate; - QMO connections follow moving spaces.

Static edges + dynamic center is a governing visual rule.
