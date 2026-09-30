# RAEON — Genesis Horizon and Python Hypervisor
## Implementation work order v2 · 2026-09-30

**Directive:** implement both components in `xApologies/_raeon`, compile and execute the Genesis programs with the actual upstream toolchain, demonstrate their integration, and package the results. This is not a request for another proposal, architecture synopsis, documentation-only change, or fake-runtime demonstration.

**Only write repository:** `xApologies/_raeon`.
**Read-only upstream:** `xApologies/_bricked`.
**Delivery scope:** reusable singleton Genesis Horizon + operational Python translation fence + real headless integration. Full RAEON gameplay and native iOS/Android/Windows applications are later deliverables.

This work order supersedes the implementation instructions in `RAEON_CODEX_IMPLEMENTATION_HANDOFF_2026-09-30.md`. It preserves the accepted architecture and gameplay decisions. It does not invalidate useful work already present in the Codex task. Reconcile this order with that work and continue; do not restart.

**Important status distinction:** this document specifies work to execute. Neither this document nor its acceptance-case file is executable implementation or evidence that a test passed.

---

## 1. Start here: first actions, not a planning loop

Perform these actions in order in the existing `_raeon` workspace:

1. Read applicable `AGENTS.md`, `PROJECT_CONSTITUTION.md`, `DEVELOPMENT_CONSTITUTION.md`, `CONTRIBUTING.md`, `development/PIPELINE.md`, the current module authority map, and the active task's execution record.
2. Inspect `git status --short --branch`, `git log -8 --oneline`, and the existing worktree. Identify existing Horizon/Hypervisor source before creating any new files. Do not reset, clean, overwrite, or discard unrelated work.
3. Verify authorized access to `_bricked` and actual source bytes, including required LFS objects. Establish the precise upstream revision. Do not ask for credentials in chat or embed credentials in files.
4. Resolve the implementation locations in section 3. Reuse equivalent existing locations; only use the specified defaults when no established implementation exists.
5. Create/update the single execution record, dependency lock, and task branch. Record the actual worktree and upstream commit, not just branch names.
6. Execute the upstream compiler baseline in section 4. Produce parsed AST, lowered IR, verified bytecode, and an execution receipt from an existing upstream example.
7. Start implementing the first missing work unit in section 13. Save files and coherent commits throughout; do not stop after writing the inventory.

Continue ordinary implementation, test failures, correction, and integration autonomously. Stop for missing access, a demonstrated missing semantic capability that cannot be composed from supported facilities, or a decision changing accepted game/Genesis semantics. Do not ask the director to approve every source file, ordinary bug fix, or work unit.

### 1.1 Repository persistence and write boundaries

All new maintained source, schemas, tests, packaging commands, dependency locks, and concise provenance belong in `_raeon`. All task branches/commits/pull requests target `_raeon`. `_bricked` is never an implementation destination for this task.

Run tools that write caches/fixtures/build output against an isolated dependency working copy under an ignored `_raeon` build/dependency area. Keep the pinned authoritative upstream source unchanged. A compatibility patch, if needed, belongs in `_raeon`, names the precise upstream revision, and remains explicitly separate from the frozen source.

A local file is not a commit. A local commit is not a successful push. Follow existing authorization to push coherent checkpoints to the task branch; report separately when remote persistence is unavailable. Never force-push or merge into main without the required authorization. Do not create a second concurrent writer over another task's working files.

### 1.2 Observed baselines, not rollback instructions

During handoff preparation, the inspected `_raeon/main` commit was `69a0030805b8c3858c877a514e2f50644421115a`. The inspected `_bricked/bootstrap/canonical-architecture` source revision was `c89676fc26000ae6f5fdad66a56e118b285d9b1d`.

The active Codex branch may contain newer work not represented by either default-branch view. Inspect it first. These commits are reproducible navigation baselines, not instructions to overwrite newer accepted work or treat a working upstream branch as merged main.

---

## 2. What must exist at delivery

There are **exactly three top-level architectural objects**:

```text
GENESIS HORIZON  <->  PYTHON HYPERVISOR  <->  PLATFORM PORT
```

The present task implements the first two and a headless conformance implementation of the third. Boundary schemas, codecs, adapters, queues, and build helpers are internal implementation parts, not new architectural domains.

### 2.1 Genesis Horizon

Implement one complete contained VM profile:

```text
sea: one coupled 9D/10D/11D containing object
  contains Shell: one coupled 7D/8D interaction object
    contains Nexus: one 6D hypercube mediation object
      contains State: one 5D / 3+1+1 application-state object

Chirality Fabric: foundational throughout
Rainbow Road: internal information transport throughout
```

`sea` is the literal outer identifier. No object named `C`, `CSEA`, or `SEAT`. Configuration Space label C and numerical charge variables are unrelated and remain valid.

The four identities are persistent machine-domain identities. Their versions, receipts, transport envelopes, application Geometrics, and ancestry are not additional domain instances. Do not split Shell into two objects or sea into three. Do not implement an eleven-stage processing pipeline.

**Mandatory semantic route:** external input enters through sea, then Shell, then Nexus, then State; permitted readout returns through Nexus, Shell, sea. Rainbow Road realizes the admitted traversals. Do not move the authoritative State domain itself into Shell/sea merely to simulate a message route: transport the request/readout organization while State remains contained by Nexus.

The Horizon must operate independently of RAEON rules. RAEON is an admitted application organization in State. No Prime arithmetic, deck policy, field-color recipe, or gameplay authority belongs in the reusable Horizon or Hypervisor.

### 2.2 Python Hypervisor

Implement a usable library with lifecycle, a real Horizon adapter, a versioned byte interface, strict validation, trusted session binding, synchronization, retry safety, bounded buffering, fault reporting, and checkpoint/replay coordination.

It hosts/coordinates the supported reference runtime and translates only the Horizon's admitted projections and incoming intentions. It does not become the Genesis interpreter or game rules engine. Supplied upstream Python compiler/VM/backend code remains language implementation, not Hypervisor game logic.

### 2.3 Scope of proof

The delivery must demonstrate actual `.gen` execution through the supplied compiler/runtime and through the Hypervisor in both directions. It must also document the reference backend actually used. This is not a claim of physical higher-dimensional hardware, completed mathematical embedding proofs, hostile-code isolation, App Store acceptance, or three finished native platform ports.

Do not use these exclusions to omit the two components. Do not pretend unrelated open game timing/victory rules block a game-agnostic conformance application.

---

## 3. Exact implementation destinations and file responsibilities

The repository already has `game/`, `platform/shared/`, `tools/`, `tests/`, `data/`, `development/`, and `provenance/` responsibilities. Do not create another top-level repository structure.

**Path rule:** first inspect current work for equivalent files. If an equivalent implementation home exists, reuse it and record a one-time path mapping in the execution record. Otherwise implement the following layout. File names below are instructed destinations, not claims that these files already exist.

| Destination under `_raeon` | Implement here |
|---|---|
| `game/core/genesis_horizon/src/` | Actual Genesis modules described below. |
| `game/core/genesis_horizon/bindings/python/src/raeon_genesis_horizon/` | Supported upstream compiler/runtime adapter; no replacement game engine. |
| `game/core/genesis_horizon/README.md` | Actual build/run/integration commands and scope. |
| `platform/shared/python_hypervisor/src/raeon_hypervisor/` | Python fence library. Use a `src` package layout; do not import the repository's `platform/` as Python's standard-library `platform`. |
| `platform/shared/python_hypervisor/schemas/` | Single authoritative boundary schema and sample wire vectors. |
| `platform/shared/python_hypervisor/pyproject.toml` | Installable library metadata, package data, test/dependency constraints. |
| `platform/shared/python_hypervisor/README.md` | Public API, byte protocol, trust model, native-port integration instructions. |
| `data/platform/genesis-runtime-lock.json` | Source revisions, files/hashes, dialect entry points, dependencies, backend, artifact hashes. |
| `data/platform/genesis-horizon-profile.json` | Singleton machine profile, supported capability set, resource-limit defaults, profile/schema version. |
| `tools/genesis_runtime.py` | Implemented, reproducible command entry point specified in section 12. |
| `tests/unit/hypervisor/` | Codec, validation, queues, retry and lifecycle unit tests. |
| `tests/integration/genesis_horizon/` | Real compiler/runtime and joint Horizon/Hypervisor tests. |
| `tests/integration/genesis_horizon/application/` | The small Genesis conformance application and its real definitions. |
| `tests/integration/genesis_horizon/cases/` | Data-driven acceptance cases imported from this work order. |
| `development/modules/core-game/GENESIS_RUNTIME_EXECUTION.md` | One live execution record and requirement-to-test links. |
| `development/modules/core-game/GENESIS_RUNTIME_BUILD_ORDER.md` | One repository copy of this work order, reconciled with equivalent existing contract. |
| existing provenance decision area | One narrow source/dependency and implementation decision; not one new document per commit. |
| designated ignored build/distribution area | Generated AST/IR/bytecode, logs, test receipts, dependency working copies and ZIPs. |

### 3.1 Genesis source modules

Implement these responsibilities using actual supported Genesis syntax. Combine/split compilation units only when the real compiler/package model requires it; retain explicit traceability of responsibilities.

| Source file | Required behavior |
|---|---|
| `boot.gen` | Bind Fabric/profile definitions, instantiate the four domain identities, establish containment, bind Road interfaces, verify closure and emit boot receipt. |
| `sea.gen` | Validate instance scope, contain Shell, mediate admitted outer input/output, lifecycle participation. No application semantics. |
| `shell.gen` | Resolve declared command/observation exports, request authority, dispatch through Nexus, correlate results. |
| `nexus.gen` | Mediate read/proposed write; validate target/app scope; commit an admitted State successor or reject without mutation. |
| `state.gen` | Hold authoritative application organization, version/state root, application realization and application-scoped state transitions. |
| `road.gen` | Reusable wrappers/composition around upstream Corridor/Portal/Road primitives with adjacent routing, closure and History. No second bus. |
| `application_contract.gen` | Define admitted application exports, dependencies, state scope, operations and projections using the supported package/type/capability facilities. |
| `lifecycle.gen` | Quiesce, checkpoint/restore contract, close open work, stop/fault transitions without secretly implementing game rules in Python. |

Do not add a `.gen` file that is merely a label while its promised semantic operation is implemented only in new Python code. The dependency lock and operation trace must identify which Genesis module and which upstream runtime implementation carry each behavior.

### 3.2 Python implementation modules

Within the Hypervisor package, use clear modules with a small public API:

- `contracts.py`: immutable envelope/results/config types and explicit Horizon adapter protocol.
- `codec.py`: byte framing, serialization/deserialization, streaming input bounds.
- `validation.py`: envelope/body checks, field sizes, type checks; no gameplay validation.
- `session.py`: trusted bindings, authorization context association and reconnect lifecycle.
- `sync.py`: published/acknowledged projection revisions, retained delta replay and snapshot fallback.
- `delivery.py`: bounded inbound/outbound queues and cached outcomes for retries.
- `hypervisor.py`: compose lifecycle and one request-processing transaction; no game rules.
- `bridge.py`: native-embedding-facing bytes-in/bytes-out calls.
- `errors.py`: stable boundary errors and committed-versus-delivery status distinctions.

Avoid circular imports. Use a single place for protocol constants and schemas. A simple module may remain small; file count/LOC is not a completion target.

The Horizon Python binding package provides `toolchain.py`, `adapter.py`, and checkpoint/serialization helpers only to the extent required by the upstream facilities. Its type contracts must match the Hypervisor contracts without introducing a circular import. Prefer a tiny shared contract dependency owned by the Hypervisor distribution; the Horizon package may depend on it or implement structural protocols without importing it.

---

## 4. Upstream source map and compiler verification

### 4.1 Direct navigation

Read the paths in `SOURCE_MAP.json`, including:

```text
_bricked/genesis/registries/DOMAIN_REGISTRY.json
_bricked/genesis/registries/CROSSCUTTING_REGISTRY.json
_bricked/genesis/domains/{sea,shell,nexus,state}/MANIFEST.json
_bricked/genesis/systems/rainbow_road/README.md
_bricked/language/README.md
_bricked/language/20 GENESIS/05_LANGUAGE_SPEC/GENESIS_V1_0_LANGUAGE_SPEC.md
_bricked/language/20 GENESIS/01_RELEASE_FREEZE/GENESIS_V1_0_RELEASE_DESCRIPTOR.json
_bricked/language/20 GENESIS/04_CONFORMANCE/CONFORMANCE_RULES.md
```

Then inspect executable source, not just those documents:

```text
language/10 Genesis Surface Language/12_REFERENCE_IMPLEMENTATION/genesis_frontend/
  parser.py
  lower.py
  compiler.py
  __main__.py
  vendor/genesis_semantics/{checker,linker,capabilities}.py
  vendor/genesis_semantics/vendor/genesis_vm/{compiler,verifier,runtime,backend}.py

language/1 Packages/09_EMULATOR/genesis_chirality_machine/
  cell.py
  constants.py
  image.py

language/3 Transformation Engine & Geometry Forking/11_REFERENCE_IMPLEMENTATION/
  genesis_transform_engine/operators.py

language/17 System I-O & BLACKGLASS-BRANE Interface/12_REFERENCE_IMPLEMENTATION/
  genesis_system_io/{parser,compiler,verifier,runtime,brane}.py
```

Read the Sections 02, 04, 05 and 08–20 `00_START_HERE` records and follow their actual implementation/example/test pointers for capabilities used. Section 13 provides callable expansion; Sections 14–16 provide control/data, recursion and scheduling; Sections 17–19 provide explicit I/O/toolchain/bootstrap facilities. Reuse them where needed, not because a higher section number is automatically a replacement compiler.

### 4.2 Do not repeat the mixed-dialect error

The frozen **language release 1.0** is not a promise that every parser accepts the union of every source dialect. At the inspected revision:

- The Section 10 parser explicitly expects `genesis 0.1.0` and parses graph operations.
- The Section 17 parser parses its system-I/O declarations/operations separately. It is not an arbitrary graph-syntax superset merely because its example says `genesis 0.6.0`.
- Section 13 documents expansion from callable `0.2` source into `0.1` core, followed by the existing semantic checker/linker/GVM.

Keep graph programs and system-boundary programs in their supported compilation units. Determine the actual supported package/import/realization boundary from source and tests. Changing a header is not a composition mechanism.

### 4.3 Run the real baseline before custom code

Resolve `UPSTREAM` to the authorized pinned source and `BUILD` to an ignored `_raeon` output directory. The following command forms are supported by the inspected Section 10 CLI; recheck them if using another revision. These are commands to run, not pre-recorded passing results:

```sh
PYTHONPATH="$UPSTREAM/language/10 Genesis Surface Language/12_REFERENCE_IMPLEMENTATION" \
python -B -m genesis_frontend parse \
  "$UPSTREAM/language/10 Genesis Surface Language/16_EXAMPLES/RAINBOW_ROAD.gen"

PYTHONPATH="$UPSTREAM/language/10 Genesis Surface Language/12_REFERENCE_IMPLEMENTATION" \
python -B -m genesis_frontend lower \
  "$UPSTREAM/language/10 Genesis Surface Language/16_EXAMPLES/RAINBOW_ROAD.gen"

PYTHONPATH="$UPSTREAM/language/10 Genesis Surface Language/12_REFERENCE_IMPLEMENTATION" \
python -B -m genesis_frontend build \
  "$UPSTREAM/language/10 Genesis Surface Language/16_EXAMPLES/RAINBOW_ROAD.gen" \
  -o "$BUILD/upstream-rainbow-road.gvm"

PYTHONPATH="$UPSTREAM/language/10 Genesis Surface Language/12_REFERENCE_IMPLEMENTATION" \
python -B -m genesis_frontend run \
  "$UPSTREAM/language/10 Genesis Surface Language/16_EXAMPLES/RAINBOW_ROAD.gen"
```

Use isolated `PYTHONPATH`/processes per compiler family to avoid importing a same-named vendored package from the wrong section. Do not add all 20 implementation directories to one import path and hope resolution is correct.

The root language README also documents `python -B language/tools/run_tests.py` and its `--domain N` option, using Python 3.12. Run reused-domain regressions in an isolated writable dependency copy if the tests produce output. Historical `98_BUILD` scripts with absolute host paths are not portable build commands. Historical `99_RELEASE` files are source evidence, not tests run by this task.

**Baseline exit evidence:** successful source parse, semantic lowering/linking, verified bytecode, actual execution receipt, and actual source/runtime identity. If the baseline fails, preserve its exact command and error and fix environment/dependency issues before pretending custom Horizon source is valid.

### 4.4 Binding review: concrete traps to eliminate

Read the backing implementation for each primitive. At the inspected reference path, some operations are deliberately reference-level. In particular, examine how Fabric mounting, MMO lookup, `rel` targets, admission flags, `fork`, transformation and Road history are represented.

The Horizon must resolve an MMO/profile to actual supplied definition data, bind the Fabric to an actual image/store, resolve containment to actual existing domain identities, and evaluate actor/operation scope. A URI, arbitrary attribute or fabricated handle is not itself that binding.

A reference backend may be reused, but document exactly what it enforces. If an existing more complete upstream engine supplies missing semantics, bind it. If an adapter must resolve named profiles/targets, implement that adapter explicitly and test it. If a true semantic extension is needed, keep a named, versioned `_raeon` patch proposal with parser/checker/lowering/runtime tests; do not edit `_bricked` or claim it was in the frozen language.

---

## 5. Genesis Horizon: implement behavior, not labels

The operation names in this section are **semantic contracts/pseudocode names**, not invented Genesis syntax. Express them through the actual language. A compiler-supported callable/module boundary may use different names; record the mapping once.

### 5.1 Data and identity contracts

Maintain these concepts in the declared Genesis organization:

- `HorizonIdentity`: persistent identity of one contained machine instance.
- `DomainIdentity`: stable identity for each of sea, Shell, Nexus and State.
- `DomainVersion`: inherited successor/version, separate from persistent domain identity.
- `ApplicationIdentity`: admitted application instance within State, bound to package/content identity.
- `StateRoot`: authoritative current application/relationship root plus semantic revision.
- `RequestIdentity`: identity of one requested operation, separate from retries/delivery attempts.
- `ActorAuthority`: trusted scope over application, operation and allowed targets; never accepted solely from client claims.
- `ExecutionReceipt`: commit/rejection, source revision, resulting revision, identity/history references and transport-closure evidence.

Keep topological domain cardinality separate from the number of immutable versions/resources produced by the runtime. The same semantic domain may acquire new history without creating another parallel State domain.

### 5.2 `boot_horizon(profile, fabric_ref, instance_identity)`

**Inputs:** validated finite runtime profile, pinned Fabric source binding, explicit machine-instance identity. Required definitions are resolved before publication.

**Procedure:**

1. Validate the dependency lock and profile references. Reject missing/tampered definitions and unresolved MMO bindings.
2. Open the source Fabric read-only through the actual supplied image/store implementation. Establish a per-instance writable derived overlay using supported upstream facilities. Do not modify the source Fabric.
3. Instantiate one bounded domain Geometric for each of sea, Shell, Nexus and State. Do not obtain four domain labels simply by forking one anonymous Geometric and changing names.
4. Establish genuine containment/interface relations `sea contains Shell`, `Shell contains Nexus`, `Nexus contains State`. Resolve target identity and type, not just a string.
5. Bind the three adjacent bidirectional interfaces to the existing Rainbow Road/Corridor/Portal machinery. Establish declared direction, request scope, failure behavior and receipts.
6. Verify domain uniqueness, containment, Fabric binding, interface closure and absence of dangling imports/resources.
7. Publish the booted machine atomically with lifecycle `READY`, one authoritative State root and a boot receipt. A failure leaves no partially published ready machine.

**Outputs:** usable Horizon handle, immutable boot receipt, domain identity/version map, capability/projection declarations. No application is silently supplied by the Hypervisor.

**Tests:** four genuine domain identities; intact nested relations; distinguish two separately booted machines; deny duplicate publication within one machine; missing Fabric/MMO rejected; source bytes unchanged; no application/Road authority from metadata alone.

### 5.3 `realize_application(package_ref, authority)`

**Preconditions:** Horizon is READY; caller has application-realization authority; package references and exported contracts resolve against the selected toolchain; package content hash/version matches the supplied lock/manifest.

**Procedure:** verify package/capabilities; compile/link/verify required Genesis modules; allocate application-scoped Geometrics inside the existing State; bind declared operation/projection exports; construct an admitted successor State; commit only after closure and ownership checks. The application cannot replace sea, Shell, Nexus, Fabric or machine interface policy.

**Postconditions:** same four machine-domain identities; one newly admitted application identity and state scope; queryable declared operations; receipt with package hash and inherited State version. Repeating the same realization request is not a second application instance.

**Failure cases:** unresolved import, unsupported source dialect, wrong package digest, missing authority, illegal attempt to mutate a machine domain. All reject without installing partial application state.

A genuine loader/realizer is not assigning the string `RAEON` to a Python attribute. This runtime task must realize the small conformance application in section 10; full RAEON mechanics are not required here.

### 5.4 Shell request dispatch

Implement `dispatch(request, authority)` as the Horizon's semantic entry point, reached through sea. It must:

1. Resolve the addressed machine/application and the declared operation export.
2. Bind the request to trusted actor scope, expected State version if applicable, and execution budget.
3. Refuse unknown operations, undeclared effects, invalid target domains or mismatched applications.
4. Dispatch only through Nexus using the admitted Road interface; never directly call an application state-mutating host function as a shortcut.
5. Return a correlated receipt and permitted projection change. Do not export compiler traceback internals or arbitrary application memory to an ordinary player.

Commands are declared application operations. Never concatenate raw intent text into executable `.gen` source or invoke Python `eval`/`exec` on inbound payloads. Use supported typed binding/serialization for request values.

### 5.5 Nexus read, propose, commit

Implement three separate contracts even if a supported module combines them internally:

**`observe(scope, projection, authority)`** resolves the permitted State view through Nexus. It does not mutate application State or advance semantic State revision merely because a read occurred. Observation/audit history may record the read separately.

**`propose(operation, state_version, authority, budget)`** applies an admitted operation to a candidate/derived State using supported transformation/overlay/continuation facilities. It checks current ownership, capability scope and expected version. It may not mutate live State during validation.

**`commit(candidate, proof_receipts)`** verifies final closure and atomically publishes the successor State plus its operation receipt. Failed source/capability/closure checks leave the previous application State root unchanged. Store/associate the successful request identity and result with the committed successor so a retry cannot duplicate a transition.

If the upstream runtime lacks a single transaction call, compose its supported immutable successor/overlay publication operations. Document and test the actual commit point. A Python `try/except` after mutating live dictionaries is not rollback.

**Critical commit/delivery distinction:** once State committed, a later output failure does not mean the action was rejected. Recover/re-deliver the committed result; do not repeat the mutation.

### 5.6 State application environment

State owns the application's objects and relationships, the authoritative semantic revision, and immutable version/history links. Maintain the same instance across multiple user operations. Do not create a fresh `VM().run()` with unrelated state for every request and call that a persistent game.

Use the upstream supported runtime continuation/store/import mechanism. If host orchestration invokes compiled handlers separately, it must bind the same admissible persistent resources and demonstrate identity/history continuity. Do not use an untracked host-only dictionary as a substitute for Genesis application State.

A state-changing accepted operation advances semantic revision exactly once. Rejected operations do not advance it. A no-op observation or a retry of a prior request does not advance it. An accepted operation whose semantic effect is intentionally a no-op must have a declared revision policy tested separately.

### 5.7 Rainbow Road implementation

Use the upstream Road implementation, not a list of labels named `Road` or an ordinary message queue renamed `Rainbow Road`.

For each required traversal:

1. Resolve permitted source/destination endpoints and their adjacent interface.
2. Obtain admissibility/authority evidence for the actual transported object/request; a declaration alone cannot grant authority.
3. Open the typed Portal over its admitted Corridor.
4. Transport the request/readout organization while preserving stable semantic identity and required ancestry according to the source contract.
5. Close the Portal with its destination witness and receipt.
6. Append the receipt to the persistent ordered Road history and close the completed traversal when required by the upstream ownership contract.

Trace inward and outward legs. Assert that the authoritative State remains at its domain location. Test a forged direct sea-to-State jump and a Portal left open. Cancellation, rejected steps and budget faults must have explicit failure/closure behavior and must not publish a partial application mutation.

Do not require every game-local object relation to pass through all four domains. The full adjacent path is mandatory for the external request/readout interaction; application-local transport follows the admitted upstream rules within State.

### 5.8 Lifecycle and persistence

Internal lifecycle is `CREATED -> BOOTING -> READY -> QUIESCING -> STOPPED`, with `FAULTED` on unrecoverable runtime failure. These are implementation states, not new Genesis dimensions or gameplay phases.

- `QUIESCING` stops admission of new state-changing requests and handles pending requests deterministically.
- A normal stop closes resources, persists the chosen checkpoint where requested, and emits a stop receipt.
- A budget/capability/validation failure is not automatically a machine-wide fault; reject the operation when isolation/rollback is intact.
- An unknown commit state, invalid persisted root or broken runtime invariant faults the affected instance and prevents unverified further writes.
- `checkpoint()` runs at a quiescent transaction boundary. It preserves application/domain identities, State root/version, source/bytecode identities, overlays/continuations and required History. It is not merely the player render snapshot.
- `restore()` verifies dependency/profile/schema/hash compatibility and restores into an unpublished candidate. A failed restore does not replace the live instance. Publish only after invariants hold.
- A restore starts a new boundary epoch; old pending client assumptions cannot be replayed blindly against a rewound state.
- `replay()` executes recorded semantic inputs against the same package/seed/initial snapshot and verifies resulting state roots and receipts. Host timestamps and transport message IDs are outside semantic determinism.

Use the actual upstream persistence/continuation facilities and identify their coverage. If a true backend limitation prevents a promised checkpoint/continuation behavior, preserve the failing case and label that part incomplete rather than exporting a fake save file.

---

## 6. Python boundary: exact public contracts

These are Python-side **implementation interfaces to create**, not claims about existing upstream APIs. Adapt the actual runtime behind them; do not modify the frozen language to match their spelling.

### 6.1 Horizon adapter protocol

Expose a typed interface with these behaviors:

```text
boot(profile, trusted_context, budget) -> BootReceipt
realize_application(package_ref, authority, budget) -> ApplicationReceipt
observe(view_context, projection_cursor) -> AuthorizedProjection
execute(intent, authority, budget) -> TransitionOutcome
lookup_outcome(operation_key) -> RecordedOutcome | NotRecorded
checkpoint(authority) -> CheckpointRef
restore(checkpoint_ref, authority, budget) -> RestoreReceipt
quiesce(budget) -> QuiesceReceipt
close() -> CloseReceipt
```

`AuthorizedProjection` contains only data the Horizon permitted for that view. `TransitionOutcome` distinguishes rejected, committed, and fault/unknown-result outcomes. It carries the request/commit identity, semantic revision change, authorized view deltas and required receipts. The Hypervisor must not infer accepted state from an exception or from the presence of a field called `success`.

The adapter invokes compiled Genesis and the real supplied runtime. A fake implementation is useful in isolated unit tests, but it cannot satisfy integration acceptance.

### 6.2 Hypervisor native-embedding API

Implement this small byte-facing bridge or an equivalent existing API with the same semantics:

```text
open(horizon_adapter, config) -> HypervisorHandle
bind_session(trusted_session_context) -> SessionHandle
receive(session_handle, frame_bytes) -> IngressResult
step(execution_budget) -> StepResult
drain(session_handle, max_frames, max_bytes) -> tuple[bytes, ...]
close_session(session_handle) -> SessionCloseResult
save_checkpoint(trusted_authority) -> CheckpointRef
restore_checkpoint(checkpoint_ref, trusted_authority) -> RestoreReceipt
close(mode, execution_budget) -> CloseResult
```

`receive()` validates/bounds and queues data; it does not run unbounded compilation or secretly mutate State. `step()` performs bounded work under one serialized semantic execution owner. `drain()` removes only deliverable frames; it never interprets game rules. The native Port can invoke these functions after hosting the Python runtime. Do not build a network server or require native SDKs for this task.

Caller-supplied raw session IDs are not authentication. `bind_session()` receives trusted actor/application/view authority from the owning application, not from an arbitrary inbound JSON field. Bind each transport handle to that authority. The schema need not carry secrets.

### 6.3 Processing algorithm

```text
ON receive(handle, bytes):
    validate transport handle and finite input limits
    decode one supported frame/envelope or buffer a bounded partial frame
    reject malformed schema/direction/version before any Horizon execution
    associate trusted actor/application/view from handle
    enqueue or return backpressure without side effects

ON step(budget):
    take next bounded request in deterministic accepted order
    validate request identity / retry / authority / projection preconditions
    return recorded outcome for an identical prior request
    reject reuse of request identity with different content
    reserve outcome-delivery capacity before executing a fresh mutation
    dispatch through real Horizon adapter
    record the actual committed/rejected outcome
    queue correlated receipt and authorized projection updates
    if output delivery fails after commit: retain/recover committed outcome

ON drain(handle):
    return bounded queued frames in declared order
    retain required replay/outcome records until acknowledged or safely expired
```

Never report `accepted=false` merely because a port failed after the Horizon committed. Never globally deduplicate by message ID without actor/application scope. Never allow two simultaneous retries to bypass deduplication and both execute.

### 6.4 No RAEON semantics in the fence

The Hypervisor may inspect declared envelope fields, limits and trusted binding. It may not calculate FG closure, Prime H/C, field color, legal targets, ACTIVE/DEFENSE permissions, or which player owns a card. Those are Horizon/application decisions. It may reject an unbound session before reaching those decisions.

---

## 7. Byte protocol, validation and synchronization

### 7.1 Engineering default and compatibility

First check whether the active `_raeon` task already has an approved boundary protocol. Reuse it if it satisfies this work order. Otherwise implement the following **new internal Hypervisor wire profile v2**; it is not presented as existing Genesis syntax or an upstream ABI.

Use a documented binary frame carrying strict UTF-8 JSON. This makes cross-language inspection straightforward while preserving a byte interface. No pickle, Python object references, native pointers, or arbitrary code serialization.

Default frame, network byte order:

| Field | Bytes | Meaning |
|---|---:|---|
| Magic | 8 | ASCII `RAEONH2!` |
| Major | 1 | `2` |
| Minor | 1 | `0` |
| Flags | 2 | `0`; reject unknown flags |
| Payload length | 4 | Length of encoded JSON only |
| CRC32 | 4 | Checksum of JSON bytes |
| Payload | declared length | Valid UTF-8 JSON envelope |

Header format is `>8sBBHII`, 20 bytes. A checksum detects accidental corruption; it is not authentication. An in-process bridge does not require an internet listener. No unauthenticated listener is to be opened by default.

Old handoff archives used different magic/fields and unreliable contracts. Do not pretend wire compatibility. Keep a compatibility adapter only if there is a real consumer to preserve and it has tests; otherwise report that profile v2 replaces the unverified prototypes.

### 7.2 Envelope and message families

Required envelope fields: `schema_version`, `kind`, `message_id`, `application_id`, `epoch`, and `payload`. Response `correlation_id` identifies the triggering request. `commit_id` identifies an authoritative committed transition, not a transport packet. IDs are opaque nonempty bounded strings, never memory addresses.

Incoming families: `HELLO`, `INTENT`, `SYNC_REQUEST`, `ACK`, `HEARTBEAT`.
Outgoing families: `WELCOME`, `SNAPSHOT`, `DELTA`, `RECEIPT`, `EVENT`, `ERROR`, `HEARTBEAT_ACK`.

`INTENT` body includes a declared operation name, typed arguments, stable request identity and any required view/object preconditions. It does not carry an authoritative replacement State or permission grant.

`SNAPSHOT` body contains the authorized view, `view_id`, epoch, projection revision and content digest. `DELTA` includes `view_id`, epoch, `base_revision`, `revision`, commit identity and changes. Deltas patch the projection, never the internal VM memory layout.

`RECEIPT` distinguishes `REJECTED`, `COMMITTED`, `OBSERVED` and `FAULTED_OR_UNKNOWN`. A duplicate of a committed request returns its recorded committed result rather than claiming it never happened. Ordinary errors expose stable codes and safe context; diagnostic tracebacks remain in controlled diagnostics.

### 7.3 Strict validation

Validate encode and decode paths, not only inbound JSON. Reject:

- unsupported major version/flags; unknown direction/kind; inconsistent header/envelope version;
- truncated/oversized frame; unexpected trailing bytes in a single-frame API; corrupt checksum;
- invalid UTF-8/JSON, duplicate JSON keys, NaN/Infinity, non-object payload, unknown required enum;
- booleans where an integer is required; negative revisions; IDs outside size/character rules;
- undeclared top-level fields unless a documented optional extension namespace permits them;
- session/application/epoch mismatch and client attempts to select another trusted actor;
- shape-invalid operation args according to the declared boundary schema, while leaving gameplay validity to the application.

Make numeric cross-language behavior explicit. Encode unbounded counters as decimal strings, or constrain integer JSON fields to the interoperable exact range in the schema. Do not silently coerce malformed types. Frame/body sizes and recursion depth are bounded before expensive work.

### 7.4 Revision and reconnect algorithm

Maintain **three different concepts**:

1. Horizon semantic revision/state root: owned by the Horizon.
2. Per-view projection revision: identifies exactly what a particular Port may see.
3. Delivery sequence/acknowledgment: describes transport, not gameplay mutation.

A receipt does not by itself update the platform projection. Do not compare incoming preconditions against a stale Hypervisor clock that never incorporated the latest committed result.

- Initial connection establishes a supported protocol and fresh trusted session, then an authorized snapshot.
- A delta applies only to the matching view/epoch and exact base revision; reject/request resynchronization otherwise.
- On reconnect, replay a contiguous retained sequence where available; otherwise request a fresh authorized snapshot from the Horizon. Do not reconstruct hidden state in the fence.
- A stale read may receive an updated snapshot. A stale state-changing intent is rejected or revalidated by the declared Horizon precondition policy; never silently apply it to another State.
- Authority/view changes invalidate old projections and require a snapshot. A new checkpoint restore changes the epoch.
- Hidden-state-only changes must not leak hidden data or an internal checkpoint. The view/revision exposure policy belongs to the Horizon, not to raw global memory revision publication.

### 7.5 Retry and delivery guarantees

Use `(application_instance, trusted_actor, request_identity)` plus canonical request digest as the logical operation key; bind it to session/view authorization on response delivery. Identical retransmission returns the saved outcome. Same identity with different intent content returns `REQUEST_ID_CONFLICT` before execution.

Coordinate the committed operation record with Horizon State commit or a recoverable authoritative journal. A volatile 4096-entry set cannot prove exactly-once execution across restart. Bound retention and explicitly reject an expired retry token rather than silently treating it as a new mutation. Pending and committed states must be recoverable or reported as unknown without repeating an unsafe operation.

Promise only the tested retry scope: in-process, reconnect, and restart behavior must each be named and demonstrated. If durable recovery is not supported by the selected runtime, state that limitation and do not call the persistence acceptance complete.

### 7.6 Bounded operation and resource policy

Select finite, configurable engineering defaults and put them in one configuration source. Initial defaults for the host-reference profile:

- payload limit: 1 MiB;
- pending incoming messages: 256 per trusted session;
- outbound queued bytes: 8 MiB per session;
- retained outcome entries: 4096, with explicit expiry/retry policy;
- default GVM instruction budget: 100,000 steps per admitted request where supported;
- diagnostic and replay storage limits: explicitly configured, never unbounded by accident.

These are engineering defaults, not game rules or measured mobile performance claims. Reject oversized views with an explicit error, or implement and test chunked snapshots. Never truncate silently. Backpressure must occur before accepting work that cannot retain its commit outcome. Queue exhaustion must not lose a Geometric or duplicate a committed action.

Use supported cooperative runtime budgets. Do not claim a Python thread timeout forcibly stops arbitrary native/untrusted code or creates security isolation. Trusted bundled app execution with controlled interfaces is the default deployment model here.

---

## 8. Dependency lock and build artifacts

Implement a lock containing actual values discovered by the build, not placeholders presented as a resolved dependency:

```text
schema_version
upstream_repository
upstream_commit
upstream_release_descriptor_hash
selected_source_paths_and_hashes
source_dialect -> compiler_entry_point -> IR -> verifier -> runtime/backend
required_runtime_data -> actual local/cache path -> content hash
upstream_notices/licenses
local_compatibility_patches -> scope/version/hash/tests
Python/toolchain requirements
Horizon profile/schema versions
build-artifact hashes
```

Keep absolute developer-machine paths out of the tracked lock. Resolve local locations through environment/config at runtime. Never modify global Python import configuration or silently select whatever version happens to be installed.

The lock records a capability binding matrix: Fabric, domain realization, relations, admission, immutable transforms, Portal, Road, application realization, dispatch, persistence. Each entry identifies the exact upstream function/module or local Genesis module that implements it, the scope it guarantees, and the executing test. A human name such as `@genesis_sea_singleton` is not enough.

Generated artifacts must include source hashes, lowered IR, compiler/linker/checker receipts, bytecode/disassembly where provided, and execution receipts. Store them in ignored build output or approved release artifacts. Stable required test vectors may be tracked under tests; avoid dumping every transient debug run into Git.

When upstream uses reference host registers or storage, describe them as its implementation backend. Do not promote host projection details into Genesis-native ontology. Conversely, do not hide the fact that an actual host/reference implementation is used.

---

## 9. Ownership, projection and fault rules

These rules are completion requirements because the earlier prototypes did not establish them:

**Ownership:** Domain identities belong to the Horizon; application Geometrics belong to the admitted State organization; session authority is granted by the owning application/Horizon; view state belongs to a permitted projection; transport buffers belong to the Hypervisor. Native ports own their local presentation only.

**No direct state setter:** The public Hypervisor has no API accepting a Python dict that overwrites authoritative game State. Checkpoint restoration is a separately privileged operation verified by the Horizon.

**No projection aliasing:** Outbound DTOs/serialized data cannot alias mutable live runtime data. Mutating a local copy in a Port or test does not change authoritative State. Deep copy or immutable conversion must occur at the declared projection boundary.

**Errors:** distinguish `MALFORMED_FRAME`, `UNSUPPORTED_VERSION`, `UNBOUND_SESSION`, `AUTHORITY_DENIED`, `UNKNOWN_APPLICATION`, `UNKNOWN_OPERATION`, `STALE_PRECONDITION`, `INVALID_ROUTE`, `ADMISSION_REJECTED`, `CLOSURE_FAILED`, `BUDGET_EXCEEDED`, `REQUEST_ID_CONFLICT`, `RETRY_EXPIRED`, `BACKPRESSURE`, `COMMITTED_DELIVERY_PENDING`, and `RUNTIME_FAULT`. Stable error-code spelling is a new fence contract, not an upstream Genesis language claim; preserve equivalent existing approved codes if present.

**No broad exception fiction:** Catch and classify known failures. Unexpected exceptions fault the correct scope and preserve diagnostics. Do not swallow them and return a generic `accepted=false` that implies rollback occurred.

**Persistence:** source authority is read-only, derived state is writable, and receipts/history are append-preserving according to upstream contracts. File/object paths are validated against configured storage capabilities. No traversal outside the allowed build/checkpoint root.

---

## 10. Required real integration scenario

Implement an executable test/demonstration named `test_real_horizon_roundtrip` and a headless demo command. This scenario is the minimum functional proof, not the whole test suite and not a substitute for lifecycle/error work.

### 10.1 Conformance application

Create a real Genesis application with two distinct, supplied profile/MMO-backed Geometrics `A` and `B` inside State. Its authorized fixture actor can observe them, add a declared relationship between them, and execute a supported identity/history-preserving transformation. A different fixture actor has observation-only authority. The fixture is clearly test-only; its privileges are not exposed as production defaults.

Use actual upstream instance/profile data. For a cell-level change, prefer the supplied `MIRROR_CHIRALITY` operator and its actual Fabric-backed realization when the selected compiler/backend supports that path; read initial/expected patterns from the pinned upstream definitions. Do not fake a field change by incrementing a `PING` counter. If another supported native operator is used, name it and test its real effect and history explicitly.

Suggested fixture operation names `OBSERVE`, `RELATE_A_B`, and `TRANSFORM_A` are application intent vocabulary, not new Genesis keywords. Their handlers are compiled `.gen` modules/callables.

### 10.2 Exact successful trace

1. Start a fresh Horizon from the locked Fabric/profile. Record four distinct persistent domain identities, their live nesting and a closed boot receipt.
2. Realize the conformance application into the existing State. Record application identity and semantic revision `r0`.
3. Open the real Hypervisor with the real Horizon adapter. Bind a trusted fixture session and negotiate the byte protocol through the headless Port.
4. Obtain a snapshot. Decode it using the Port's independent decoder; verify that the authorized view contains A/B, not the entire backend's private state.
5. Submit a framed `RELATE_A_B` intent with request identity `q1` and the declared revision precondition.
6. Inspect actual Road/Portal receipts: inward interface sequence is sea -> Shell -> Nexus -> State. No direct jump occurs; machine-domain identities remain in place.
7. Execute the compiled Genesis handler, admit/commit the relationship and publish State revision `r1 = r0 + 1`.
8. Inspect actual outward traversal and encoded receipt/delta. Decode/apply the delta to the Port's prior snapshot. The resulting projection equals a new authorized Horizon snapshot at the same revision.
9. Submit `TRANSFORM_A` with fresh request identity. Verify a real declared native transformation and preserved semantic identity/ancestry, rather than only the presence of a keyword in source.
10. Keep using the same running application instance for additional operations. Domain identities do not reset or multiply.

### 10.3 Exact rejected/retried trace

- Resend `q1` with the identical operation: same recorded outcome, no second relationship and no extra semantic revision.
- Resend `q1` with changed arguments: `REQUEST_ID_CONFLICT`, no change.
- Submit the mutation from the observation-only actor: `AUTHORITY_DENIED`, application State root unchanged.
- Request a direct sea->State bypass: rejected by the actual route/admission path, State unchanged.
- Force a failure after a candidate transformation but before commit: no partial authoritative state.
- Force delivery failure after commit: the next recovery/retry returns the committed result without applying it again.
- Send a stale/gapped projection cursor: recover with valid contiguous deltas or a fresh authorized snapshot; no silent application of a stale delta.
- Quiesce, checkpoint, close, restore and observe: identities, semantic state and declared history persist. Old-epoch requests cannot modify the restored instance.

### 10.4 Independent evidence

The Port decoder must not simply call the Hypervisor's decoder and declare cross-language compatibility established. Use a separately implemented reference decoder or fixed normative byte vectors, plus schema/endianness/length assertions. This verifies the byte contract in the available host environment; it is not a substitute for later Swift/Kotlin/C++ SDK tests.

Track authoritative application State root separately from audit history. A rejected operation may produce a rejection receipt; the fact that the audit ledger grew does not mean application State changed.

---

## 11. Required acceptance cases

`ACCEPTANCE_CASES.json` contains concrete positive and negative cases with input/action/expected evidence. They are specifications only and begin `NOT_RUN`. Import or map them to actual tests. Do not build a runner that marks them passed by checking a label or reading a prewritten status.

Coverage categories:

- source access/lock and actual language entry-point verification;
- genuine domain instantiation, containment, identity continuity and read-only Fabric;
- supported application realization and State scope;
- real Portal/Road transport, authorization and closure;
- immutable transaction/candidate publication and commit-versus-delivery failure;
- framing/schema validation in both directions;
- trusted session isolation, projection privacy and no mutable aliasing;
- retries, stale revisions, reconnect and epoch changes;
- budgets, queue backpressure, quiesce/stop/fault and persistence;
- build reproduction and two clean-extraction distributions.

A failing negative test is evidence of an implementation defect, not permission to weaken the rule. An upstream regression that fails before local changes is recorded separately from a local regression. Preserve the failure and exact environment; fix in-scope integration without silently changing upstream authority.

The `_raeon` sixteen-gate development pipeline still applies. Map this work into its current module records. Source/implementation completion does not automatically mean performance acceptance, native-device validation, whole-game GOLD, or approved release. Where device SDKs/hardware are unavailable, report `NOT_RUN`, not `PASS` or an invented performance result.

---

## 12. Implement these commands

Create `tools/genesis_runtime.py` as a thin command orchestrator over real compiler/runtime/package functions. These commands are **required future entry points to implement**, not commands already available at handoff time:

```sh
python -B tools/genesis_runtime.py doctor
python -B tools/genesis_runtime.py dependencies verify
python -B tools/genesis_runtime.py upstream-test
python -B tools/genesis_runtime.py build
python -B tools/genesis_runtime.py verify
python -B tools/genesis_runtime.py demo --headless
python -B tools/genesis_runtime.py test
python -B tools/genesis_runtime.py package
python -B tools/genesis_runtime.py verify-distributions
```

**`doctor`** reports actual Python/compiler/backend versions, repository paths/revisions, missing dependencies and source availability. It must not manufacture an environment or silently treat a pointer as source.

**`dependencies verify`** checks all required local pinned source/data hashes and notices. Implement an explicit reproducible dependency-resolution/setup procedure if absent. Downloads use existing authorized access and write only to the configured dependency cache; execution can then run offline.

**`upstream-test`** invokes reused-domain regressions in isolation and records exact commands/results. Do not run all unrelated physical/research tests to block an otherwise bounded integration unnecessarily.

**`build`** compiles every distributed Genesis module with the correct dialect entry point, links supported composition boundaries, verifies actual bytecode and emits build/IR/receipt artifacts. Any compile/check error exits nonzero.

**`verify`** validates the emitted artifacts, required resources, dependency lock and explicit local runtime invariants. No source-string-only conformance gate.

**`demo --headless`** performs section 10 end to end and emits a readable trace plus machine-readable evidence. It exits nonzero if the real adapter, Road path, State change, identity continuity or byte round trip is missing.

**`test`** runs actual local unit/integration/negative tests and relevant upstream regressions; it reports collected/passed/failed/skipped and the reason for every skip. Required tests skipped due to missing runtime are not green completion.

**`package`** builds two archives from one identified clean source revision and a verified lock. Refuse a release-labelled package when required local tests fail or source/digest drift exists. A clearly named diagnostic/WIP package may be generated separately without a false release label.

**`verify-distributions`** extracts both archives to fresh paths, checks exact manifests, resolves their declared dependency layout without accidental developer checkout imports, and runs installation/import plus the real joint headless demonstration. Test a path containing spaces. This is required before delivery.

Existing repository validators remain authoritative for hygiene. At the inspected `_raeon` baseline they include the following; re-read current README and preserve newer commands:

```sh
node tools/validators/validate-bootstrap.mjs
node tools/validators/validate-design-state.mjs
node tools/validators/validate-normalization.mjs
node tools/validators/validate-continuity.mjs
node tools/validators/validate-cycle1-import.mjs
node tools/validators/validate-full-migration.mjs
node --test tests/regression/*.test.mjs
git diff --check
```

Do not weaken structural validators to hide duplicate trees or preserved-source modifications. Amend a validator only when an authorized source/schema change requires it, with positive and negative regression tests.

---

## 13. Work queue — perform the build in these units

Each unit has input, code output and executable exit evidence. The queue is not a request to stop after each unit. The agent may work in bounded internal chunks and commit coherent progress, but should continue without repeated director approval.

### W00 · Recover existing work and select paths

**Read:** current worktree, active execution record, applicable repository instructions, this order.
**Do:** recover interrupted files and task commits; map section 3 to established implementation locations; verify sole write scope; capture actual starting status without discarding work.
**Write:** one execution record plus a short pointer in applicable `_raeon` AGENTS instructions if missing.
**Exit:** known source locations, pinned/current task commit, no duplicate implementation roots, no upstream writes.

### W01 · Prove the upstream toolchain and lock dependencies

**Read:** source map, release/dialect records, actual parser/compiler/linker/verifier/runtime sources and examples.
**Do:** retrieve required source bytes; run section 4 baseline; exercise actual selected callable/control/system composition boundaries as needed; run relevant upstream regressions.
**Write:** dependency lock, implemented dependency checks and baseline receipt in build evidence.
**Exit:** actual example compiles/verifies/runs; supported dialect matrix resolved. No custom Horizon syntax before this passes.

### W02 · Bind Fabric, domain profiles and real identities

**Read:** instantiation, Fabric image/cell, Geometric and domain definitions; upstream realization tests.
**Do:** supply/resolve all required profiles/MMOs; implement read-only base with per-instance derived state; bind actual IDs and containment target resolution.
**Write:** profile data, necessary documented adapter bindings and initial Genesis boot definitions.
**Exit:** domain data resolves, missing/tampered definitions reject, source unchanged, duplicate instances rejected by actual behavior.

### W03 · Implement the four-domain Genesis boot

**Read:** W02 bindings and supported module/callable semantics.
**Do:** implement boot/sea/Shell/Nexus/State Genesis responsibilities; establish real nesting and closure; publish READY atomically.
**Write:** compiled source plus boot/rejection tests and receipts.
**Exit:** one of each domain with persistent identities, no peer/pipeline substitute, no partially READY boot.

### W04 · Implement admitted Rainbow Road traversal

**Read:** upstream Portal/Corridor/Road code and closure/ownership tests.
**Do:** wire all adjacent inbound/outbound interfaces with request/readout transport; preserve ordered History; reject direct jumps, wrong authority, unclosed/invalid traversal.
**Write:** `road.gen`, interface bindings and real behavioral tests.
**Exit:** actual six-direction traversal evidence and negative rejection without application mutation; State does not relocate into the outer domain.

### W05 · Implement State application realization and transactions

**Read:** supported application/package/continuation/data/control facilities.
**Do:** implement realization/dispatch/Nexus candidate-commit operations; state persistence across commands; the real conformance application's relationship/transformation handlers.
**Write:** application contract, state/dispatch source, conformance app and failure-injection tests.
**Exit:** actual Genesis operations work in one persistent State; denied capability/route/stale request cannot partially mutate it.

### W06 · Implement the Hypervisor library and byte bridge

**Read:** sections 6–9 and any existing approved fence protocol.
**Do:** implement typed adapter contract, binary codec/schema, validated ingress, trusted sessions, bounded buffers, public native-embedding calls and structured errors.
**Write:** installable Python package, schema, independent wire vectors and unit tests.
**Exit:** codec/direction/type/limits/session tests pass. Mock Horizon tests remain labelled unit-only; this unit alone does not complete the fence.

### W07 · Connect the fence to the real Horizon

**Read:** actual runtime outputs, W05 handlers and W06 contracts.
**Do:** implement the real adapter; dispatch framed intentions into compiled Genesis; return real correlated receipts and authorized snapshots/deltas. No PING-only fake in integration.
**Write:** joint headless fixture/Port decoder, real adapter, projection mappings.
**Exit:** section 10 successful trace passes through all three architectural objects in both directions.

### W08 · Implement retry, revision, delivery and reconnect semantics

**Read:** actual commit boundary and projection contract.
**Do:** implement scoped operation records, ID-content conflict checks, contiguous delta handling/snapshot recovery, epoch isolation, and post-commit delivery recovery.
**Write:** sync/delivery logic, concurrent-duplicate and injected-failure tests.
**Exit:** repeated/cross-session/stale requests cannot duplicate or misreport mutation; reconstructed Port projection matches authorized State.

### W09 · Implement lifecycle, budgets, checkpoint and replay

**Read:** supported runtime continuation/storage/scheduling facilities.
**Do:** quiesce, bound work, checkpoint/restore identity/history, close resources, fault affected scopes and reproduce recorded semantic transitions.
**Write:** lifecycle Genesis source and Python coordination, bounded-run tests, restart/replay tests.
**Exit:** actual repeated operation/stop/restore/replay chain, unchanged source data and declared resource behavior.

### W10 · Run full acceptance and repository regression

**Read:** acceptance-case mapping and previous baseline failures.
**Do:** run every required case, independent byte checks and fault injection; correct implementation failures; run repository validators and relevant upstream regressions; measure host-reference behavior without inventing device performance.
**Write:** machine-readable test receipt, exact commands and narrowly scoped limitations.
**Exit:** required local software acceptance passes. Any real unsupported requirement remains explicit, with implementation progress saved and exact failing evidence.

### W11 · Package, verify extraction and persist delivery

**Read:** verified source/lock and approved distribution conventions.
**Do:** package two distributions, verify both from clean extraction, commit maintained source/tests/lock/docs, push when authorized, report commit and remote status.
**Write:** two ignored/release ZIPs, exact manifests/digests and final execution record.
**Exit:** reproducible source-backed distributions; no cache files/missing manifest entries; no false main-merge or device-release claim.

---

## 14. Distribution contents and handoff to native ports

Implement one packaging command producing:

**`raeon-python-hypervisor-<version>.zip`** — library source, install metadata, schemas, public byte-bridge documentation, tests/wire vectors, exact dependency requirements, build/test receipts and manifest. No game rules, no bundled native application, no secret credentials.

**`genesis-horizon-<version>.zip`** — real Genesis source modules, all required Horizon profiles/definitions, locked reference-runtime/compiler subset or a reproducible resolved dependency mechanism, bytecode/IR/receipts appropriate to distribution, actual Horizon adapter, conformance application, tests, lifecycle/deployment instructions and manifest.

Preferred distribution policy for this task: vendor the exact required source/runtime subset in the Horizon distribution when permitted, retaining origin/version/hashes/notices; do not copy the whole multi-gigabyte archive as padding. Otherwise supply a pinned resolver with precise access requirements and test the declared setup. The archive must state whether it is offline self-contained. Never call a dependency-only archive self-contained.

Package sources deterministically where practical: stable path order, newline policy, fixed build inputs, no absolute machine paths in semantic receipts, optional normalized ZIP timestamps. Remove caches/temporary files **before** calculating inventory hashes. Manifest includes every shipped file except itself; no listed file may be absent. A sidecar records the final archive hash to avoid a self-referential checksum.

The two archives must work together after clean extraction. Native SDK integration remains later. Describe how an embedded host would initialize the library and exchange bytes; do not claim Swift directly executes Python, the package supplies an iOS interpreter, or a Python class boundary alone isolates hostile code.

---

## 15. Preserve RAEON design; do not expand this runtime task into redesign

Use the newest Codex-reconciled `_raeon` design/data. The following protects thread continuity:

- Primitive object GEOMETRIC. Card copies keep runtime identity while immutable QMO definitions remain separate.
- BOARD has Deck, Hand, Graveyard, fixed Prime positions and a Configuration Space region. Typed attachments are not the containers themselves.
- Deck/Hand/Graveyard contain CARD Geometrics only. Current deck construction is 60 cards; Hand capacity seven. Ordered deck/graveyard, shuffle/access policy and admitted identity-preserving transfers remain in application rules.
- Cycle 1: 120 FG + 14 ordinary Prime + 51 ordinary Utility = 185 ordinary identities; 2/3/unique respective copy limits. Preserve source catalogs byte-for-byte.
- Three permanent universal starting Configuration Spaces A/B/C; nine is the accepted expansion cap, not a one-per-Utility-color rule. Merge can reduce independently operating spaces; do not restore an unconditional three-independent-active-spaces assertion.
- Configuration Space is a persistent live workspace outside the finite QMO corpus. It accepts QMO-backed FGs. No Configuration Frontier object.
- Both required FG membership and admitted XY arrangement/3D orientation must match before activation. No field by count alone. Source/runtime mapping gaps are not `TERMINATES` or permission.
- Valid ordinary 3/4/5/6/7/8-FG closure maps to R/O/Y/G/B/V. Atlas: 60 base + 343 fusion-derived + 1,691 emergent = 2,094 field/manifold QMOs, separate from the FG catalog.
- Individual committed FGs do not freely migrate between spaces; whole-space merge preserves their identities. Link/emergence preserves supports, consumes no new space and permits multiple admitted pairwise emergents. Emergent fields are not directly targetable and are support-dependent.
- Native topology/max color is separate from mutable field output. Field destruction routes supporting FG cards to Graveyard. Prime health zero instead makes the same fixed-slot Prime INACTIVE.
- Prime rank r defines Hmax=Cmax=r; normal start H=r,C=0; restoration fills H before C; degradation consumes C before H. Full H and positive C are required to spend. Charge is both resource and shield; partial/repeated spending allowed. White Restore Prime gives (1,0), not full health/charge.
- Ordinary fields are READY/USED once per refresh cycle; use persists into defense. Color enters the owner's Prime system before hostile action. ACTIVE permits Restore/Degrade; DEFENSE permits friendly Restore only, including Universal's Restore direction.
- Rainbow Road is the only native transport. No extra board color bus, independent Boundary API object, or new game mechanics.

Refresh boundary, defensive response order, overflow, setup/victory/timing, some merged-space accounting and emergent production cadence may remain unresolved unless newer accepted work closes them. They do not block implementing the reusable runtime with a conformance application. Do not invent those rules to make a test pass.

---

## 16. Recovery, progress reporting and completion decision

Maintain one execution record containing:

```text
Current work unit and next exact action
Current local commit and last successfully pushed commit
Actual implementation path map
Upstream source/dialect/runtime lock location
Requirement -> source/module -> real test mapping
Commands run, exit codes and concise results
Known upstream baseline failures versus local failures
Remaining blockers and smallest executable reproduction
Distribution paths/hashes when actually built
```

Keep AGENTS instructions short: point to this contract and execution record, name build/test entry points once implemented, and preserve existing repository rules. Do not paste this entire document into every module or create a new checkpoint file for each sentence.

On interruption, resume from actual Git state and the last failing command. Do not re-run the whole architecture workshop or rename the same scaffold as a higher version. Continue ordinary coding and testing without requiring the director to say “audit” again.

Before final report, review staged files, `git diff --check`, tests, the upstream read-only hash baseline, and clean-extraction results. Ensure no other task's work was discarded.

Report: implementation locations; commit and push status; pinned sources/toolchain; actual build/run/test commands; real integration evidence; limitations; two distribution locations/sizes/hashes. Do not say finished based on architecture prose, keyword checks, number of files, archive size or unit tests against only a fake adapter.

**Completion is a scoped software result:** the two operational components, their actual integration and their declared recovery/delivery behavior pass the required local tests. Native-device certification/performance and whole-game release remain separate pipeline gates. If a promised local behavior remains unsupported, report that behavior and evidence explicitly; do not conceal it behind the phrase “external dependency.”

---

## 17. Evidence and source status of this work order

The prior handoff was read directly. `_raeon` runtime boundaries and `platform/shared` were inspected, along with `_bricked` language navigation, domain registry, callable architecture, actual Section 10 CLI and Section 17 parser. The source map records those locations and observed Git blob IDs. Earlier pinned source reads for the compiler/backend are also identified.

A concrete failure to avoid: graph statements accepted by Section 10 and system statements accepted by Section 17 cannot be combined by simply writing `genesis 0.6.0` at the top of a file. The build has to prove the actual supported module/realization composition.

Another concrete packaging failure to avoid: the previous Hypervisor 1.0 prototype ZIP omitted five `__pycache__` files that were still listed in its manifest. v2 packaging must inventory only shipped files. Do not preserve that mistake for nominal compatibility.

The source map, execution plan and acceptance cases accompany this document for machine-readable navigation. They are not new architectural systems and are not claimed to be passing implementation tests. Validate the new code against them, not the other way around.
