# Contributing to raeon.

main → temporary working branch when needed → validate → authorized merge into main → delete temporary branch. Main is the sole canonical development tree; branches are disposable working surfaces, not permanent project organization.

## Local inbox workflow

_inbox/ is local-only transfer storage for ChatGPT/Codex handoffs, ZIPs, generated artifacts, recovery packages, source imports, Blender handoffs, temporary files. It is never canonical and must never be committed.

Inspect → classify → validate → import into proper boundary → meaningful provenance record → test → accepted Git state on main. Inspect package contents, destination paths, source identity, and authority before extraction. Do not execute unreviewed intake scripts or import another repository's material. Reject paths outside the intended destination; inspect and preserve meaningful files before replacement.

A source record includes identifier/origin, supplied authority, receipt date, package hash where applicable, destination, permission/license where applicable, and conflicts. Distinguish GAME_CANON from PROVISIONAL/OPEN. SOURCE_IMPORT_REQUIRED persists until authoritative material is imported and reviewed. Keep temporary/excluded content local.

## Development and validation

1. Start from up-to-date main; create a temporary working branch when needed.
2. Assign a module and [pipeline](development/PIPELINE.md), applicable gates, and dependency evidence.
3. Import/implement reviewed material in the correct boundary. Update sources, structured state, docs, inventories together.
4. Run relevant checks: `node tools/validators/validate-bootstrap.mjs` and `node tools/validators/validate-design-state.mjs`. Also run `node tools/validators/validate-normalization.mjs`. Validator regressions: `node --test tests/regression/*.test.mjs`. Node with ES modules and Git are required; bootstrap tested with Node 24.
5. Integrate dependencies; record actual results, limitations, source/artifact revisions.
6. Record validation in the commit or review. Create a numbered checkpoint only when it carries substantive design, source, mathematical, milestone or migration evidence; ordinary commits and Git operations do not require one. Preserve useful historical records. Review `git status --short`, `git diff --check`, staged changes; never force-add inbox or compiled/cache files.
7. Commit and submit for acceptance. Merge into main when authorized, verify the accepted state there, then delete the temporary branch only after its required commits are reachable from main. Never force-push for routine promotion.

Chat threads and Codex sessions are workspaces, not canonical storage. The Git repository is canonical storage. Future Cycles follow [Cycle production](design/cards/CYCLE_PRODUCTION.md).
