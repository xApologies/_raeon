# RAEON Pass 1 receipt

Status: **COMPLETE** — production empty-match realization and its software proofs.
Repository: `xApologies/_raeon`. Branch: `codex/raeon-pass-01`. Date: 2026-09-30.
Whole-game phase remains **PREPRODUCTION**; unaccepted module gates are unchanged.

## Git identities

Starting SHA: `71b3a3fbdbce7eece25076a0fd303887cc70d4f1`.
Implementation ending SHA and verified remote SHA:
`f7b312099a518b42d42775fb84db32a1b5d825c9`.
The closing commit changes only this maintained Markdown/JSON receipt and corrects
the historical upstream test-count arithmetic. Its exact ending/remote SHAs,
clean worktree and unmerged-main proof are resolved after push in
`build/genesis_runtime/evidence/pass-01-acceptance.json`. Reproduce with
`python -B tools/genesis_runtime.py audit`; resolve the receipt's own commit with
`git log -1 --format=%H -- development/modules/core-game/PASS_01_RECEIPT.json`.
A commit cannot embed its own hash inside its files.

Main started and remains `69a0030805b8c3858c877a514e2f50644421115a`. The audited
runtime milestone remains an ancestor. No main merge is authorized or performed.

## Production package and topology

[Manifest](../../../game/core/raeon/application/manifest.json): identity `raeon`,
version `0.1.0`, scope `PASS_01_EMPTY_MATCH`. Real compiled sources are
[raeon_realize.gen](../../../game/core/raeon/application/raeon_realize.gen) and
[raeon_observe.gen](../../../game/core/raeon/application/raeon_observe.gen).
The manifest hashes both programs and the bounded representation definitions.

Actual Genesis execution creates **37 native Geometrics**: one Match; two Players;
two Boards; ten distinct attachment roles; two each of Deck, Hand and Graveyard;
two Prime regions; two Configuration regions; six fixed Prime positions; six
permanent universal Configuration Spaces A/B/C. All contents are empty. There
are no cards or expansion spaces. **163 explicit relationships** comprise
State-to-Match containment plus 162 application ownership, containment,
attachment and visibility relationships.

Genesis creates every instance and relationship through the native engines.
Python validates the package, binds representations, filters projections and
atomically publishes one State successor after checking the actual native graph.
The existing finite engineering encoder is reused; this is not a Python-only
graph or new QMO/dimensional mathematics. All original nine runtime/conformance
Genesis sources remain unchanged; the additive guard pins two production sources.

Identities are unique, persistent and independent of screen coordinates. Owner
views expose their own empty container contents/order; opponent/public views hide
those private internals and private visibility relations. Neither snapshots nor
production operation receipts leak backend paths, resources or native receipt IDs.
Identical package realization is idempotent. Observation does not duplicate
topology or advance game revision.

The headless demonstration boots, realizes, binds both real Hypervisor sessions,
independently decodes HELLO/SNAPSHOT, checkpoints, closes, restarts/restores and
reconnects. Both views, all identities and the semantic root survive; the boundary
epoch changes. Game revision remains **0**. Native proof receipts stay in ignored
owner evidence, separate from player projections.

## Exact commands and results

Executed with Windows Python 3.12.14 and NumPy 2.3.5. Use the installed Python 3.12
interpreter as `python`, from repository root:

```text
python -B tools/genesis_runtime.py doctor
python -B tools/genesis_runtime.py dependencies verify
python -B tools/genesis_runtime.py build
python -B tools/genesis_runtime.py verify
python -B tools/genesis_runtime.py dialect-test
python -B tools/genesis_runtime.py demo --headless
python -B tools/genesis_runtime.py demo --headless --application raeon
python -B tools/genesis_runtime.py test
python -B tools/genesis_runtime.py repository-test
python -B tools/genesis_runtime.py package
python -B tools/genesis_runtime.py verify-distributions
python -B tools/genesis_runtime.py audit
git diff --check
```

- **1,075** locked dependency files verified; **11** Genesis sources compile,
  verify and rebuild byte-identically, including both production sources.
- **6 protocol + 34 integration = 40** tests pass. Integration comprises **18
  Pass-1** tests and the existing **16** runtime/archive tests.
- **575** upstream checks/tests across **13** suites pass. The thirteen actual
  logs sum to 575; the earlier execution note's 675 was an arithmetic overcount
  and is corrected. Original conformance demo and both dialect checks pass.
- All **7 validators**, **204 repository regressions**, **17 gameplay specification
  tests**, and `git diff --check` pass. Validator check counts: bootstrap 2,326;
  design 2,864; normalization 2,535; continuity 1,594; Cycle-1 integrity 100,085;
  full migration 457; game-definition 55.
- Existing runtime acceptance: **74/74 PASS**. All **38** pouch cases map to named
  tests or concrete build/demo/source/Git evidence. Final `audit` must report
  **38/38 PASS** after the closing receipt commit is pushed. Requirements retain
  their original NOT_RUN specification fields; outcomes are separate evidence.
- Fresh offline extraction verifies **1,202** exact archive payloads. All **10**
  installation/build/demo/test commands pass, including installed Hypervisor,
  both demos, deterministic rebuild, 6 unit and 34 integration tests.

`repository-test` executes the following commands (expanding test globs itself):

```text
node tools/validators/validate-bootstrap.mjs
node tools/validators/validate-design-state.mjs
node tools/validators/validate-normalization.mjs
node tools/validators/validate-continuity.mjs
node tools/validators/validate-cycle1-import.mjs
node tools/validators/validate-full-migration.mjs
node tools/validators/validate-game-definition.mjs
node --test tests/regression/*.test.mjs
node --test tests/gameplay/cards/*.test.mjs tests/gameplay/primes/*.test.mjs tests/gameplay/sandbox/*.test.mjs tests/gameplay/manifolds/*.test.mjs
git diff --check
```

## Negative tests and source integrity

Rejections cover unauthorized realization; package/source SHA tamper; root/source
path escapes; undeclared/malformed Genesis; duplicate/conflicting semantic and
native-definition IDs; duplicate instantiated bindings; missing/unapproved
relationships; application inheritance/instantiation of machine domains; wrong
owner/private-view authority; and exhausted execution budget. Injected failures
after candidate creation and immediately before publication preserve the prior
semantic root, native bindings and journal. Source guards also reject altered
Genesis, manifest, definitions, decision and inventory. Final review removed
native diagnostic IDs from production operation receipts; an independent byte
frame test proves the correction. No validator was suppressed.

The original pouch is preserved byte-for-byte; all **10** manifest payloads match.
The **120 Field Generator** corpus, **2,094-object atlas**, accepted design and
remaining SOURCE_IMPORT_REQUIRED entries are unchanged. `_bricked` remains clean
and read-only at `c89676fc26000ae6f5fdad66a56e118b285d9b1d`; only the ignored
isolated copy executes. See the [exact source amendment](../../../provenance/decisions/raeon-pass-01.json)
and [machine receipt](PASS_01_RECEIPT.json) for hashes, commands and changed files.
The pass adds 18 files and modifies 10; it moves/deletes no files.

## Evidence and distributions

Ignored evidence: `build/genesis_runtime/evidence/`, particularly `build.json`,
`verify.json`, `dependencies.json`, `tests-unit.json`, `tests-integration.json`,
`tests-source.json`, `upstream-tests.json`, `repository-validation.json`,
`pass-01-demo.json`, `acceptance.json`, `pass-01-acceptance.json`, `remote.json`,
`upstream-readonly.json` and `distribution-verification.json`, with command logs.
Archives use implementation commit `f7b312099a518b42d42775fb84db32a1b5d825c9`:

| Archive under build/genesis_runtime/distributions | Bytes | SHA-256 |
| --- | ---: | --- |
| genesis-horizon-0.1.0.zip | 17,552,311 | f14f148914f6e3108963955b74359f8582c3a31c0cd9f38507c147da74ed5c6d |
| raeon-python-hypervisor-0.1.0.zip | 17,297 | b6996e2c5f477cbb5bca35299298fd51607dbcac0c7aca4d956376b336edadc1 |

This remains the bounded Windows/Python native-engine reference deployment.
Higher-dimensional embeddings/coupling, native SDK/device certification and
hostile-code isolation are outside its claims. Whole-game phase is PREPRODUCTION.

## OPEN items and exact Pass-2 entry state

Starting hand, draw cadence, mulligan, first-player rule, turn phases,
action/reaction order, refresh boundary, targeting/effect timing, victory/loss,
timeout, overflow/destruction ordering and temporary-space expiry remain OPEN.
Cards, shuffle/draw/movement, field/QMO resolution, Prime arithmetic, color,
turns, combat, victory, UI, animation, Blender and native ports were not implemented.

Pass 2 starts from one empty realized `raeon` 0.1.0 Match in State, two semantic
player organizations and Boards, all required empty attachments/regions,
revision 0, validated owner/public projections and proven checkpoint/restart.
**OBSERVE is the only exported operation.** Later-pass work needs its own
scope; this checkpoint infers no missing rules and regenerates no Cycle-1 mathematics.
