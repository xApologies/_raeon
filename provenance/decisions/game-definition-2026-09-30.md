# Game-definition reconciliation — 2026-09-30

Authority: GAME_CANON for explicitly accepted package rules. Whole-game PREPRODUCTION; implementation and production gates remain OPEN. This is the single decision/checkpoint and audit for this reconciliation. The matching [machine receipt and exact amendment ledger](game-definition-2026-09-30.json) is evidence, not a parallel current specification.

## Receipt, baseline and disposition

User request: execute CODEX_PROMPT inside RAEON_GIT_UPDATE_PACKAGE_2026-09-30.zip. Read every member, including all cumulative development/rules files, before editing. The concise GIT_RECONCILIATION_AUTHORITY.md governs integration; later explicit locks supersede older OPEN statements in the cumulative models.

- Repository: xApologies/_raeon.
- Starting main, package baseline and verified remote default HEAD: `69a0030805b8c3858c877a514e2f50644421115a`.
- Working branch: `codex/game-definition-2026-09-30`, created after `git pull --ff-only origin main` returned Already up to date.
- Package: 40,204 bytes; SHA-256 `25804fe4d58c8bce15c455e0f16aab7936954f092e8788fb3eddab0aae74aed4`.
- Development model ZIP SHA-256: `5fcc5e4f0afcfdc20bb5064c8f9def69c16c88bf6248e57cfb707d221e01706e`.
- Rules model ZIP SHA-256: `f326694464f9d70a14ab1b720138b42b0ef87694c796c740044c9d99afd6371a`.
- Verified all 5 outer manifest entries, all 22 development-model entries and all 3 rules-model entries (sizes and SHA-256). Two nested manifests also parsed. The source receipt inside the development model names earlier upstream archives; those are citations, not newly verified imports.
- Transfer ZIPs and unpacked model trees stay outside Git. No other repository was read or modified. No Genesis grammar, VM integration or source conformance was claimed.
- Commit this reviewed work on the working branch. The directive does not authorize merging this change to main; main remains canonical and unchanged. No push is required by this prompt. The enclosing Git commit supplies the ending SHA without a self-referential hash in this document.

## Accepted deltas and canonical homes

| Accepted state | Existing authoritative homes |
| --- | --- |
| Persistent identity-bearing card Geometrics; card-only ordered Deck/Hand/Graveyard; ports distinct from containers; atomic admitted movement; normal Hand capacity 7 | design/game/board, design/cards/CARD_SYSTEM.md; data/board/genesis-horizon.json; data/game/match.json |
| Permanent A/B/C plus up to six additional spaces, at most nine active; live State workspace outside QMO corpus; both membership and admitted XY/3D orientation required | design/topology/sandbox and field_generators; corresponding data/topology and FG interaction data |
| Native topology identity separate from mutable current color; restoration capped at native maximum; zero destroys field and routes supporting FG identities to Graveyard | design/topology/sandbox; data/topology/configuration-spaces.json |
| Merge preserves FG identities and reduces two independent spaces to one; pairwise emergence consumes zero slots, can coexist and remains dependent/non-targetable | design/topology/fusion and emergent_fields; data/topology/relationships.json |
| Normal Prime H_max/0 start; four operational states; damaged Prime cannot operate; partial C spending, shield, family limits and charge-limited reuse | design/cards/cycle_01/primes; data/cycles/cycle_01/primes/working-model.json |
| READY generates current color once, becomes USED without unresolving; availability persists ACTIVE into DEFENSE; ACTIVE friendly Restore/hostile Degrade; DEFENSE friendly Restore only; Universal obeys window | design/game/match and transduction; data/game/match.json and configuration-spaces.json |
| Existing Rainbow Road color transport; ordinary hostile field actions go through Primes; State/Nexus/Shell/SEA ownership and external Python boundary | design/game/GAME_DESIGN_DOCUMENT.md and transduction; data/platform/runtime-direction.json |

GAME module READMEs now expose the corresponding contracts; they remain OPEN / UNIMPLEMENTED. Test-only deterministic examples live under the existing tests/gameplay hierarchy. There is no executable Genesis source or new repository architecture. DESIGN → DATA → GAME → TESTS remains intact, with mathematical legality upstream of all layers.

## Supersession and conflicts

1. Prior Hand maximum OPEN becomes normal capacity 7. Starting hand, overflow, short-deck handling and multi-card effect resolution stay OPEN. Only `hand_size_maximum` changes in the six original Utility family datasets; all 50 effects/counts/ranks and the additive White Restore Prime are preserved. The old Draw/Deck sentence is amended in place, with its exact historical text retained in the decision ledger.
2. Prime starting H/C OPEN becomes H=H_max,C=0. The older v0.6 recovery file's instruction to retain OPEN is superseded by the concise authority and rules R10. Overflow and detailed targeting/timing remain OPEN.
3. Earlier model language left all field expenditure OPEN. Later v0.7/R19–R25 accepts READY/USED and direction/side limits. Exact refresh boundary, partial/all-at-once output allocation and Emergent cadence remain unresolved; no end-of-ACTIVE refresh is added.
4. An early transport pseudocode requires an ACTIVE Prime without defining the four states. The later healthy/charged operational gate and ACTIVE/DEFENSE rules govern current contracts. Historical pseudocode is not executable source.
5. White reactivation still gives (1,0). The package's broad “further restoration” wording does not override H_max=rank: Red Universal is healthy but uncharged at (1,0); higher ranks remain damaged. All still require C>0 to operate.
6. Nine active spaces is a board maximum, not an FG capacity or solution to permanent-base identity accounting after merge. Existing permanent minimum and two-to-one independent-space cost are both preserved; their exact merged accounting/split remains OPEN.
7. “Configuration Region framework CLOSED” in source evidence does not advance repository module gates. No Configuration Frontier object is introduced. The visible Genesis Horizon divider and the machine/runtime Horizon are distinguished in board documentation.
8. Source statements about another repository's supported grammar are not independently verified here. Actual grammar validation is a future source gate; missing capabilities remain PROPOSED_EXTENSION. Existing SOURCE_IMPORT_REQUIRED categories are not cleared by architecture prose.
9. Corrected a stale ordinary “50-Utility set” reference in the current Black overview to 51; no Black mechanics changed. Prior dated manifests, sources, audits and checkpoint OPEN lists remain immutable history, superseded by current design/data and the current accepted-state pointer.

## Preservation and remaining OPEN scope

The baseline comparison found **301 selected catalog/mathematics/render/source/history files byte-identical**, including original imported catalogs and Constitution. Existing validators additionally protect earlier provenance and checkpoints. All **187 JSON files** parse. Catalog query returns 120 FGs, 60 base manifolds, 343 fusion-derived, 1,691 emergent, 2,094 atlas objects, 1,770 manifold pairs, 2,482 compatibility pairs and 60 supplied RenderSpecs. No source mathematics, pair relations or compatibility data was regenerated or rewritten. The ordinary identity count remains 185 = 120 + 14 + 51.

OPEN: exact READY/USED refresh boundary; action/reaction ordering and detailed timing/target windows; starting hand, normal draw cadence, first-player and mulligan; victory/loss, timer/exhaustion; Prime Restore overflow; temporary space expiry; merged ceiling/runtime admission/permanent-base accounting/split; field-destruction transaction ordering; output allocation/Emergent generation cadence; final metadata, balance, remaining Utility/Black details; executable Genesis, actual grammar/API/VM/platform integration. Existing unrelated OPEN/PROVISIONAL items remain in the [current accepted-state ledger](../../data/manifests/accepted-state.json).

SOURCE_IMPORT_REQUIRED is unchanged: Genesis mathematics; Chirality mathematics; Propagation mathematics; broader QMO definitions/API; broader closure operators; Transduction mathematics/API; Generator/derived RenderSpecs; unsupplied Blender Generator/derived geometry references; higher-dimensional projection mathematics. No recovered source item was falsely re-opened or absent item cleared.

## Validation evidence

Node v24.19.0 tooling. These commands test repository/source consistency and specification examples, not a production runtime, QMO mathematical proof, balance, rendering or multiplayer implementation.

| Exact command | Final result |
| --- | --- |
| `node tools/validators/validate-bootstrap.mjs` | PASS; 2,320 checks; PREPRODUCTION |
| `node tools/validators/validate-design-state.mjs` | PASS; 2,719 checks; 0 errors |
| `node tools/validators/validate-normalization.mjs` | PASS; 2,455 checks; 0 errors |
| `node tools/validators/validate-continuity.mjs` | PASS; 1,464 checks; 0 errors |
| `node tools/validators/validate-cycle1-import.mjs` | PASS; 100,085 checks; 0 errors |
| `node tools/validators/validate-full-migration.mjs` | PASS; 457 checks; 0 errors |
| `node tools/validators/validate-game-definition.mjs` | PASS; 55 checks; 0 errors |
| `node --test tests/regression/*.test.mjs` | PASS; 188 tests, 0 failed/skipped/todo |
| `node --test tests/gameplay/cards/*.test.mjs tests/gameplay/primes/*.test.mjs tests/gameplay/sandbox/*.test.mjs tests/gameplay/manifolds/*.test.mjs` | PASS; 17 tests, 0 failed/skipped/todo |
| `node tools/qmo/query-cycle1.mjs counts` | Counts above; PASS |
| `git diff --check` | PASS; exit 0, no output |
| `git diff --cached --check` | PASS; exit 0, no output |

The first full run correctly rejected new schema versions and amended GAME README hashes in older continuity/source guards (14 and 9 errors; two regression positives failed). Fixed by applying the same exact pinned before/after amendment checks, with no broad exclusion or disabled validator. The final suite retains negative tests against source tampering, invented mechanics and unrelated historical drift. The new focused examples cover all 14 Prime starts, all family/window/side combinations, partial reuse, damaged/inactive states, Hand overflow rejection, both closure gates, shared availability, native/current color, destruction routing, real imported emergence pairs and identity-preserving merge.

The pinned decision contains 7 assembled-state amendments and path-level amendments for 10 existing JSON files. Every changed current value is checked before historical projection; unamended values still face the previous checks. No validator is silenced. No package archive, cache, scratch script, generated asset or parallel source tree is committed.

## File audit

10 files created, 51 modified; none moved, renamed or deleted. Maintained current inventory: 615 files. The lists below include this coherent decision pair and validator/test changes; earlier inventories remain historical.

Created:

- `provenance/decisions/game-definition-2026-09-30.json`
- `provenance/decisions/game-definition-2026-09-30.md`
- `tests/gameplay/cards/containers.test.mjs`
- `tests/gameplay/manifolds/relationships.test.mjs`
- `tests/gameplay/primes/constitution.test.mjs`
- `tests/gameplay/rule-model.mjs`
- `tests/gameplay/sandbox/configuration.test.mjs`
- `tests/regression/game-definition.test.mjs`
- `tools/validators/game-definition-contract.mjs`
- `tools/validators/validate-game-definition.mjs`

Modified:

- `CHANGELOG.md`
- `data/board/genesis-horizon.json`
- `data/cycles/cycle_01/field_generators/interaction.json`
- `data/cycles/cycle_01/primes/working-model.json`
- `data/cycles/cycle_01/utilities/draw_deck.json`
- `data/game/match.json`
- `data/manifests/accepted-state.json`
- `data/manifests/authority-map.json`
- `data/manifests/current-files.json`
- `data/platform/runtime-direction.json`
- `data/schemas/ACCEPTED_STATE_V4.md`
- `data/topology/configuration-spaces.json`
- `data/topology/relationships.json`
- `design/cards/CARD_SYSTEM.md`
- `design/cards/black/SYSTEM.md`
- `design/cards/cycle_01/primes/SYSTEM.md`
- `design/cards/cycle_01/utilities/draw_deck/SYSTEM.md`
- `design/game/GAME_DESIGN_DOCUMENT.md`
- `design/game/board/SYSTEM.md`
- `design/game/match/SYSTEM.md`
- `design/topology/emergent_fields/SYSTEM.md`
- `design/topology/field_generators/SYSTEM.md`
- `design/topology/fusion/SYSTEM.md`
- `design/topology/sandbox/SYSTEM.md`
- `design/transduction/SYSTEM.md`
- `development/FOUNDATIONAL_BACKLOG.md`
- `game/board/README.md`
- `game/cards/README.md`
- `game/cards/generators/README.md`
- `game/cards/primes/README.md`
- `game/manifolds/README.md`
- `game/match/README.md`
- `game/sandbox/README.md`
- `game/state/README.md`
- `game/transduction/README.md`
- `provenance/README.md`
- `tests/README.md`
- `tests/gameplay/README.md`
- `tests/gameplay/cards/README.md`
- `tests/gameplay/manifolds/README.md`
- `tests/gameplay/primes/README.md`
- `tests/gameplay/sandbox/README.md`
- `tests/regression/design-state-validator.test.mjs`
- `tests/regression/full-migration.test.mjs`
- `tools/validators/README.md`
- `tools/validators/full-migration-contract.mjs`
- `tools/validators/validate-continuity.mjs`
- `tools/validators/validate-cycle1-import.mjs`
- `tools/validators/validate-design-state.mjs`
- `tools/validators/validate-full-migration.mjs`
- `tools/validators/validate-normalization.mjs`
