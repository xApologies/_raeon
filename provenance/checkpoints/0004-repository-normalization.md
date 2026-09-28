# Checkpoint 0004 — Repository normalization

Date: 2026-09-28. Source branch: design/cumulative-recovery-0003. Working branch: architecture/repository-normalization-0004. Starting SHA: 6e5bd716160f41cb4225a60a5ef3127cffcc1f84. Ending SHA: resolve the containing checkpoint commit using `git log -1 --format=%H -- provenance/checkpoints/0004-repository-normalization.md` (a commit cannot embed its own hash).

## Result

System-oriented design specifications, split Utility/Black material, normalized machine datasets, linked runtime/test boundaries and maturity-only dashboards. [Authority map](../../data/manifests/authority-map.json) defines navigation; [schema migration](../../data/schemas/ACCEPTED_STATE_V4.md) explains schema 4. [Final trees](../audits/0004-final-tree.md) and [file inventory](../../data/manifests/design-checkpoint-0004.json) enumerate the result.

WHOLE-GAME PHASE REMAINS PREPRODUCTION.
NO GAMEPLAY MECHANICS WERE REDESIGNED BY THIS CHECKPOINT.
NO GAMEPLAY IMPLEMENTATION WAS CLAIMED BY THIS CHECKPOINT.

Module statuses unchanged: Utilities DESIGN, all others OPEN. No gate or phase newly accepted. All OPEN/source-import values preserved in the [state index](../../data/manifests/accepted-state.json).

## Evidence

[Decision](../decisions/0004-repository-normalization.md), [audit](../audits/0004-repository-normalization.md), before inventory/state/design snapshots and migration map record origin, relocation, losses prevented, and history preservation.

Validation completed successfully on 2026-09-28 (Node v24.19.0, Git 2.53.0.windows.3):

| Command | Result |
| --- | --- |
| `node tools/validators/validate-bootstrap.mjs` | PASS: 2,194 checks |
| `node tools/validators/validate-design-state.mjs` | PASS: 1,835 checks, 0 errors |
| `node tools/validators/validate-normalization.mjs` | PASS: 1,885 checks, 0 errors |
| `node --test tests/regression/bootstrap-validator.test.mjs tests/regression/design-state-validator.test.mjs tests/regression/normalization-validator.test.mjs` | PASS: 85 tests; 0 failures, skipped, cancelled or todo |
| `git diff --check` | PASS: no whitespace errors |

Final inventory: 295 files; 103 added, 93 modified, 0 deleted. Five content relocations retain old-path redirects (no physical Git renames); six Utility sections split into dedicated specifications. Complete path lists are in the linked file inventory and migration map. All original paths remain present; 99 original files remain unchanged. No source or mechanical conflict remains from this migration.

Migration audit: PASS. All prior accepted semantic values reconstruct exactly, original Utility family prose is retained, historical checkpoints/decisions/sources/audits 0001–0003 remain byte-identical, and current local Markdown links resolve. GAME_CANON, OPEN fields, all 15 SOURCE_IMPORT_REQUIRED categories, module maturity and gate acceptance are unchanged. Checks do not establish mathematical or gameplay correctness.

Publication target: origin/architecture/repository-normalization-0004; main is not merged. The final execution report provides the containing commit SHA and remote verification.

## Not performed

No Utility ID assignment, Prime catalog design, rule/price/balance selection, QMO/math import or reconstruction, graphics generation or runtime implementation. Existing unresolved timing, targeting, costs, UI, transport, AI and source artifacts remain unresolved. Recommendation: deterministic working Utility ordering/IDs as a separate authorized design task.
