# CODEX DIRECTIVE — RAEON CHECKPOINT 0004
## Repository Normalization and Scaffold Population

Target: https://github.com/xApologies/_raeon
Source branch: design/cumulative-recovery-0003
Create branch: architecture/repository-normalization-0004

## Mission
Checkpoint 0003 recovered raeon design state, but the repository information architecture is not functioning as the intended game-development workspace. Fix the organization. This is not a bootstrap, design-note dump, redesign, or gameplay implementation. Preserve the root scaffold and normalize/populate it so a developer can immediately locate current design, machine data, implementation boundaries, tests, development status, and provenance.

## 1 Audit first
Recursively inventory the complete source branch before editing. Classify files as governance, production, development status, design specification, mathematical authority, machine data, runtime implementation, content/asset, tooling, test, platform, provenance/history, placeholder, duplicate/redundant, or misplaced. Identify duplicated current rules, monoliths, stale OPEN statements, empty scaffold areas that now have relevant content, broken links, competing authority, and state stored only in provenance or accepted-state.json. Make an internal migration plan. Never delete historical provenance.

## 2 Preserve root spine
Keep README.md, PROJECT_CONSTITUTION.md, DEVELOPMENT_CONSTITUTION.md, CONTRIBUTING.md, CHANGELOG.md and production/, development/, design/, mathematics/, game/, content/, data/, tools/, tests/, platform/, releases/, provenance/. Keep _inbox/ local-only/gitignored. Do not create a competing root architecture.

## 3 Authority chain
Constitutions govern process. Design specifications define accepted game behavior. Mathematics defines mathematical legality. Machine-readable data encodes accepted design/math. game/ implements it. tests/ verifies it. development/ tracks maturity/gates/milestones/builds/checkpoints. provenance/ records history/decisions/sources/audits. content/ is presentation assets. platform/ is platform integration. No downstream layer silently redefines upstream authority. Provenance is history, not primary current specification; development status is not gameplay specification.

## 4 System-oriented design
Normalize design/ around actual raeon systems. Semantic target:

design/
  README.md
  game/
    GAME_DESIGN_DOCUMENT.md
    match/
    board/
    progression/
  cards/
    CARD_SYSTEM.md
    cycle_01/
      CYCLE.md
      field_generators/SYSTEM.md + catalog/
      primes/SYSTEM.md + catalog/
      utilities/
        SYSTEM.md
        transduction/SYSTEM.md
        activation/SYSTEM.md
        sandbox_activation/SYSTEM.md
        draw_deck/SYSTEM.md
        recovery/SYSTEM.md
        stability/SYSTEM.md
        catalog/
    black/
      SYSTEM.md
      primes/
      utilities/
      black_mode/
  topology/
    sandbox/
    field_generators/
    manifolds/
    fusion/
    emergent_fields/
  transduction/
  collection/
  economy/
  ai/
  multiplayer/
  rendering/
  ui_ux/

Adapt names only where existing conventions justify it. Requirement: one obvious current-specification home for every system.

## 5 Split Utility monolith
Refactor checkpoint-0003 design/cards/cycle_01/UTILITIES.md into a Utility overview plus dedicated current specifications for Transduction, Activation, Sandbox Activation, Draw/Deck, Recovery, Stability/Protection. Overview contains total 50, family allocation, shared Utility rules, copy limit 3, links, status, global OPEN questions. Do not lose mechanics. Historical checkpoint files remain untouched.

Preserve exactly:
Transduction 18 = Restore 6 + Degrade 6 + Universal 6.
Activation 7.
Sandbox Activation 6.
Draw/Deck 7.
Recovery 6.
Stability/Protection 6.
Utility identity copy limit 3; no color uniqueness restriction.

Restore: Red +1, Orange +2, Yellow +3, Green +4, Blue +5, Violet +6.
Degrade: Red -1, Orange -2, Yellow -3, Green -4, Blue -5, Violet -6.
Universal: Orange ±1, Yellow ±2, Green ±3, Blue ±4, Violet ±5, White ±6.
Activation: seven identities Red through White; eligible early USED->READY; detailed per-rank effects OPEN.
Sandbox Activation: Red capacity 3, Orange 4, Yellow 5, Green 6, Blue 7, Violet 8. Three permanent Sandboxes remain universal; capacity does not guarantee closure.
Draw/Deck: preserve all seven checkpoint-0003 definitions unchanged.
Recovery: preserve all six checkpoint-0003 definitions unchanged; ordinary Prime resurrection excluded.
Stability: preserve Color Guard, Prime Guard, Manifold Guard, Shield Lock, Structural Anchor, Emergent Amplification. Coupling Stabilizer remains rejected.
Do not rebalance during normalization.

## 6 Card system
Create obvious current homes for Field Generators, Prime Fields, Utilities, Black cards, Cycle 1. Preserve 120 Field Generators + 30 Prime Fields + 50 Utilities = 200; deck size 60; Field Generator identity max 2; Utility identity max 3; Prime identity unique; 3 active Prime positions. Do not invent missing catalogs. Catalog boundaries may explicitly say OPEN or SOURCE_IMPORT_REQUIRED.

## 7 Topology
Give Sandbox, Field Generator geometry, Local Manifolds, Fusion, Emergent Fields obvious current homes. Preserve 3 permanent universal Sandboxes; committed Generators cannot be independently extracted; whole Sandbox domains may merge/fuse; closure precedes color; closed counts 3/4/5/6/7/8 -> Red/Orange/Yellow/Green/Blue/Violet; base basis 15/13/11/9/7/5 = 60; external inventory 60 + 343 + 1691 = 2094; actual QMO packages SOURCE_IMPORT_REQUIRED.

Emergent Fields: supports remain; field is relational/supported; cannot be directly attacked or independently destroyed; remove by breaking required support topology. Emergent Amplification +1 capped Violet/6 and does not change support rules.

## 8 Black system
Normalize Black material coherently. Preserve Black=8 above White; no Black Field Generators; exactly 3 Black Prime identities; Black Utilities exist; Black cards legal in normal decks; all-Black deck = 3 Black Primes + 57 Black Utilities; legal all-Black deck unlocks hidden Black Mode. Fourth Prime accessible iff all three Black Primes alive; not a fourth deck card; supported/emergent; inaccessible if any supporting Prime dies. Shield of the Abyss and Topaz Lake remain WORKING DESIGN, not finalized cards.

## 9 Machine data mirrors design
Normalize data/ conceptually as:

data/
  cycles/cycle_01/
    manifest.*
    field_generators/
    primes/
    utilities/
      transduction.*
      activation.*
      sandbox_activation.*
      draw_deck.*
      recovery.*
      stability.*
  qmo/generators/
  qmo/manifolds/
  qmo/fusion/
  qmo/emergent/
  black/
  balance/
  render_specs/
  schemas/
  manifests/

Do not fabricate missing catalogs/QMOs. Use explicit OPEN/SOURCE_IMPORT_REQUIRED status manifests. Keep accepted-state.json high-level, with pointers to detailed datasets instead of becoming the entire database. Increment schema and document migration if needed.

## 10 Mirror invariant
Document: DESIGN defines behavior -> DATA encodes accepted behavior/state -> GAME implements it -> TESTS verifies it. Major systems should be navigable across those layers. Runtime/test locations may be boundary/index files only for now; no fake implementation/tests.

## 11 game/ implementation only
Normalize game/ as executable boundaries: core, match, state, rules, board, cards/generators, cards/primes, cards/utilities, sandbox, qmo, manifolds, transduction, collection, ai, multiplayer, rendering, ui, persistence. Reuse existing directories. Do not implement gameplay. Boundary READMEs link upstream.

## 12 tests/ mirrors systems
Support unit, integration, regression, gameplay/cards, gameplay/sandbox, gameplay/manifolds, gameplay/transduction, gameplay/primes, gameplay/utilities, qmo, rendering, multiplayer, adversarial, performance. Preserve validator regression tests. No fake passing gameplay tests.

## 13 development/ tracks status, not rules
development/ tracks module maturity, gates, milestones, builds, checkpoints. Module dashboards link to authoritative design, mathematics, data, implementation, tests, provenance. Replace duplicated gameplay rules in module READMEs with links/status summaries where appropriate.

## 14 provenance/ is history
Preserve checkpoints/decisions/sources/audits 0001-0003. Provenance answers origin/change/rationale/date/rejections/evidence; it is not primary current gameplay specification.

## 15 README and current-state index
Update root README as developer entry point linking Game Design, Card System, Topology, Mathematics, Machine Data, Runtime, Content, Tests, Development Status, Production Status, Provenance, Inbox. Update/create design/README.md as concise current-state index: what raeon is, GAME_CANON, structurally designed systems, OPEN, SOURCE_IMPORT_REQUIRED, implemented/not implemented, next design task. Link outward; do not duplicate all specs.

## 16 Remove redundancy safely
For duplicate non-historical prose rules, choose one authoritative current specification and replace other copies with concise summaries/links. Never delete provenance/history. Never remove structured data merely because prose exists. Migrate validators before removing validator-required paths.

## 17 Validation
Update validators for normalized architecture. Validate root spine; links; design system boundaries; Cycle-1 card boundaries; six Utility family boundaries; structured Utility data mirrors families; runtime/test boundaries; development dashboards link upstream; _inbox untracked; accepted-state pointers resolve; no conflicting current authority; all checkpoint-0003 numerical invariants remain true. Migrate prior design-state tests to normalized paths. Repository validators explicitly do NOT validate QMO mathematics, gameplay balance, rendering, AI, or multiplayer correctness.

## 18 Migration audit
Create provenance/audits/0004-repository-normalization.md (or convention-equivalent) with before/after tree summary, moves/renames/splits/consolidations, retained files, authority changes, links, schemas, validators, proof no accepted rule was lost, proof provenance 0001-0003 intact.

## 19 Decision/checkpoint
Create Decision 0004 and Checkpoint 0004. Record source/working branches, starting/ending SHA, files added/moved/renamed/modified/deleted, validator results, production phase, module statuses, OPEN, SOURCE_IMPORT_REQUIRED. Whole-game phase remains PREPRODUCTION. No gameplay implementation claimed.

## 20 Do not redesign or implement
This is an information-architecture migration. Do NOT change accepted mechanics, rebalance cards, assign UT-001..UT-050, design 30 Primes, generate QMOs, implement runtime, implement networking/AI/rendering, or invent missing mathematics. Preserve unresolved fields as OPEN and missing authoritative packages as SOURCE_IMPORT_REQUIRED.

## 21 Source-import boundary
Preserve SOURCE_IMPORT_REQUIRED for Genesis mathematics, Chirality mathematics, Propagation Engine mathematics, QMO API/definitions, closure operators, transduction math/API, Field Generator QMO data, 60 base manifold package, 343 fusion-derived package, 1,691 emergent package, complete 2,094 atlas, Cycle Generation Constitution, deterministic RenderSpec/API packages, Blender-facing atlas/reference material, higher-dimensional projection mathematics.

## 22 Execute
1. Fetch source branch.
2. Audit recursively.
3. Create architecture/repository-normalization-0004.
4. Build migration plan.
5. Normalize design/data/game/tests/development navigation.
6. Preserve mathematics/source-import boundaries.
7. Update README/current-state index.
8. Update accepted-state/schema/pointers as necessary.
9. Update validators/tests.
10. Create Decision/Audit/Checkpoint 0004.
11. Run validators/regression tests and git diff --check.
12. Inspect git status/diff for accidental mechanic changes or lost information.
13. Commit.
14. Push branch to GitHub.
15. Do NOT merge to main.

## 23 Final report
Report: branch; starting/ending commit SHA; complete top-level tree; normalized design tree; data tree; game tree; tests tree; files added/moved/renamed/modified/deleted; monoliths split; duplicate authority removed; schema migration; validators/tests and exact results; provenance records; GAME_CANON preserved; OPEN preserved; SOURCE_IMPORT_REQUIRED preserved; production phase; module statuses; conflicts; anything intentionally unchanged; recommended next task.

Explicitly state:

WHOLE-GAME PHASE REMAINS PREPRODUCTION.
NO GAMEPLAY IMPLEMENTATION WAS CLAIMED BY CHECKPOINT 0004.
REPOSITORY NORMALIZATION DID NOT CHANGE ACCEPTED GAME MECHANICS.
