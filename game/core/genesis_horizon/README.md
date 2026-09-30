# Genesis Horizon

This is a bounded host reference implementation of one sea → Shell → Nexus →
State machine. Its compiled Genesis 0.1 programs execute through the pinned
Section 10 compiler, semantic checker/linker and GVM. The explicit bindings use
the coherent Section 5 vendored Instantiation, Transformation, Portal and Rainbow
Road engines. No symbolic fallback, generated game mathematics, or new language
syntax is used.

`src/boot.gen` instantiates all four native domains and resolves containment.
`road_in.gen` and `road_out.gen` implement the fixed adjacent Shell/Nexus interfaces
and carry request/readout commitments. `state.gen` produces immutable native State
successors. `lifecycle.gen` checks and seals quiescent State. These linked primitive
handlers cover the sea/Shell/Nexus responsibilities without empty per-domain
source stubs. The Python binding supplies trusted authority, declared MMO/profile
resolution, persistent resources and atomic root publication.

The supplied profile is a finite engineering fixture using the upstream
Generic3p1p1 cell encoder, deterministic Fabric recipe and canonical domain
registry. Four separately instantiated bounded Geometrics carry architectural
types 9/10/11, 7/8, 6 and 5. This demonstrates software containment, admission,
real native cell transforms and transport. It does **not** prove higher-dimensional
mathematical embeddings or close upstream OPEN geometry/coupling mathematics.

The test-only conformance package realizes two distinct MMO-backed objects in
State. Its declared RELATE_A_B and TRANSFORM_A handlers resolve a real relationship
and use upstream MIRROR_CHIRALITY. Stable identities remain while immutable native
versions and History advance. Production gameplay policies are not implemented.

Each compiled invocation binds the same persistent native resource graph.
Candidate transforms create immutable overlay files; publication atomically
replaces a flushed root journal containing both bindings and the scoped outcome.
An exception before publication restores candidate references, never edits old
cells. Return/delivery failure after publication recovers the recorded outcome.
Readouts are detached authorized projections. Native audit receipts include host
time and paths; declared semantic roots exclude those fields.

Checkpoint requires a serialized transaction boundary and copies the native
overlays, History, allocator, compiler identities and root journal with exact
hashes. Restore validates a separate candidate before publication, preserves
semantic identities/root and changes boundary epoch. Storage is confined to the
configured instance directory. A checkpoint is a recovery point; later uncheckpointed
history is not promised after an intentional rewind. Power-loss durability beyond
the host filesystem's fsync/atomic-replace guarantees is not asserted.

Use `python tools/genesis_runtime.py --help` from the installed source root. Read
the maintained [execution record](../../../development/modules/core-game/GENESIS_RUNTIME_EXECUTION.md)
for current evidence, limits and delivery status. Whole-game phase remains
PREPRODUCTION; native-device tests remain NOT_RUN.
