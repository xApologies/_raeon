# Pass 4 receipt

Status: **107/108 execution cases passed; final receipt/push audit pending**.
Original Pass 3 now passes **98/98**, including P3-047 current-color/availability carryover. Pass 3B remains **85/85**. Whole-game **PREPRODUCTION**.

## Git and inheritance

- Branch: `codex/raeon-pass-04`
- Starting Pass-3B SHA: `d644a361aa2ce788a1da991b15e3b8e3be5c7cba`
- Validated implementation ending SHA and verified remote SHA: `0c0bfe128cfd45655075ddea28d14e3e00c5388e`
- Receipt audit HEAD/remote: `0c0bfe128cfd45655075ddea28d14e3e00c5388e`
- Main: `69a0030805b8c3858c877a514e2f50644421115a`, unchanged and unmerged.
- A later documentation-only commit seals this record. The exact final clean HEAD/remote are checked and recorded by `tools/genesis_runtime.py audit` in `build/genesis_runtime/evidence/pass-04-acceptance.json`.
- `_bricked` remains read-only and clean at `c89676fc26000ae6f5fdad66a56e118b285d9b1d`. Runtime uses the locked dependency copy under this repository.

A fresh entry audit verified the complete Pass-3B checkpoint and inherited Pass-2 privacy correction before implementation. All 63 prior test/fixture files remain byte-identical. Their hashes, the complete pouch and original entry evidence remain preserved.

## Implemented scope

Ordinary fields retain immutable native QMO authority with mutable current color and READY/USED state. Generation uses the current magnitude exactly once through Rainbow Road. Same-topology reconfiguration preserves color and availability. Restore caps at native maximum; zero-color destruction moves exact support copies to Graveyard and collapses incident emergents atomically.

All 14 ordinary Prime identities retain their fixed positions, rank-based H/C, health-first Restore, shield-first Degrade and partial repeated C spending. Inactive Primes stay in their slots; admitted White Restore produces only (1,0). Explicit ACTIVE/DEFENSE authority admits the accepted side/direction rules. Switching active player never refreshes fields. Trusted refresh and White Restore primitives do not invent a scheduler or generic Utility timing.

Five new compiled Genesis handlers run through the existing Nexus transaction and Rainbow Road. Negative tests reject altered Genesis admission/transform and bypassed Road delivery. Hypervisor source is unchanged. Recovery, stale revisions, concurrent use, rollback, lost delivery, deterministic replay and selected-view privacy remain exercised.

## Preserved authority

- 120 Field Generators; 60 base + 343 fusion + 1,691 emergent = 2,094 atlas objects. All 11 QMO source hashes remain unchanged; no mathematics was regenerated or fabricated.
- The 14-Prime catalog, 51-Utility structure and ordinary Cycle-1 count of 185 remain unchanged.
- Pouch SHA256: `078b7d8c4c052dc506336337645950b2457655826a3eca160c79c116f3b07dbf`
- Implementation digest: `a6b701577dfb228355249d33cc6f8bf3eec3ee0c550743a9322a07eaf4d63937`

## Validation

The offline validator continued through the usage-limit interruption. No completed case was restarted. Publication was held until all remaining execution and offline checks finished and the complete acceptance evidence was reviewed; remote/receipt gates stayed unpassed until their publication was verified.

- Local Python: 6 unit and 121 integration tests passed, including all 60 base witnesses and all prior tests.
- Upstream: 575 checks across 13 pinned domains passed.
- Runtime 74/74; Pass 2 83/83; privacy correction 8/8; original Pass 3 98/98; Pass 3B 85/85.
- Seven repository validators, 238 regression tests and 17 gameplay specifications passed.
- All 46 Genesis sources rebuilt deterministically. Supported dialect integration passed. `git diff --check` passed.

Qualified host: CPython 3.12.10, normal allocator, process affinity mask 65536 (logical CPU 16). TEMP/TMP point to the repository build directory. This changes only the task process, not machine-wide settings. **HOST-RUNTIME-001 remains OPEN_QUALIFIED**; unrestricted Windows runtime stability is not claimed.

Reproduction commands under that qualified process and pinned Python:

```text
python -X utf8 -B tools/genesis_runtime.py verify
python -X utf8 -B tools/genesis_runtime.py test
python -X utf8 -B tools/genesis_runtime.py dialect-test
python -X utf8 -B tools/genesis_runtime.py repository-test
python -X utf8 -B tools/genesis_runtime.py package
python -X utf8 -B tools/genesis_runtime.py verify-distributions
python -X utf8 -B tools/genesis_runtime.py audit
git diff --check
```

Repository-test runs validate-bootstrap, validate-design-state, validate-normalization, validate-continuity, validate-cycle1-import, validate-full-migration, validate-game-definition, every repository regression and all existing gameplay specification tests.

## Offline delivery

| Archive | Bytes | SHA256 |
| --- | ---: | --- |
| `genesis-horizon-0.4.0.zip` | 19234914 | `b84c47ac81847c488d84db9620abec318bd9e8ee3292d542baf6857878781881` |
| `raeon-python-hypervisor-0.4.0.zip` | 17401 | `3c5f93f101c28cb34c5527f4a0ef137e6f1740a9eb479a8be0740b6cc1a94d90` |

Fresh extraction passed offline installation, deterministic compilation, all demos, 6 unit and 121 integration tests, and missing-runtime/QMO/Pass-4-input negatives. The color scene demonstrates generation, partial spend, hostile degradation, reserved DEFENSE output and restart.

Independent audit hooks recorded 2,418,965 events with zero unexpected violations. Explicit probes denied network, DNS, Git, original `_raeon` and `_bricked` checkout reads. This verifies the trusted qualified host runtime; native devices/graphics remain NOT_RUN.

## Remaining OPEN items

- Exact refresh boundary and full turn/phase/priority/reaction scheduler
- Starting hand, draw cadence, mulligan, first-player choice
- Overflow beyond H/C or field capacity: reject; no discard or redirection
- Generic Utility timing and cost; White reactivation requires admitted policy
- Exhaustive targeting and output allocation; self-spend target rejected
- Victory/loss/deck exhaustion, timer, temporary-space expiry
- Derived additions/splitting/recursive fusion-emergence and derived/emergent production cadence
- Native UI/graphics and unrestricted host-runtime stability
- HOST-RUNTIME-001: unrestricted host stability and underlying cause.

## Files

No files moved, renamed or deleted. Added/modified files:

```text
M	AGENTS.md
A	data/game/pass-04-runtime.json
M	data/manifests/current-files.json
A	development/modules/core-game/HOST_RUNTIME_RISKS.json
A	development/modules/core-game/PASS_04_EXECUTION.md
A	development/modules/core-game/PASS_04_PROGRESS.json
A	development/modules/core-game/PASS_04_RECEIPT.md
M	development/modules/core-game/README.md
M	game/core/genesis_horizon/bindings/python/src/raeon_genesis_horizon/collections.py
M	game/core/genesis_horizon/bindings/python/src/raeon_genesis_horizon/native.py
A	game/core/raeon/application/generate_field.gen
M	game/core/raeon/application/manifest.json
A	game/core/raeon/application/refresh_fields.gen
A	game/core/raeon/application/set_active_player.gen
A	game/core/raeon/application/spend_prime.gen
A	game/core/raeon/application/white_restore_prime.gen
M	game/match/README.md
M	game/primes/README.md
A	game/primes/state.py
M	game/sandbox/topology.py
A	provenance/decisions/raeon-pass-04.json
A	provenance/imports/raeon-pass-04/RAEON_DIPLOMATIC_POUCH_PASS_04_2026-10-01.zip
A	provenance/imports/raeon-pass-04/entry.json
A	provenance/imports/raeon-pass-04/handoff/00_EXECUTE_THIS_FIRST.md
A	provenance/imports/raeon-pass-04/handoff/CURRENT_STATE.json
A	provenance/imports/raeon-pass-04/handoff/MANIFEST.json
A	provenance/imports/raeon-pass-04/handoff/PASS_04_ACCEPTANCE.json
A	tests/integration/genesis_horizon/pass_04_support.py
A	tests/integration/genesis_horizon/test_pass_04.py
A	tests/integration/genesis_horizon/test_pass_04_math.py
A	tests/regression/pass-04-contract.test.mjs
M	tools/genesis_runtime.py
M	tools/genesis_runtime_distribution.py
M	tools/genesis_runtime_isolation.py
M	tools/genesis_runtime_pass02.py
M	tools/genesis_runtime_pass03.py
M	tools/genesis_runtime_pass03b.py
A	tools/genesis_runtime_pass04.py
M	tools/validators/genesis-runtime-contract.mjs
M	tools/validators/pass-03b-contract.mjs
A	tools/validators/pass-04-contract.mjs
```

Case evidence, exact hashes, archive identities and inherited results: [PASS_04_PROGRESS.json](PASS_04_PROGRESS.json). Authority and implementation boundaries: [PASS_04_EXECUTION.md](PASS_04_EXECUTION.md).
