# Full exhaustive migration audit — 2026-09-29

Starting main: `dff71b9504b36b2c49496932688ba5f00c10ab10`. Working branch: `codex/full-migration-2026-09-29`; accepted destination: `main`. Main was clean, fetched and pulled before edits. Push/default-checkout evidence is reported after integration.

## Source chain

Original full ZIP: `raeon_FULL_exhaustive_migration_2026-09-29.zip`, 242,064,399 bytes; SHA-256 `48d6ca53999cc06a27e309f3f51d4ba6cb5ed3ed65592781c6a21b5dfbb1d958`. The original is preserved through Git LFS, with the complete newest delta and entry directives also directly readable in ordinary Git. [Receipt](../sources/full-migration-2026-09-29/receipt.json).

All 15 outer-manifest entries and all 10 current-delta entries validate. Prior packages are byte-identical to previously imported uploads:

- ORIGINATING_THREAD_FULL_CONTINUITY_IMPORT.zip: 233,852,323 bytes; `e0942b2492612b5692ab2be12309b359ba6c58b73feb62a9716e4ffc98782da2`.
- AUTHORITATIVE_CYCLE1_SOURCE_IMPORT.zip: 8,187,872 bytes; `ebee1782caa972bca0db3ee11d07206bd81ed46866f01ee7613731eef9d1dc3f`.

Recursive inspection indexed 6,838 members across 244 distinct ZIP-named payloads, deduplicating identical nested archives by SHA-256. AppleDouble `__MACOSX/._*.zip` resource-fork files are metadata, not failed source ZIPs. JSON members parse. [Nested inventory](../sources/full-migration-2026-09-29/nested-inventory.json), [archive notes](../sources/full-migration-2026-09-29/nested-archive-notes.json), and [manifest inspection](../sources/full-migration-2026-09-29/manifest-inspection.json) preserve the inspection. Historic self-referential, relocated or prior-version manifests are not rewritten or falsely claimed to all match. Existing continuity and locked Cycle-1 validators still verify their canonical source identities.

## Reconciliation and preservation

The [decision](../decisions/full-migration-2026-09-29.md) maps every conflict and accepted resolution. Current ordinary identities are 185: 120 FG + 14 Prime + 51 Utility. The prior 50 Utility effects/data remain unchanged; White Restore Prime is additive. Fourteen structural Prime identities and accepted health/charge orders are now machine-readable. Final printed IDs are not invented.

Persistent Configuration Spaces own contents, XY positions, 3D orientations, closure and resolved field state; adding an FG reopens a resolved space. Temporary capacity remains a maximum independent of current field color. Detailed FG interaction is fixed top-down XY + 3D orientation with presentation-only partial relationship feedback. Merge preserves combined contents and trades two independent spaces for one; deterministic fusion/emergence retain QMO admission and support rules. Genesis runtime direction is recorded without implementation claims.

Original 120 FG records, 60 base + 343 fusion + 1,691 emergent = 2,094 atlas objects, compatibility, all 1,770 pair relations, database, RenderSpecs, original archives, Black data and all previous historical checkpoints remain unchanged. Preservation compares against the [starting file hashes](full-migration-2026-09-29-baseline.json). No Cycle-1 mathematics or dataset was regenerated.

Existing schema-4 authority flow remains DESIGN → DATA → GAME → TESTS. [Machine manifest](../../data/manifests/full-migration-2026-09-29.json) and [13 explicit semantic amendments](full-migration-2026-09-29-semantic-changes.json) record the accepted changes. Baseline comparisons verify new values against this pinned contract before projecting only approved fields; unrelated changes remain errors.

## OPEN items

Turn/match sequencing, victory/loss, starting hand/Prime H-C, overflow, exact targeting/timing, final printed card IDs/names/flavor/wording, unresolved Utility ranks, gesture/layout tuning, merged-domain capacity/runtime admission, permanent-base accounting/split behavior, balance, VM/platform/render integration, AI/multiplayer/economy and release remain OPEN. Existing missing theoretical/source categories remain unchanged. Black mechanics remain separate and unchanged.

Whole-game phase remains PREPRODUCTION. No gameplay, Genesis VM or renderer implementation is claimed.

## Validation and file ledger

All six validators passed, including continuity and source-import validation. All 162 regression tests passed, with zero failures, skips or cancellations. The prior 119 regressions remain active; 43 new tests cover accepted design changes, source integrity and rejection of unauthorized amendments.

| Command | Result |
| --- | --- |
| `node tools/validators/validate-bootstrap.mjs` | PASS |
| `node tools/validators/validate-design-state.mjs` | PASS |
| `node tools/validators/validate-normalization.mjs` | PASS |
| `node tools/validators/validate-continuity.mjs` | PASS |
| `node tools/validators/validate-cycle1-import.mjs` | PASS — 100,085 checks; original source/FG/atlas integrity unchanged |
| `node tools/validators/validate-full-migration.mjs` | PASS — 457 checks with hydrated full source archive |
| `node --test tests/regression/*.test.mjs` | PASS — 162 tests |
| `git diff --check` | PASS |

The full archive is stored through Git LFS. Fresh checkout verification hydrates and rechecks its bytes; an intentionally unhydrated checkout can validate the exact LFS identity but cannot claim full payload verification. These checks establish source consistency and accepted design representation, not gameplay implementation or theoretical proof. [Created/modified/moved/deleted files](full-migration-2026-09-29-files.json) record the complete change set; no new repository architecture is created.
