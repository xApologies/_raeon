# RAEON Genesis application — Pass 1

Stable package identity `raeon`, version `0.1.0`. This production application
realizes an empty two-player match inside the existing Genesis Horizon. It uses
the same pinned compiler, GVM and native geometric engines as the conformance
application, which remains under tests.

`raeon_realize.gen` instantiates 37 distinct native Geometrics and executes 163
explicit relationships: one State-to-Match containment and 162 application
relationships. There is one Match and, per player, one Player organization, one
Board, five separate attachment roles, Deck/Hand/Graveyard, Prime and Configuration
regions, three fixed empty Prime positions and permanent universal spaces A/B/C.
All contents are empty. No cards or expansion spaces are created.

The immutable manifest hashes both Genesis programs and `definitions.json`.
Definitions supply bounded representations and semantic/projection metadata;
they never construct objects or relationships. The real Genesis program creates
the native graph. The representation uses the existing finite Generic3p1p1
engineering encoder; it is not a QMO definition, a Cycle-1 generator, or a proof
of the upstream OPEN dimensional mathematics.

The trusted owner admits the package, routes admission through sea → Shell →
Nexus → State, executes its compiled realization, validates the resulting graph
and publishes a single State successor. Rejection leaves the previous root and
bindings intact. Identical package admission is idempotent. Runtime identities
and semantic roles survive checkpoint/restart; screen coordinates are absent.

`raeon_observe.gen` checks the realized Match through the pinned VM. Public views
expose structural objects and relationships. The owner view additionally exposes
that player's empty container memberships/order and private visibility relations.
Opponent container internals and native backend resources never enter those
projections. View authority comes from the trusted session binding; `player_1`
and `player_2` are semantic roles, not screen positions or external account IDs.
These are projections of one State. Observation does not advance game revision.

Run `python -B tools/genesis_runtime.py demo --headless --application raeon` from
the repository root. This boots, realizes, binds both real Hypervisor sessions,
decodes HELLO/SNAPSHOT, checkpoints, restarts/restores, reconnects and compares
both views and their persistent identities across a new boundary epoch.

The only exported operation is OBSERVE. Cards, movement, draw/shuffle, QMO/field
resolution, Prime arithmetic, color, turns, combat, victory, presentation and
platform ports remain outside Pass 1. Whole-game phase remains PREPRODUCTION.
See the [receipt](../../../../development/modules/core-game/PASS_01_RECEIPT.md).
