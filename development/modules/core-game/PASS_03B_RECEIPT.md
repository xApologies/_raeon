# Pass 3B receipt

Status: **PASS — 85/85 Pass-3B cases**. Original Pass 3: **97 PASS / 1 BLOCKED / 0 FAIL / 98 total**.
The remaining case is P3-047 (mutable current-color/availability carryover, G-COLOR / Pass 4). It is not counted as passed. No Pass-4 work or readiness is claimed. Whole-game **PREPRODUCTION**.

## Git and continuity

- Branch: `codex/raeon-pass-03b`
- Recovered Pass-3 parent: `33f4139719c5b4af83610dcb9600be594a50e78c`
- Corrected Pass-2 ancestor: `d991278bc72518e9abe2df7741298a2631c787d0`
- Validated implementation and paired-archive commit: `27daedd3772a3b33634e21622a6b80b7b67e2d5c`
- Main remains `69a0030805b8c3858c877a514e2f50644421115a`, unmerged.
- Final closing-documentation HEAD/remote and clean status are checked by `python -B tools/genesis_runtime.py audit`; its exact live receipt is `build/genesis_runtime/evidence/pass-03b-acceptance.json`.
- `_bricked` remains read-only at `c89676fc26000ae6f5fdad66a56e118b285d9b1d`; the isolated locked dependency copy supplies execution.

Entry evidence preserved the recovered 49/49/0 Pass-3 audit and a fresh eight-test privacy run before editing. All 59 earlier test/fixture files remain byte-identical. The previous privacy correction and application architecture are inherited.

## Implemented behavior

All 60 frozen witnesses positively resolve through the actual RAEON Genesis application and Hypervisor. Labeled SE(2) fitting excludes reflection, scale and label permutation. Frozen 24-class quaternion targets share the fitted yaw; 295 required edges retain source face/signature provenance. Candidate and magnetized output do not activate fields without both capture gates.

Atomic LOCK creates a separate native field referencing the existing QMO and preserves card identity/history. Explicit reopen invalidates closure. Deterministic fusion transports the exact physical union into one derived space, retains SUBSUMED source provenance and preserves support-local frames. Capacity remains unspecified; no addition or split rule is introduced. Passive native emergence retains ordinary supports, costs zero spaces and removes only incident emergents when supports are lost.

Public, owner and opponent projection/privacy, failure rollback, committed retry, lost delivery, concurrency, source tamper, deterministic replay and nonempty restart are exercised. Genesis handlers and closed Rainbow Road transport are required; Hypervisor source is unchanged.

## Preserved authority

- 120 Field Generators; 60 base + 343 fusion + 1,691 emergent = 2,094 atlas objects.
- All 11 source-locked QMO datasets remain byte-identical. No Cycle-1 mathematics was regenerated or fabricated.
- Pouch SHA256: `acd410d548ea5503640e789f3acf8c4a77f33b4552b9f5980f8eee06055be23f`.
- Nested realization authority ZIP SHA256: `5e2ed2b3583391ce81e6060b0edfd454bf6b0a3a6b03ca1390e33f2fbc7c486f`.

| Consumed authority | SHA256 |
| --- | --- |
| `data/game/configuration_realization/v1/BASE_MANIFOLD_WITNESSES.json` | `22a264e5ebaa7cc35015e1433b415b5bfaf0fd18339441c2a04713afbb92b2b8` |
| `data/game/configuration_realization/v1/REALIZATION_CONTRACT.json` | `3ba86cfa99db2bbca1083bf6b66ceec1b160512f3a6f83f3340d9fb774dd4876` |
| `data/game/configuration_realization/v1/WITNESS_SCHEMA.json` | `be2cf78a38c876ee6a5766ee14d63bf7f1c3a86300587379bea0eb58d17ef544` |
| `data/game/configuration_realization/v1/ROTATION_CLASS_TABLE.json` | `df2fc56010f01d3389a130d651deb1fe1883795d3acafcfca49ec3fcda251d33` |
| `data/game/configuration_realization/v1/SOFT_SNAP_V1.json` | `4e7a2b18ae3f78d066d1fd6c04d8b1d6d1ecab9669fea6c516c961247301c8a2` |
| `data/game/configuration_realization/v1/ORIENTATION_REALIZATION_V1.json` | `cb70cda9c3e152e9b387bbd99f2d31aedaa006309461678537a04bd628f1dc97` |

## Validation

- Python unit: 6 passed. Integration: 102 passed, including the exhaustive 60-field positive test and all prior privacy tests.
- Pinned upstream: 575 checks across 13 domains passed.
- Runtime acceptance 74/74; Pass 2 83/83; privacy correction 8/8; Pass 3B 85/85. Original Pass-3 denominator stays 98.
- Seven repository validators, 228 repository regressions and 17 gameplay-design tests passed.
- All 41 Genesis sources compile and verify with identical deterministic rebuilds. Supported dialect integration passes.
- `git diff --check` passes.

Qualified host settings: CPython 3.12.10, normal allocator, process affinity mask 65536. In PowerShell set `[System.Diagnostics.Process]::GetCurrentProcess().ProcessorAffinity=[IntPtr]65536` before launching the commands. The executable used was `build/dependencies/python-3.12.10/tools/python.exe`; `TEMP` and `TMP` were the repository `build/` directory. This process restriction is a validation qualification, not a machine-wide change.

Commands (Python 3.12, pinned dependencies):

```text
python -B <extracted-pouch>/VERIFY_POUCH.py
python -B -m unittest discover -s tests/integration/genesis_horizon -p test_pass_02_projection_privacy.py -v
python -B tools/genesis_runtime.py verify
python -B tools/genesis_runtime.py test
python -B tools/genesis_runtime.py dialect-test
python -B tools/genesis_runtime.py repository-test
python -B tools/genesis_runtime.py demo --headless --application raeon --scenario realization
python -B tools/genesis_runtime.py package
python -B tools/genesis_runtime.py verify-distributions
python -B tools/genesis_runtime.py audit
git diff --check
```

Repository-test runs validate-bootstrap, validate-design-state, validate-normalization, validate-continuity, validate-cycle1-import, validate-full-migration and validate-game-definition; it also runs every repository regression and the existing cards/primes/sandbox/manifolds gameplay tests.

## Offline delivery

An initial restricted-process run passed all 60 witnesses but failed a repeated checkpoint at a 271-character destination while Windows long-path support was disabled. The delivery tool now uses the shorter temporary prefix `c `, retaining a space. The unchanged checkpoint test passed in the shorter layout and in an additional focused run inside the exact final extraction; final source validation and full offline verification were rerun after the tool amendment.

The first offline attempt crashed in a preserved privacy-test setup before producing its case receipt and was rejected. Memory diagnostics on bundled CPython 3.12.14 reproduced the access violation on repetition 5. The unchanged case then passed eight consecutive executions on the independently signed CPython 3.12.10 build from [the CPython NuGet package](https://www.nuget.org/packages/python/3.12.10). The complete unrestricted 3.12.10 offline run also failed. A stdlib-only reproducer then crashed without importing RAEON, NumPy or upstream code; the crash also reproduced with `-I -S` (site/user startup disabled), while it passed 5,000 deterministic iterations with process affinity restricted to logical CPU 16 (mask 65536). The three affected application cases passed twice each under that restriction. Final full offline verification uses 3.12.10 with the normal allocator and that process-only affinity mask; no assertions are removed or retried inside a suite. The host access-violation cause remains unproven, including for fresh processes.

| Archive | Bytes | SHA256 |
| --- | ---: | --- |
| `genesis-horizon-0.3.1.zip` | 19101083 | `0e004bebea58da0c8eef50e8a9ff2859bf37f07ed4dbfd1f6762b94acab7b3ea` |
| `raeon-python-hypervisor-0.3.1.zip` | 17400 | `09c0c87865eaba08809ddb098994e9cbb1afb476164c7a616f1663c550686bf1` |

Both archives are under `build/genesis_runtime/distributions/`. Safe exact manifests include the consumed witness/rotation/snap/orientation authority, QMO data, Genesis sources, bindings, tests and the pinned runtime dependency slice. Python 3.12 on Windows x64 is the declared prerequisite.

Fresh extraction passed offline installation, deterministic rebuild, all demos, all 6 unit and 102 integration tests, missing-runtime and missing-QMO negatives. The new scene demonstrates query, magnetization, positive resolution, emergence, fusion and restart. The independent Python audit hook recorded 1,662,737 events with zero unexpected violations; network/DNS, Git and original-checkout reads were denied. An additional fresh-venv probe explicitly verified denial of reads from the original RAEON checkout (build/pass03b-original-checkout-probe.log). This verifies the trusted Python host runtime, not a native-device security sandbox.

## Remaining scope

- Pass-4 current color/output availability, cadence, combat and healing remain outside this pass.
- Arbitrary subset/leftover membership selection is not authorized; ordinary closure uses exact whole membership.
- Derived additions, splitting and recursive fusion/emergence remain unsupported without further authority.
- Native device ports, graphical spring animation and device performance acceptance are not claimed.
- Bundled CPython produced access violations during garbage collection after repeated native-runtime lifetimes in one process. Every test case and every base witness now uses a checked fresh process; the interpreter fault itself and unlimited multi-instance host stability remain unproven.

Historical gate records remain intact. The new authority supersedes the named pose/fusion/emergence gaps within Pass 3B only. The color/availability carryover case stays blocked. Initial development checks exposed an overbroad new owner-privacy assertion and floating-point endpoint comparisons; the assertion now follows the existing selected-view rule and exact-threshold regressions cover the numerical fix. No existing regression was weakened.

## Files

No files moved, renamed or deleted. The exact created/modified list follows (`A` added, `M` modified).

```text
M	AGENTS.md
A	data/game/configuration_realization/v1/BASE_MANIFOLD_WITNESSES.json
A	data/game/configuration_realization/v1/ORIENTATION_REALIZATION_V1.json
A	data/game/configuration_realization/v1/REALIZATION_CONTRACT.json
A	data/game/configuration_realization/v1/ROTATION_CLASS_TABLE.json
A	data/game/configuration_realization/v1/SOFT_SNAP_V1.json
A	data/game/configuration_realization/v1/WITNESS_SCHEMA.json
M	data/manifests/current-files.json
A	development/modules/core-game/PASS_03B_EXECUTION.md
A	development/modules/core-game/PASS_03B_PROGRESS.json
A	development/modules/core-game/PASS_03B_RECEIPT.md
M	development/modules/core-game/README.md
M	game/core/raeon/application/manifest.json
M	game/core/raeon/application/merge_configuration.gen
M	game/core/raeon/application/reopen_configuration.gen
M	game/core/raeon/application/resolve_configuration.gen
M	game/qmo/README.md
M	game/qmo/corpus.py
A	game/qmo/realization.lock.json
A	game/qmo/realization.py
M	game/sandbox/README.md
M	game/sandbox/topology.py
A	provenance/decisions/raeon-pass-03b.json
A	provenance/imports/raeon-pass-03b/RAEON_DIPLOMATIC_POUCH_PASS_03B_2026-09-30.zip
A	provenance/imports/raeon-pass-03b/entry.json
A	provenance/imports/raeon-pass-03b/handoff/MANIFEST.json
A	provenance/imports/raeon-pass-03b/handoff/POUCH.json
A	provenance/imports/raeon-pass-03b/handoff/acceptance/BLOCKED_PASS3_TARGETS.json
A	provenance/imports/raeon-pass-03b/handoff/acceptance/PASS_03B_ACCEPTANCE.json
A	tests/integration/genesis_horizon/pass_03b_support.py
A	tests/integration/genesis_horizon/test_pass_03b.py
A	tests/integration/genesis_horizon/test_pass_03b_math.py
A	tests/regression/pass-03b-contract.test.mjs
M	tools/genesis_runtime.py
M	tools/genesis_runtime_distribution.py
M	tools/genesis_runtime_pass02.py
M	tools/genesis_runtime_pass03.py
A	tools/genesis_runtime_pass03b.py
M	tools/genesis_runtime_tasks.py
A	tools/genesis_runtime_test_worker.py
M	tools/validators/game-definition-contract.mjs
M	tools/validators/genesis-runtime-contract.mjs
M	tools/validators/pass-03-contract.mjs
A	tools/validators/pass-03b-contract.mjs
```

Structured case-by-case evidence, source hashes and distribution details: [PASS_03B_PROGRESS.json](PASS_03B_PROGRESS.json). Scope and authority decisions: [PASS_03B_EXECUTION.md](PASS_03B_EXECUTION.md).
