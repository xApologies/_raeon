# raeon.

Canonical repository: https://github.com/xApologies/_raeon

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
node --test tests/regression/*.test.mjs
```

Node and Git required. Checks verify structure, preserved design data, migration and provenance; they do not validate QMO mathematics, gameplay balance, final timing, rendering, AI or multiplayer correctness. No game launch command exists.
