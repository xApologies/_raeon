# Audit 0004 — Repository normalization

Date: 2026-09-28. Starting branch/commit: design/cumulative-recovery-0003 @ 6e5bd716160f41cb4225a60a5ef3127cffcc1f84. Working branch: architecture/repository-normalization-0004.

## Before inventory and findings

Recursively read/classified all 192 tracked source files before editing. [Before inventory](0004-before-inventory.json) records category, placeholder flag, size and SHA-256 for each file; 85 were generic placeholders. Categories cover governance, production, development status, design, mathematics, data, runtime boundaries, content, tooling, tests, platform and provenance. _inbox ZIP was inspected separately and remains local-only.

Findings: accepted-state.json held nearly all detailed machine state (29,568 bytes); Utility prose was one monolith; accepted rules and module checkpoint notes repeated current rules; card/topology/runtime/test scaffold areas lacked system navigation; generic OPEN boundary text obscured structurally accepted Utility state. Historical source/checkpoint prose was discoverable more readily than primary current specifications.

## Migration plan executed

1. Preserve governance/root spine/history; snapshot pre-migration semantic data and design prose.
2. Assign one current-specification home per system; split Utilities and Black material; consolidate broad overviews into links.
3. Encode identical values in per-system JSON and six family datasets; keep accepted-state high-level.
4. Populate implementation/test navigation without code or fake tests; replace module rule copies with status/gate dashboards.
5. Migrate existing validators/tests; verify lossless data, original family prose, authority markers, links and historical hashes.

[Migration map](0004-migration-map.json) lists content relocations, splits and consolidations. Relocations retain tiny old-path redirects so historical documents are not edited. Git may classify these as additions/modifications rather than physical renames; the semantic move ledger is explicit. No accepted structured data was deleted merely because prose exists.

## After tree and authority

[Complete final tree](0004-final-tree.md) shows retained top-level spine and normalized design/data/game/tests boundaries. [Authority map](../../data/manifests/authority-map.json) names unique current homes and 27 cross-layer dashboards. Old rule aggregates/module copies no longer act as authorities. DESIGN → DATA → GAME → TESTS; mathematics governs legality. Provenance remains history, development remains readiness.

## Proof of preservation

The normalization validator reconstructs all schema-3 semantic values from current datasets and deep-compares them with [before state](0004-before-state.json), excluding only schema/checkpoint metadata. Six Utility specifications retain their original family section prose verbatim. All prior provenance under decisions/checkpoints/sources/audits, prior development checkpoints, constitutions, pipeline and phase registry are hash-checked against the before inventory. The original [design snapshot](0004-before-design.json) is historical audit evidence, never a competing current specification.

Existing numerical/rule regressions remain active against normalized data; no values, catalogs, statuses or source requirements are relaxed to pass migration. Link checks include retained historical Markdown. Historical source attachments are integrity-checked and never executed. Schema migration is documented at [schema 4](../../data/schemas/ACCEPTED_STATE_V4.md).

## Results and limits

Validation passed: 2,194 bootstrap checks, 1,835 design checks, 1,885 normalization checks, 85 regression tests and git diff --check. Final inventory: 295 files; 103 added, 93 modified, 0 deleted; five content relocations with redirects and six Utility family splits. Exact commands and evidence are recorded in [checkpoint](../checkpoints/0004-repository-normalization.md) after execution. No pre-existing uncommitted changes or source-branch divergence found. No mechanical conflicts resolved by invention. Whole-game phase stays PREPRODUCTION; module statuses/gates unchanged. Validation does not prove mathematical closure, balance, final timing, rendering, AI or multiplayer correctness.
