# RAEON Pass 3 receipt

**Status: PARTIAL. Not ready for Pass 4. Whole-game PREPRODUCTION.**
Date: 2026-09-30. Repository: xApologies/_raeon. Branch: `codex/raeon-pass-03`.

Corrected Pass-2/start SHA: `d991278bc72518e9abe2df7741298a2631c787d0`.
Implementation and archive source SHA: `84bb5ec6e773cf6cf3f8957c13f80cbbccc09b54` (pushed and verified).
Pre-correction ancestry anchor: `8a20961b97b0bbb6e2e257d3c3ff62992ea6d839`.
Main before/after: `69a0030805b8c3858c877a514e2f50644421115a`; no merge.
The closing documentation commit cannot name itself. Resolve it with `git log -1 --format=%H -- development/modules/core-game/PASS_03_RECEIPT.md`; compare `git rev-parse HEAD` with `git ls-remote origin refs/heads/codex/raeon-pass-03`. The generated post-push audit records the exact final SHA and clean status.

## Entry and preserved work

Before any implementation edits, the corrected branch passed all 64 existing integration tests, including eight real privacy regressions, plus six boundary tests, 575 upstream checks and repository validation. The original runtime/Pass-2 denominators remain 74/83. The entry was clean and correction complete; no concurrent unfinished correction was overwritten. Exact results and log hashes are preserved in `provenance/imports/raeon-pass-03/entry.json`.

All preceding test/fixture sources are hash-preserved by the additive Pass-3 decision. `_bricked` remains read-only, clean and pinned at `c89676fc26000ae6f5fdad66a56e118b285d9b1d`. Runtime execution uses the isolated dependency copy. Existing design, Cycle-1 sources and historical decisions were not rewritten.

## Implemented and demonstrated

- Complete source-locked, lossless index: 120 FGs, 60 base manifolds (15/13/11/9/7/5 ROYGBV), 343 fusion, 1,691 emergent, 2,094 atlas objects, 1,770 manifold pairs and 2,482 compatibility pairs. JSON/SQLite checks and large integer preservation pass.
- Native FG-specific source payloads retain source occupancy, void, faces, color views, rotation class, parity and hash. Copy IDs, ownership and history remain distinct from source QMO IDs. The eight samples are indexed A..H; they are not an invented physical cube embedding.
- `SET_FG_POSES` executes through actual Genesis, Horizon, Rainbow Road and byte-boundary sessions. Bounded integer XY and canonical projective quaternion values represent full 3D orientation. Position Z, malformed/overflow components, zero quaternion, unknown/reflection inputs, wrong ownership, stale membership/pose revisions and extraction attempts reject.
- Atomic batches preserve native copy identity; rollback, identical retry, post-commit delivery recovery, concurrent stale refusal and nonempty checkpoint restoration are tested. Removing Road closure fails compilation; altering required predicates or omitting the handler transformation fails execution. Retirement/recovery clears prior local placement before redeployment.
- Read-only whole-membership candidate search scans all 60 ordinary source rows with multiplicity preserved. Partial face correspondences are explicitly catalog potential, not admitted live edges. Incomplete search remains unresolved. No query activates, heals, refreshes or retires a field/card.
- Reopen retains the persistent space and cards. Merge preview conserves its proposed copy list and reports missing policy. Resolve/merge/link Genesis handlers fail closed; their refusals are not positive field/merge/link implementations.
- Selected-view privacy is retained across source/pose projections, byte deltas and reconnects. Public views do not acquire private Hands, inspections, private relations, native paths or grants.

Live field instances, actual merge/fusion activation, and active emergent support graphs have **not** been demonstrated or claimed. Runtime field/link stores stay empty because no live closure admission has been fabricated; the imported QMO datasets themselves remain fully populated.

## Source and ABI boundary

Application version and paired distribution release: 0.3.0. Existing graph profile: Genesis 0.1.0; existing integer/control profile: Genesis 0.3.0. Extensions: `state-extension-v1`, `raeon-topology-values-v1`, `xy-quaternion-integer-v1`; existing collections ABI remains `state-collections-v1`.

Genesis source declares each effect; the verified generic host extension loads the hash-pinned application source and corpus. The Hypervisor remains game-agnostic. This remains the three-object architecture with one sea/Shell/Nexus/State chain and Rainbow Road transport. The State extension is an in-process application binding, not another VM or transport.

Pose codec: integer XY scale 1000, bounded components, quaternion order w,x,y,z, right-handed active orientation, gcd/sign canonicalization. Numeric equivalence does not confer geometric legality. Physical units, world-face correspondence, contact and snapping remain unassigned.

The recovered nested v0.2 chirality reference defines complementary boundaries; the generator contains unimplemented operator bodies. The normalized closure API is a catalog lookup, and RenderSpec geometry is a downstream presentation adapter. Neither supplies a complete runtime XY/orientation-to-contact law. Exact source paths and smallest missing decisions are in `PASS_03_POLICY_GATES.json`.

## Actual validation

| Check | Result |
|---|---|
| Boundary unit tests | 6 passed |
| Runtime/application integration | 81 passed, including 17 new Pass-3 tests and all eight privacy cases |
| Pinned upstream regression checks | 575 passed |
| Genesis compile/verify | 41 sources; deterministic rebuild |
| Repository validators | Seven passed |
| Repository regressions | 221 passed |
| Gameplay-design regressions | 17 passed |
| Previous acceptance | Runtime 74/74; Pass 2 83/83; privacy correction 8/8 |
| Pass-3 unchanged rubric | **49 PASS / 49 BLOCKED or unproven / 0 FAIL; 98 total** |
| Whitespace | `git diff --check` and staged checks passed |

The complete unchanged IDs, expected outcomes, real test names, source digest and per-case results are in `PASS_03_PROGRESS.json`. Full required positive behaviors are not replaced by rejection tests. Some remaining rubric scenarios need further certification as well as the missing live topology contracts. No native-device validation is claimed.

Commands used (Python 3.12, bytecode caches disabled):

```text
python -B -m unittest discover -s tests/integration/genesis_horizon -p test_pass_02_projection_privacy.py -v
python -B -m unittest discover -s tests/integration/genesis_horizon -p test_pass_03.py -v
python -B tools/genesis_runtime.py verify
python -B tools/genesis_runtime.py test
python -B tools/genesis_runtime.py dialect-test
python -B tools/genesis_runtime.py repository-test
python -B tools/genesis_runtime.py demo --headless --application raeon --scenario topology
python -B tools/genesis_runtime.py package
python -B tools/genesis_runtime.py verify-distributions
python -B tools/genesis_runtime.py audit
git diff --check
git diff --cached --check
```

`repository-test` ran validate-bootstrap, validate-design-state, validate-normalization, validate-continuity, validate-cycle1-import, validate-full-migration and validate-game-definition, both Node test groups, and whitespace validation. Exact command arrays and evidence hashes are recorded in progress JSON.

## Offline delivery and integrity

Both archives were built from the same clean implementation commit. Fresh extraction installs only included wheels and uses no original checkout, Git, DNS or network fallback. The original demos, new cold topology query/pose/recovery scenario, six unit tests and all 81 integration tests pass after extraction. Deliberately missing required QMO data and missing runtime source each fail as expected, without fetching replacements. Isolation recorded 506,062 audited events with zero unexpected violations. Cold bytecode matches local output.

| Archive | Source commit | Bytes | SHA-256 |
|---|---|---:|---|
| horizon | 84bb5ec6e773cf6cf3f8957c13f80cbbccc09b54 | 19020547 | `f7edcac7aa74c2f8e6f1ee5b8b14308d85b66e1c7a87d2b7f8ffc7c66df31f62` |
| hypervisor | 84bb5ec6e773cf6cf3f8957c13f80cbbccc09b54 | 17290 | `9e2128763050ec1c045200a7ea5f0f436e203478b0c8233ec5c95c6140d27471` |

Archive directory: `build/genesis_runtime/distributions/`. Supported host: Windows x64 with CPython 3.12 installed; NumPy 2.3.5 and setuptools 84.0.0 wheels are included. Native platforms remain NOT_RUN. Closing receipt edits do not change the tested executable/data digest: `2600bb846ef78ab15d5c0330100d7dc069a2c5264899f4915f9b3aa1e4037f7c`.

The original diplomatic pouch ZIP is preserved unchanged (SHA-256 `9eb693a9adae2469544fa57010d98df6ccc5604172c916dea5b42c780270a35f`); the directly stored acceptance JSON matches its ZIP member byte-for-byte. Original Markdown formatting stays in the archive. Every consumed dataset and hash is in `game/qmo/cycle1.lock.json`; original source archives and canonical mathematical data remain unchanged.

## OPEN and next action

- G-POSE: accepted complete XY/3D pose-to-live-contact mapping, face/frame conventions and simultaneous closure proof. First supply an accepted valid and wrong-pose example for the same source membership, then implement/review the mapping and live field lifecycle.
- G-MEMBERS: accepted handling of duplicate definitions, leftover copies, overlapping assignments and subset selection. Current lookup preserves multiplicity and does not silently discard extras.
- G-MERGE: resulting capacity, local-frame mapping and permanent base-space accounting. Current preview/refusal does not invent a nine-FG limit or restore consumed width.
- G-LINK: live pair admission/timing and permitted recursive domains; dependent support-loss and emergent scenarios require real resolved fields first.
- G-COLOR: current-output carryover/generation eligibility remains separate Pass-4 work. No combat, spending, refresh timing, Utility scheduler, GUI or native ports were added.

Remaining rubric IDs: P3-018, P3-020, P3-030, P3-031, P3-033, P3-034, P3-038, P3-039, P3-040, P3-041, P3-042, P3-043, P3-044, P3-045, P3-047, P3-048, P3-049, P3-051, P3-052, P3-053, P3-054, P3-056, P3-057, P3-058, P3-059, P3-060, P3-062, P3-063, P3-064, P3-065, P3-066, P3-067, P3-068, P3-069, P3-070, P3-071, P3-075, P3-076, P3-077, P3-080, P3-081, P3-082, P3-083, P3-084, P3-085, P3-087, P3-088, P3-093, P3-095.

Continue this branch from the latest receipt commit; inspect Git first. Re-run `python -B tools/genesis_runtime.py audit` to recover current evidence, then address the source contracts above and certify the remaining rubric scenarios. **Do not enter Pass 4 as complete.** Whole-game phase remains PREPRODUCTION. No Cycle-1 mathematics was regenerated, no source QMO was fabricated, main remains unmerged, and `_bricked` was not modified.

## Files

20 added; 12 modified; none moved, renamed or deleted relative to corrected Pass 2. Existing root architecture is preserved.

```text
M	AGENTS.md
M	data/manifests/current-files.json
A	development/modules/core-game/PASS_03_EXECUTION.md
A	development/modules/core-game/PASS_03_POLICY_GATES.json
A	development/modules/core-game/PASS_03_PROGRESS.json
A	development/modules/core-game/PASS_03_RECEIPT.md
M	game/core/genesis_horizon/bindings/python/src/raeon_genesis_horizon/adapter.py
M	game/core/genesis_horizon/bindings/python/src/raeon_genesis_horizon/application.py
M	game/core/genesis_horizon/bindings/python/src/raeon_genesis_horizon/collections.py
A	game/core/raeon/application/link_configuration.gen
M	game/core/raeon/application/manifest.json
A	game/core/raeon/application/merge_configuration.gen
M	game/core/raeon/application/native_instantiate.gen
A	game/core/raeon/application/reopen_configuration.gen
A	game/core/raeon/application/resolve_configuration.gen
A	game/core/raeon/application/set_fg_poses.gen
A	game/qmo/corpus.py
A	game/qmo/cycle1.lock.json
A	game/sandbox/topology.py
A	provenance/decisions/raeon-pass-03.json
A	provenance/imports/raeon-pass-03/RAEON_DIPLOMATIC_POUCH_PASS_03_2026-09-30.zip
A	provenance/imports/raeon-pass-03/entry.json
A	provenance/imports/raeon-pass-03/handoff/acceptance/PASS_03_ACCEPTANCE.json
A	tests/integration/genesis_horizon/test_pass_03.py
A	tests/regression/pass-03-contract.test.mjs
M	tools/genesis_runtime.py
M	tools/genesis_runtime_distribution.py
M	tools/genesis_runtime_pass02.py
A	tools/genesis_runtime_pass03.py
M	tools/validators/genesis-runtime-contract.mjs
M	tools/validators/pass-02-contract.mjs
A	tools/validators/pass-03-contract.mjs
```
