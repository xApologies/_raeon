# RAEON Pass 2 receipt

Status: SOFTWARE_SCOPE_COMPLETE. Date: 2026-09-30.
Repository: `xApologies/_raeon`. Working branch: `codex/raeon-pass-02`.
Starting commit: `23ebfc3be3a4e6ae4883793bfc99b1dbfae67bf8`.
Implementation/archive commit: `f5c380deccb1297f455a599004b159706b39735c` (verified pushed).
Closing receipt commit and exact final remote SHA: resolved by the final
`build/genesis_runtime/evidence/pass-02-acceptance.json` and `remote.json` after
this documentation commit; these generated records avoid self-referential hashes.
Main before/after: `69a0030805b8c3858c877a514e2f50644421115a`. No main merge.
Whole-game phase: PREPRODUCTION; existing module gates unchanged.

## Implemented source and bindings

Production application: `game/core/raeon/application/`, ID `raeon`, version
0.2.0, schema 3. Seventeen mutating Genesis handlers export:

`INITIALIZE_INVENTORY`, `SHUFFLE_DECK`, `DRAW_ONE`, `COMMIT_FG`, `BIND_PRIME`, `RETIRE_CARDS`, `RETIRE_SUPPORT`, `RECOVER_1`, `RECOVER_2`, `RECOVER_3`, `RECOVER_4`, `RECOVER_5`, `RECOVER_6`, `INSPECT_TOP`, `REORDER_TOP`, `BATCH_TO_HAND`, `ADD_CONFIGURATION_SPACE`.

Three bounded native units instantiate, relate and transport actual card
Geometrics; three Section-14 value templates execute equality, bounds and
addition. OBSERVE and the original empty realization remain available. The
build verifies **36 Genesis sources**, including retained historical sources.
Exact source/bytecode hashes are in `build/genesis_runtime/evidence/build.json`
and the additive `provenance/decisions/raeon-pass-02.json` source amendment.
Original runtime and Pass-1 source decisions remain unchanged.

Compiler/native source pin: `c89676fc26000ae6f5fdad66a56e118b285d9b1d`.
All 1,075 locked source files verify. `_bricked` remains clean at that pin;
execution uses the isolated dependency copy. Graph profile 0.1.0 and control
profile 0.3.0 use their real parsers, compilers, verifiers and interpreters.
No new source syntax or regenerated mathematics is claimed.

Generic bindings in `game/core/genesis_horizon/bindings/python/src/raeon_genesis_horizon/`
add typed nonempty arguments, integer-value binding, candidate collections,
source/catalog validation, scoped conformance grants, native State-local Road
transport, live projections, and exact ABI-bound checkpoint recovery. See
`provenance/decisions/raeon-pass-02.md` for callers, effects and compatibility.
The Hypervisor remains unchanged and contains no game rules.

`catalog.json` indexes 120 FG + 14 Prime + 51 Utility = **185 identities**.
Each record retains its source path, pointer, original source hash and record
hash. Printed Prime/Utility IDs remain OPEN; provisional labels remain intact.
The original 120 FG records and 2,094-object atlas are unchanged, as verified by
Git comparison and the existing Cycle-1 source-integrity validator. No canonical
`design/`, `data/cycles/`, `data/qmo/` or `mathematics/` files were modified.

## Delivered behavior

- Empty boot preserves 37 application objects, 163 relationships and revision zero.
- A valid grant creates exactly 60 distinct owned native copies per inventory;
  two players produce 120 copies. Copy limits remain FG 2, Utility 3, Prime 1.
- Deck index zero is next/top. Shuffle uses versioned SHA-256 counter/rejection
  sampling and Fisher-Yates, checked against a full independent order vector.
  RNG state and ordering commit together; duplicate delivery does not advance them.
- Draw, FG commitment and structural Prime binding move existing copies. Native
  versions and history advance; logical identity and ownership persist. Hand
  capacity is seven. No free extraction, automatic field closure or Prime combat.
- Cause-authorized retirement and six source-linked recovery profiles preserve
  ordered batches and survivors. Bounded inspection/reordering/batch helpers
  remain separate from full Utility play policy.
- Initial A/B/C persist. Native Configuration Spaces grow from three to nine;
  additional capacities are Red 3 through Violet 8. Repeated colors are permitted.
- Owner Hand views, count-only future Deck/Graveyard views, bounded authorized
  inspection, detached projections, retry/conflict/stale-input checks, grant
  durability, rollback and nonempty checkpoint/restart/replay all execute.

## Commands and evidence

Host: Windows x64, CPython 3.12.14, NumPy 2.3.5, setuptools 84.0.0.
Executable source/data identity: `4bf599f2fb8fe6102424a86620ba21b2d09e81571d980332dbb3f38e53c07c09`.
Commands below use `python tools/genesis_runtime.py` with that Python runtime.
All positive commands exited 0. Generated logs/results are under
`build/genesis_runtime/evidence/`.

| Command | Verified result |
| --- | --- |
| `dependencies verify` | 1,075 pinned files; zero mismatches |
| `verify` | 36 compiled sources; verifier and deterministic rebuild pass |
| `demo --headless` | Original conformance scenario passes |
| `demo --headless --application raeon` | Current empty board and historical Pass-1 scenario pass |
| `demo --headless --application raeon --scenario cards` | Two-player native card flow, nine spaces and checkpoint/restart pass |
| `test` | 6 unit + 56 integration tests; 575 upstream checks in 13 suites |
| `repository-test` | All seven validators, 211 regression tests, 17 gameplay-design tests, whitespace check pass |
| `package` | Two exact matching archives from clean implementation commit |
| `verify-distributions` | Fresh installation/rebuild/demos/unit/integration/restart and dependency-negative probe pass |
| `audit` | Runtime 74/74 and Pass 2 **83/83** mandatory cases pass |

The 18 historical Pass-1 integration tests remain in the full suite. Their exact
old package is preserved under `tests/integration/genesis_horizon/pass_01_application/`.
The reproduced pre-change Pass-1 audit (38/38) and baseline evidence remain
under `build/genesis_runtime/pass-02-baseline/`; historical results were not rewritten.
Mandatory failures/NOT_RUN/BLOCKED: **0**. Native device/SDK tests: **NOT_RUN**,
outside the mandatory supported-host scope. Policy gates below are not waivers.

Property/negative evidence covers both owners, unique membership/conservation,
all-or-none setup and batch failures, full-Hand refusal, bad profiles/owners,
forged/reused grants, concurrent stale requests, removal/prepublication failure,
lost delivery, changed request IDs, missing handlers, unclosed native transport,
source/catalog/checkpoint/ABI tampering, and fresh-process retry/replay.

## Offline distributions

Both archives bind source commit `f5c380deccb1297f455a599004b159706b39735c`. Their exact inventories,
file hashes and original dependency notices are inside each archive.

| Component | Archive | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| horizon | `genesis-horizon-0.2.0.zip` | 17,840,560 | `c25ed8b394a5618673e32bbc745670a1b8b17141db8e326590cd45c7bc4f6b38` |
| hypervisor | `raeon-python-hypervisor-0.2.0.zip` | 17,293 | `c5c5b16fb4c34bb6fbdc298f088848401dbf4e60fdc60984e0d31dea85496002` |

Archives: `build/genesis_runtime/distributions/`. Manifest names:
`distribution/horizon-manifest.json` and `distribution/hypervisor-manifest.json`.
Fresh extraction: `C:\Users\rando\AppData\Local\Temp\RAEON clean extraction 6c0l1knd`. **1,390** inventory files verified.
All 56 installed integration tests and six installed fence unit tests passed.
Rebuilt bytecode/data identities matched at the different physical location.
Checkpoint recovery also ran in a separate process.

Isolation used independent Python audit interception installed into every fresh
venv interpreter. Probes demonstrably denied network connection/DNS, Git
subprocess execution and original-checkout reads. Runtime file access was
confined to the extracted bundle/writable state and declared Python/Windows
prerequisites. **254,406 events** were recorded with no
unexpected denials. This is interception of trusted pinned Python reference
engines, not an OS sandbox for arbitrary malicious native code. Installation
used included wheels and disabled package indexes. An essential temporary-copy
dependency was moved aside: startup exited **1 as expected**, reported missing
source, and did not fetch anything. The test file was restored afterward.

Supported delivery is Windows x64 CPython 3.12 with bundled NumPy/setuptools
wheels and compiler/runtime sources. The interpreter itself remains a declared
prerequisite. Signed native apps, mobile/desktop native Port SDKs and device
certification are not shipped or claimed.

Pass-3-only atlas/closure inputs such as `data/qmo/cycle1/atlas.json`,
`manifold_pair_relations.json`, `derived_qmos.json`, `qmo.sqlite`, manifold,
fusion and emergent catalogs remain preserved in Git. Pass 2 does not read them
at runtime, so they are not hidden external dependencies of this bundle; a
future Pass-3 package must explicitly include whichever of them it consumes.

## Still policy-gated

- **POL-01** — Opening hand, draw cadence, mulligan, first player. OPEN_POLICY.
- **POL-02** — Prime selection/start placement and deck counting. OPEN_SETUP_POLICY.
- **POL-03** — Multi-card overflow and short-deck outcomes. OPEN_RESOLUTION_POLICY.
- **POL-04** — Utility play cost/window/consumption. OPEN_PLAY_POLICY.
- **POL-05** — Selection remainder ordering and short surveys. OPEN_REMAINDER_POLICY.
- **POL-06** — Temporary-space expiry/removal, merge/base accounting. OPEN_EXPIRY; ACCEPTED_MERGE_IMPLEMENTATION_DEFERRED.
- **POL-07** — Field destruction timing and support batching. OPEN_DAMAGE_TIMING.
- **POL-08** — FG pose/manifold legality. ACCEPTED_DESIGN_IMPLEMENTATION_DEFERRED_TO_PASS_3.
- **POL-09** — Refresh, reaction, victory and complete match loop. OPEN_VICTORY; PRIME_RUNTIME_DEFERRED_TO_PASS_4.

## Git and next pass

Maintained change inventory at the implementation milestone: 48
added and 15 modified files; no deleted or renamed files.
Source, tests, catalog index, exact source amendment, original pouch, policy ledger
and this recovery/receipt documentation are maintained in Git. Build outputs,
native state, test logs, traces and archives remain ignored generated artifacts.

Pass 3 starts from deployed provenance-bearing FG copies, ordered card zones,
dynamic spaces, owner views and replayable native state. Its next substantive
work is the accepted pose/relationship/QMO legality layer. Recovery command:
`python tools/genesis_runtime.py demo --headless --application raeon --scenario cards`.
Verify the ending local/remote SHA and clean status using the generated final
audit record. The completed branch is pushed; main remains untouched.
