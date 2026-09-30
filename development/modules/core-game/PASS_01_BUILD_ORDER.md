# CODEX EXECUTION ORDER — RAEON PASS 1
This is an implementation task, not a planning/summarization task.

## Recover first
From the existing `_raeon` workspace:
1. inspect status/branch/remotes and fetch;
2. preserve newer accepted work;
3. verify audited runtime milestone `71b3a3fbdbce7eece25076a0fd303887cc70d4f1` is in ancestry or identify its accepted successor;
4. read `AGENTS.md`, `development/modules/core-game/GENESIS_RUNTIME_EXECUTION.md`, and every file in this pouch.
Create/continue a dedicated Pass-1 task branch. Do not merge main.

## Build
Create the real production RAEON Genesis application package using the already validated Horizon application-realization contract. It must realize in State:
- one Match;
- exactly two Players;
- one stable Board/player;
- empty Deck, Hand and Graveyard containers/player;
- three fixed Prime positions/player;
- exactly permanent Configuration Spaces A/B/C/player;
- explicit ownership/containment/attachment/visibility relations.

Use real Genesis source compiled/executed by the pinned toolchain. Preserve the existing `horizon-conformance` package as proof infrastructure unless a compatible refactor is required. Python may remain the trusted host binding, but may not replace Genesis realization with a Python-only RAEON graph.

Do NOT implement cards, shuffle/draw, field/QMO resolution, Prime arithmetic, color, turns, combat, victory, UI, animation, Blender or native platform ports.

## Prove
Execute every Pass-1 acceptance case, the existing Genesis runtime tests/audit, current `_raeon` validators/regressions/gameplay specification tests, source-integrity guards, `git diff --check`, and `_bricked` read-only verification.

Create maintained `PASS_01_RECEIPT.md` plus machine-readable receipt in the appropriate development/provenance area. Record exact commands/counts, branch/start/end/remote SHA, negative tests, limitations and Pass-2 entry state. Push the task branch and leave the tree clean. Main remains untouched.

# Pass 1 build order — Production RAEON realization

## Existing machine — do not redesign
`GENESIS HORIZON <-> PYTHON HYPERVISOR <-> PLATFORM PORT`.
Horizon = one `sea -> Shell -> Nexus -> State`; Chirality Fabric foundational; Rainbow Road sole internal transport. The Horizon already supports verified `manifest -> admission/integrity -> realize_application -> State successor`.

## Read current Git authority
Before coding read current versions of:
`data/board/genesis-horizon.json`, `design/game/board/SYSTEM.md`,
`data/game/match.json`, `design/game/match/SYSTEM.md`,
`data/topology/configuration-spaces.json`, `data/platform/runtime-direction.json`,
`game/core/genesis_horizon/README.md`, Horizon adapter, and conformance application.
Newer accepted Git authority supersedes this pouch snapshot.

## Production placement/package
Place production RAEON application source under the existing executable `game/` architecture, not `tests/`, without creating a redundant top-level project. Provide a stable/versioned manifest, real `.gen` realization/observation sources as needed, immutable source hashes and declared views. If Horizon allowed roots currently admit only the conformance test package, deliberately add the production RAEON root while keeping arbitrary paths denied.

## Topology
MATCH: one stable Geometric containing/owning two player organizations. Do not invent OPEN match rules.
PLAYERS: exactly two stable semantic roles, independent of screen coordinates.
BOARD: one stable Geometric/player; dynamic relational framework, not a flattened dictionary or alias of children.
BOARD attachment roles: DECK_PORT, HAND_PORT, GRAVEYARD_PORT, PRIME_PORT, CONFIG_PORT. Port/role identity is distinct from attached child.
CONTAINERS: stable empty Deck/Hand/Graveyard/player. Metadata may encode accepted ordered/capacity constraints, but no movement mechanics.
PRIME REGION: exactly three fixed empty positions/player; do not invent Prime card population.
CONFIG REGION: exactly A/B/C/player, permanent universal, persistent GEOMETRIC, initial EMPTY, no expansion spaces. Configuration Space is not QMO.

## Identity/atomicity
All runtime identities unique/stable; coordinates never identity. Relationships explicit/queryable. Realization is one coherent State successor or none. Observe cannot duplicate. Checkpoint/restore/restart preserve semantic topology. Identical package realization follows current idempotent contract; conflicting application rejected.

## Visibility
Define/test owner-private and opponent-public projections sufficient to prove authorized own topology and no hidden opponent/private/native-backend leakage. Views are projections of one State.

## Required negative cases
Unauthorized realization; package/source SHA tamper; path escape; undeclared/malformed source; duplicate/conflicting semantic identity; injected pre-publication failure; application attempt to inherit/mutate machine domains. Every rejection preserves prior semantic root.

## Genesis/toolchain
Topology must be produced by actual Genesis source. Compile twice and prove deterministic bytecode. Do not invent syntax. Do not regenerate QMO/cycle mathematics.

## Headless demonstration
Boot Horizon -> realize production RAEON -> bind both player Hypervisor sessions -> HELLO/SNAPSHOT -> prove empty topology/privacy -> checkpoint -> close/restart/restore -> reconnect -> prove same semantic identities/topology with new boundary epoch -> prove observation alone does not advance game revision.

## Hygiene/exit
Generated evidence stays in established ignored build locations. Maintained source/tests/provenance stay in established repository paths. No caches/venvs/generated ZIPs/copied `_bricked` committed. Pass 1 is complete only when every acceptance case passes, existing gates remain green, remote branch matches local HEAD, worktree clean, main unmerged.

# Test/build requirements
Inspect current tooling and extend the existing canonical runtime runner rather than creating redundant command families.

Rerun at least:
```text
python -B tools/genesis_runtime.py doctor
python -B tools/genesis_runtime.py dependencies verify
python -B tools/genesis_runtime.py build
python -B tools/genesis_runtime.py verify
python -B tools/genesis_runtime.py test
python -B tools/genesis_runtime.py repository-test
python -B tools/genesis_runtime.py audit
git diff --check
```
Add Pass-1 production RAEON realization/demo tests through this tooling or the repository's current canonical equivalent. Use real Horizon/Hypervisor, never fake integration. Run current repository validators/regressions/gameplay tests as Git currently prescribes. Record actual current counts, not historical expected counts.

Evidence: compiler/build receipts, Pass-1 tests, acceptance mapping, repository validation, branch/head/remote/clean status, upstream read-only check.
