# Sandbox Domains

<!-- raeon:current-spec sandbox -->

Authority: GAME_CANON for supplied high-level rules. The original Cycle-1 objects and catalog relations are [imported](../../../data/qmo/README.md); broader operators and runtime-instance admission remain OPEN/SOURCE_IMPORT_REQUIRED.

Each player begins with 3 permanent universal Sandbox Domains; the permanent base cannot fall below three. Effects may create additional temporary domains. Committed Field Generators cannot be independently extracted and moved. Whole Sandbox Domains may participate in merge/fusion. Topology depends on participating Generator geometry, not Sandbox provenance.

Utility-created temporary Sandboxes have maximum committed Generator capacity: Red 3, Orange 4, Yellow 5, Green 6, Blue 7, Violet 8 (ColorCharge + 2). A fourth Generator cannot enter a Red temporary Sandbox. Permanent starting Sandboxes are exempt from this colored FG-capacity system. The separate active-space cap is nine per player, including up to six additional spaces. Capacity never guarantees closure or a manifold. Temporary destruction/expiry remains OPEN. Normal Utility identity copy limit 3 applies: Red Sandbox, Red Sandbox, Yellow Sandbox, Blue Sandbox is permitted with respect to these copy rules; there is no one-per-color rule.

## Configuration Space terminology and states

Configuration Space is the general object. Permanent universal spaces are A, B, C; Sandbox / Field A–B–C are historical aliases. Sandbox Activation creates an additional temporary Configuration Space with the existing capacity rules above.

GAME_CANON minimum states: EMPTY = no committed Generator configuration; CONFIGURING = one or more committed Generators without accepted closure; RESOLVED = QMO closure VALID and a resulting Local Manifold. First commitment moves EMPTY → CONFIGURING; VALID closure moves CONFIGURING → RESOLVED. CONFIGURING is an active visual/game object, never a blank slot. Non-closing construction carries no automatic Graveyard penalty.

PROVISIONAL vocabulary: FUSED / represented-by-derived-space, and INACTIVE/REMOVED for temporary expiry if later defined. Generator lifecycle labels IN_HAND, COMMITTED, CONFIGURED, CONTRIBUTING_TO_RESOLVED_MANIFOLD are descriptive candidates, not a finalized runtime state machine. Graveyard requires a separately accepted routing rule.

Resolved reopening/reconfiguration is now accepted. OPEN: temporary expiry, relation-check timing, merged-domain capacity ceiling/runtime admission, and reconciliation of permanent base identity/minimum with merge/fusion's reduced independently active spaces. Preserve the existing permanent minimum of three; do not infer destruction/recreation of A/B/C or a split rule from the fusion visual model. See [fusion](../fusion/SYSTEM.md), [board](../../game/board/SYSTEM.md), [structured states](../../../data/topology/configuration-spaces.json).


## Persistent mutable container

The Configuration Space owns identity, capacity, committed FG contents, XY positions, 3D orientations, relationship/closure state and its current resolved field QMO, if any. A field/manifold is the space's current resolved state, not an immutable replacement for the container.

Temporary capacity is a maximum, never a required construction count. A Violet space may contain three FGs and resolve a Red field when admitted. Capacity color and current field color are independent.

Adding another FG within capacity to a RESOLVED space destabilizes its prior field and returns it to CONFIGURING. The player may reposition/reorient contents within the same domain until a new admitted closure becomes RESOLVED. Example: Violet capacity, three-FG Red field → add a fourth → CONFIGURING → four-FG Orange if admitted. Individual committed FGs still cannot be independently extracted or transferred.

Strategic presentation is EMPTY/dormant, CONFIGURING/unresolved animated, RESOLVED/stable active field. Selecting/tapping enters detailed configuration; exiting returns to the same shared state. Merge composition and its board-width cost follow [merge/fusion](../fusion/SYSTEM.md); splitting or un-fusing is not supplied.

## Resolution and field runtime — accepted 2026-09-30

Configuration Space is a live State Geometric workspace, **not part of the QMO corpus**. Runtime queries the existing corpus without regenerating it. Resolution requires both correct FG QMO membership for an existing topology and admitted XY positioning plus 3D orientation. Wrong membership or pose leaves a nonempty space CONFIGURING without an active field; empty remains EMPTY. No Configuration Frontier object exists. Runtime pose admission still needs implementation and missing mathematical authority.

A field's topology/QMO identity is separate from its mutable current color. Native/max color comes from its QMO. A native Green field degraded by three has current Red and supplies only Red; Restore may raise current color up to native Green. At current color zero the field is destroyed, supporting FG card identities route to Graveyard, and the space ceases exposing that active field. Exact transaction ordering and temporary-space expiry remain OPEN. Non-closing configuration alone never triggers this destruction penalty.

A resolved ordinary field has READY/USED availability. READY generates current color once per refresh cycle, becomes USED and retains its topology. Ending ACTIVE does not refresh it; unused availability persists into DEFENSE. Exact refresh boundary, partial/all-at-once output allocation and Emergent generation cadence remain OPEN. [Match authority](../../game/match/SYSTEM.md) governs admitted operations.
