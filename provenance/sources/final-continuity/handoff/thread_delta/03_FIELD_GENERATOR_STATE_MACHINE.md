# Field Generator / Configuration Space State Machine

Recommended formal state vocabulary recovered from the thread:

Configuration Space: - EMPTY - CONFIGURING - RESOLVED - FUSED /
represented by derived space where applicable - INACTIVE/REMOVED for
temporary-space expiry if later defined

Generator lifecycle: - IN_HAND - COMMITTED - CONFIGURED (working
descriptive state; exact runtime state model still to formalize) -
CONTRIBUTING_TO_RESOLVED_MANIFOLD - GRAVEYARD only when a separate
accepted destruction/discard rule actually sends it there

Do not invent automatic Graveyard routing for failed closure.

Core transition: EMPTY -\> CONFIGURING after first Generator commitment.
CONFIGURING -\> RESOLVED when QMO closure returns VALID. CONFIGURING
remains CONFIGURING while the player continues an unresolved legal
construction. Exact rules for reopening/reconfiguring a RESOLVED
manifold remain OPEN and require explicit design.

Inter-space checks: RESOLVED + RESOLVED -\> evaluate QMO relation.
Possible known semantic outcomes: - no admitted relationship /
termination - fusion -\> derived Local Manifold - emergence -\>
supported Emergent Field

Exact timing of when these checks occur remains OPEN.
