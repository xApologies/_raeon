# raeon.

Canonical game-development repository: https://github.com/xApologies/_raeon

**Current whole-game phase: PREPRODUCTION.** Substantial mathematical/system prototypes exist externally and await import. This bootstrap establishes boundaries, high-level rules, and repository validation; it is not a playable prototype.

**THE MATHEMATICS IS THE PERMISSION SYSTEM.** The QMO is the canonical mathematical game object.

## Start here

- [Project constitution](PROJECT_CONSTITUTION.md) and [development constitution](DEVELOPMENT_CONSTITUTION.md)
- [Contribution/inbox workflow](CONTRIBUTING.md)
- [Accepted rules](design/game/ACCEPTED_RULES.md) and [structured state](data/manifests/accepted-state.json)
- [Lifecycle](production/README.md), [pipeline](development/PIPELINE.md), [modules](development/modules/README.md)
- [Bootstrap inventory](provenance/audits/bootstrap-inventory.md) and [decision](provenance/decisions/0001-repository-bootstrap.md)

## Boundaries

| Directory | Responsibility |
| --- | --- |
| production/ | Concept through postlaunch gates |
| development/ | Modules, milestones, build channels, checkpoints |
| design/ | Player-facing/product design |
| mathematics/ | Authoritative formal sources |
| game/ | Future executable runtime |
| content/ | Presentation assets |
| data/ | Structured truth, schemas, manifests |
| tools/ | Validation and future tooling |
| tests/ | Meaningful evidence; bootstrap invariants only today |
| platform/ | Shared, Windows desktop, secondary iPadOS |
| releases/ | Release records/artifact identities |
| provenance/ | Sources, decisions, checkpoints, audits |
| _inbox/ | Local-only ignored transfer boundary |

## Validate

With Node and Git available, from the repository root:

```sh
node tools/validators/validate-bootstrap.mjs
```

Checks cover repository/bootstrap invariants only, not Genesis/Chirality mathematics, QMO closure correctness, gameplay balance, Blender geometry, GPU rendering, multiplayer correctness, or AI correctness. No game build or launch command exists yet.

This standalone project uses no other repository's material. Missing mathematics, QMO objects, and RenderSpec/API packages remain SOURCE_IMPORT_REQUIRED; unresolved designs remain OPEN.
