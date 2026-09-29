# Field Generator Interaction Recovery --- Pre-New-Propagation Baseline

This document captures the Field Generator gameplay/mathematical model
established in the originating raeon thread before reconciliation with
the newly supplied Propagation Engine package.

## Identity

A Field Generator is a first-class QMO/configuration object, not merely
a spell card.

Cycle 1 contains 120 Field Generator identities. Identity copy limit is
2. Maximum Generator rank is White. Black Field Generators do not exist.

The 120 identities are intended to be generated/derived from the
Chirality Fabric + Propagation Engine + QMO landscape, not manually
invented as arbitrary effects.

## Configuration

A player chooses a Configuration Space C_i and commits Field Generators
to it.

Working notation: `C = (C_i ; FG_1^{o_1}, FG_2^{o_2}, ..., FG_n^{o_n})`

where `o_i` is the current admissible orientation/configuration state of
Generator i.

Committed individual Generators cannot simply be extracted and moved to
another Configuration Space. Whole configuration domains may participate
in fusion/merge.

## Orientation / manipulation

The originating thread established that Generator configuration includes
player-manipulable orientation/rotation. The visual interaction may
resemble rotational manipulation, but the mathematical rule is stricter:
the player may move among states/orientations admitted by the
Generator/domain/QMO model.

Do NOT canonize arbitrary free XYZ rotation for every Generator unless
the authoritative QMO data says so.

The purpose of manipulation is to change the mathematical configuration,
not merely the appearance.

## Closure

The QMO/closure layer evaluates the active Generator configuration.

Only after closure is VALID does Generator count assign ordinary
manifold color: 3 -\> Red 4 -\> Orange 5 -\> Yellow 6 -\> Green 7 -\>
Blue 8 -\> Violet

`n = 8` alone does not imply Violet. Closure is required.

Before closure the Configuration Space is CONFIGURING.
Failed/non-closing configuration does not automatically send cards to
Graveyard; no such penalty was canonized.

Mathematical outcomes include VALID, TERMINATES, NOT_APPLICABLE, OPEN,
UNTESTED. Missing data is not TERMINATES.

## Base and recursive landscape

Base Local Manifold basis: 15 Red + 13 Orange + 11 Yellow + 9 Green + 7
Blue + 5 Violet = 60.

Accepted external inventory: 60 base Local Manifolds 343 fusion-derived
Local Manifolds 1,691 Emergent Fields 2,094 total render-relevant
field/manifold QMOs.

## Fusion

For admitted relation: `M_i ⊕ M_j -> M*`

Two resolved Configuration Spaces may physically converge/collapse into
one derived Configuration Space. Fusion reduces the number of
independently active configuration spaces by one for that relationship.
The supports do not remain independently operational while fused.

Arithmetic compatibility does not prove fusion.

## Emergence

For admitted relation: `M_A + M_B -> M_A + M_B + E`

Supporting Configuration Spaces remain distinct. They may reposition to
show their relationship. E appears between/around/above them as a
relational visual object.

E is not independently targetable. Breaking required support
removes/inactivates E.

## Rendering

QMO -\> deterministic RenderSpec -\> Blender procedural geometry -\>
mesh -\> runtime GPU renderer -\> animation.

Strategic board view shows a compact manifold/unresolved-field
representation. Detailed Configuration Space view shows the Generator
construction itself.

## Recovery boundary

The gameplay architecture above is recoverable. The actual
FG-001..FG-120 QMO catalog, exact chirality states, admitted
transformations, closure table, and RenderSpecs are not reconstructed
here and must come from authoritative source packages.
