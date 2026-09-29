# raeon.

Canonical repository: https://github.com/xApologies/_raeon — `main` is the current accepted project tree and default checkout. Temporary development branches are disposable.

**WHOLE-GAME PHASE REMAINS PREPRODUCTION.** No gameplay implementation or mechanic redesign is claimed by checkpoint 0004.

## Developer entry points

| Area | Start here |
| --- | --- |
| Governance | [Project constitution](PROJECT_CONSTITUTION.md), [development constitution](DEVELOPMENT_CONSTITUTION.md), [contributing](CONTRIBUTING.md) |
| Game design | [Current-state index](design/README.md), [Game Design Document](design/game/GAME_DESIGN_DOCUMENT.md) |
| Cards | [Card System](design/cards/CARD_SYSTEM.md), [Cycle 1](design/cards/cycle_01/CYCLE.md) |
| Topology | [Topology design](design/topology/README.md) |
| Mathematics | [Formal authority and missing sources](mathematics/README.md) |
| Machine data | [Data index](data/README.md), [accepted-state pointers](data/manifests/accepted-state.json) |
| Runtime | [Implementation boundaries](game/README.md) |
| Content | [Presentation assets](content/README.md) |
| Tests | [Validation and system boundaries](tests/README.md) |
| Development | [Maturity/gates](development/README.md), [modules](development/modules/README.md) |
| Production | [Lifecycle status](production/README.md) |
| Platform | [Integration targets](platform/README.md) |
| Releases | [Release boundary](releases/README.md) |
| Provenance | [History](provenance/README.md), [checkpoint 0004](provenance/checkpoints/0004-repository-normalization.md) |
| Inbox | [Local-only intake workflow](CONTRIBUTING.md) — _inbox/ is ignored |

## Authority flow

DESIGN defines behavior → DATA encodes it → GAME implements it → TESTS verifies it. Mathematics determines legality; constitutions govern process. Development tracks readiness, provenance preserves history, content supplies presentation and platform supplies integration. No downstream layer silently redefines upstream decisions.

Use the [cross-layer authority map](data/manifests/authority-map.json) to navigate systems. Legacy paths are concise redirects for historical links, not competing specifications.

## Verify this repository

```sh
node tools/validators/validate-bootstrap.mjs
node tools/validators/validate-design-state.mjs
node tools/validators/validate-normalization.mjs
node tools/validators/validate-continuity.mjs
node tools/validators/validate-cycle1-import.mjs
node tools/validators/validate-full-migration.mjs
node --test tests/regression/*.test.mjs
```

Node 24+ and Git required; Git LFS hydrates the preserved Propagation research archive. Checks verify structure, preserved design data, migration and provenance; they do not validate QMO mathematics, gameplay balance, final timing, rendering, AI or multiplayer correctness. No game launch command exists.

## Continue from current state

Start with [Genesis Horizon board](design/game/board/SYSTEM.md), [Field Generator configuration](design/topology/field_generators/SYSTEM.md), [foundational backlog](development/FOUNDATIONAL_BACKLOG.md), and [Propagation source boundary](mathematics/propagation/README.md). The originating-thread material is reconciled in the [continuity audit](provenance/audits/final-continuity-import.md). Mathematical integration and gameplay remain unimplemented. Git LFS retrieves the full source archive; readable current specifications and key source extracts are ordinary Git files.

Continuity verification: `node tools/validators/validate-continuity.mjs` checks recovered structure and source integrity, not external mathematics.


## Recovered original Cycle-1 data

The four original source archives, 120 FG records, complete 2,094-object atlas, all 1,770 base-pair relations, compatibility, Cycle Generation Constitution and 60 base RenderSpecs are now in Git. Start with [queries and data paths](data/qmo/README.md), [import audit](provenance/audits/cycle1-source-import.md) and [Live Model reconciliation](provenance/decisions/cycle1-source-import.md). Newer game design remains authoritative. No Cycle-1 mathematics was regenerated or fabricated; gameplay remains unimplemented.


## Latest accepted design — 2026-09-29

Cycle 1 has **185 ordinary identities: 120 FG + 14 Prime + 51 Utility**. The [Prime constitution](design/cards/cycle_01/primes/SYSTEM.md), [White Restore Prime](design/cards/cycle_01/utilities/restore_prime/SYSTEM.md), [mutable Configuration Spaces](design/topology/sandbox/SYSTEM.md), [fixed top-down FG interaction](design/topology/field_generators/SYSTEM.md), [merge semantics](design/topology/fusion/SYSTEM.md), and [Genesis runtime direction](design/game/GAME_DESIGN_DOCUMENT.md) are reconciled into current design/data. Original QMO data is unchanged. [Full migration audit](provenance/audits/full-migration-2026-09-29.md), [remaining backlog](development/FOUNDATIONAL_BACKLOG.md).
