# Pass 2: admitted card collections

Authority: the user-invoked diplomatic pouch preserved in
`provenance/imports/raeon-pass-02/`. Start from Pass 1 at
`23ebfc3be3a4e6ae4883793bfc99b1dbfae67bf8`; keep main unchanged.
Whole-game PREPRODUCTION and all existing module gates remain unchanged.

## Compatible local binding contracts

The frozen upstream is `c89676fc26000ae6f5fdad66a56e118b285d9b1d`.
No upstream file is edited. Existing graph profile `genesis 0.1.0` compiles
application handlers, bounded instance/relation units, and actual local Road
transport. The pinned Section-14 `genesis 0.3.0` compiler/interpreter performs
integer equality, addition, and bounds. Its 256-register verifier limit and
the existing runtime's finite budgets remain enforced.

The local `typed-int-const-v1` ABI binds only two declared, typed INT constant
registers in precompiled predicate templates. It does not interpolate source,
alter control flow, or add language keywords. Instantiated programs are
encoded, decoded, and verified before execution. This is a reference-runtime
application binding, not a claim that upstream has an external-input keyword.

`state-collections-v1` is a generic ADMIT/TRANSFORM operator contract. Its
caller is the actual compiled application handler; its arguments are the
strictly typed intent plus an owner-bound trusted grant. Its effects are
bounded instance creation, ordered collection transfer/permutation/inspection,
or collection extension. Copy limits, categories, capacities, exact recovery
counts, destination kinds, and effect-source references are declared in the
Genesis attributes and the accepted-source catalog/configuration. The
Hypervisor contains no card-operation code. Bypassing the handler cannot
produce the closure required for Horizon publication.

Each unit compiles within the original verifier's bounds. A roster composes
60 bounded native creation/relation units under one candidate root. A transfer
executes a real Portal/Rainbow Road carrying the selected card's native
instance, checks closure, retains its logical identity, and replaces its
active containing relation. Local endpoints remain instances inside State;
there are still exactly four machine domains. Native card representations
are finite reference fixtures with source commitments, not newly generated
QMO mathematics or a claim of field closure.

## State, authority, privacy, and compatibility

Catalog records retain their source bytes/hash/pointer and provisional/OPEN
metadata. Internal source handles do not assign printed Prime or Utility IDs.
The original 120 FG and 2,094 atlas records are not modified.

Authoritative card membership, order, history, catalog commitments, grants,
and RNG state participate in the atomic root and checkpoint. The test harness
alone injects a capability for the generic conformance grant issuer. The
issuer has no Hypervisor/Port export and is absent from normal startup.
Grants bind match, application, actor, owner, operation, revision, exact typed
selection/destination arguments, effect source, and replay ID. Grant
consumption and outcomes publish with the same candidate as the movement.

Index zero is next/top. A retirement batch is inserted at Graveyard top in
caller-declared order. Shuffle v1 uses SHA-256 of canonical JSON
`[algorithm, private seed, counter]`, an unsigned 256-bit big-endian value,
rejection above the largest multiple of the current width, and descending
Fisher-Yates. Counters include rejected draws and commit only on success.

Live views expose the owner's Hand and public placed cards, container counts,
and dynamic region members. Future Deck contents are hidden from both players.
Graveyard records require a bounded grant; an inspection view expires when
the committed revision changes. Internal seeds, grants, native diagnostics,
and future identities are not player receipt fields.

The production application keeps ID `raeon` and becomes package schema 3,
version 0.2.0. The exact Pass-1 package is retained as a historical test fixture;
its original hashes and assertions remain checked. Schema-1 conformance and
schema-2 checkpoint behavior remain supported. Schema-3 checkpoints require
their exact installed package and catalog; incompatible candidates are
rejected before live replacement.

Policy gates remain in `development/modules/core-game/PASS_02_POLICY_GATES.json`.
No opening deal, draw cadence, Utility play/consumption, Prime combat, temporary
space expiry, field closure, pose system, or victory policy is implemented by
these helpers. The acceptance specification remains 83 mandatory cases; this
decision itself is not execution evidence.
