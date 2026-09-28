# Decision 0004 — Repository normalization

Date: 2026-09-28. Source branch: design/cumulative-recovery-0003. Working branch: architecture/repository-normalization-0004. Starting SHA: 6e5bd716160f41cb4225a60a5ef3127cffcc1f84. Ending SHA is the commit containing [checkpoint 0004](../checkpoints/0004-repository-normalization.md). Source: [authorized ZIP directive](../sources/0004-CODEX_PROMPT.md), [source integrity](../sources/0004-handoff.json).

## Decision

Preserve the root spine and constitutions. Give each system one current design home and explicit cross-layer navigation. DESIGN defines game behavior; MATHEMATICS determines legality; DATA encodes accepted decisions; GAME implements them; TESTS verifies them. DEVELOPMENT tracks maturity/status/gates; PROVENANCE records history; CONTENT supplies assets; PLATFORM supplies integration. No layer silently redefines upstream authority.

Split the Utility monolith into overview plus six specifications; split Black overview/concepts/support/mode into coherent homes. Broad rules and development note copies become indexes/dashboard links. Retain old-path stubs where historical links need them; these contain no rules.

Split accepted-state schema 3 into schema-4 high-level pointers plus per-system datasets. A read-only adapter reconstructs the prior semantic shape for preserved invariant checks. Compare every value against the starting-state snapshot; only schema/checkpoint metadata changes. Final Utility IDs/catalogs, values, timings and missing sources are not resolved here.

## Scope and status

PREPRODUCTION before/after. Utilities DESIGN; other modules OPEN; all gate acceptance remains unchanged. No game/AI/network/rendering/Blender/QMO implementation. No mechanics or balance changed. Root governance and historical provenance/checkpoints remain intact.

See [audit](../audits/0004-repository-normalization.md), [migration map](../audits/0004-migration-map.json), and [file inventory](../../data/manifests/design-checkpoint-0004.json) for relocations, splits, added/modified/deleted paths and proof.

Next task recommendation only: agree deterministic Utility ordering/working IDs without inventing unresolved card details. Not executed.
