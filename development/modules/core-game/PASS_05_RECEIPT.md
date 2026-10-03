# Pass-05 receipt

PASS — 140/140 mandatory cases; FAIL 0; BLOCKED 0. Every positive gameplay case is backed by executed native integration evidence. OPEN guards preserve the supplied boundary.

## Exact implementation snapshot

- Branch: `codex/raeon-pass-05`.
- Sealed base: `63771ab37dfec9a0c9de907c60f6f8b2f7a3f670`.
- Implementation commit and verified remote SHA: `0889e5eccd45d2019c71ac6de35edd31b5becf27`.
- Executable/authority digest: `4733bdecbc397a8a4a2c260d1d449594393cb40d348caee143b43dca112061ea`.
- Pouch SHA-256: `d0c8a763eb0a4901a118611742a8abfd0075227f4f0ad1b3bba4784eead8830a`.
- Main, unchanged and unmerged: `69a0030805b8c3858c877a514e2f50644421115a`.
- Implementation audit SHA-256: `9ebf19b696073e08593ed0c2a58175f04c13e37034b6910838cc42459c69a7e2`.

This committed receipt identifies the validated implementation and its exact archives. A Git commit cannot contain its own hash. The subsequent documentation seal and its matching remote SHA are recorded exactly by the local post-seal audit at `build/genesis_runtime/evidence/pass-05-acceptance.json` and the final delivery message. Regenerate that audit with `tools/genesis_runtime.py audit` under the documented qualified host after reproducing the required evidence. No executable source changes are part of the documentation seal.

The preserved local implementation audit at `build/pass05-0889e5e-validated/evidence/pass-05-acceptance.json` and adjacent evidence files retain the exact implementation hashes recorded in progress when the live audit files are updated for the documentation seal.

## Actual validation

Local: 6 unit tests, 136 integration cases, and 575 pinned upstream tests passed. The integration suite includes the actual 60-manifold witness execution and the exact authority-pointer audit regression. All seven repository validators, 252 repository regressions, 17 gameplay specifications, dialect checks, and `git diff --check` passed. Deterministic compilation verified 60 Genesis sources, preserving all 46 inherited source and bytecode commitments.

Fresh offline extraction passed 6 unit and 136 integration cases, every inherited scene and the new match scene, missing-dependency/QMO/Pass-04/Pass-05 input negatives, physical-path bytecode equality, and explicit Git/network/original-checkout isolation probes. The genuine sealed Pass-04 checkpoint fixture migrated without reading the source checkout at runtime. The final local acceptance totals are runtime 74/74, Pass 2 83/83, privacy 8/8, Pass 3 98/98, Pass 3B 85/85, Pass 4 108/108, and Pass 5 140/140.

The [progress record](PASS_05_PROGRESS.json) contains every mandatory case, its evidence mapping, all 79 changed file names, implementation file hashes, test totals, archive identities and evidence hashes. Final documentation-file hashes are in the post-seal audit. The 67 inherited test/fixture hashes, all 11 original QMO hashes, catalog bytes, and sealed Pass-04 receipts remain unchanged.

## Offline archives

Both archives identify implementation commit `0889e5eccd45d2019c71ac6de35edd31b5becf27` and were verified together from a fresh extraction. Python 3.12 on the documented Windows host remains an explicit prerequisite. The bundle contains the pinned selected runtime sources; it does not depend on either original repository or Git at runtime.

- `genesis-horizon-0.5.0.zip`: SHA-256 `0155b3dd25ac73b2d560f326ac292c624dd57e0241c989338f8b486c7fe4dbf5`, 26533437 bytes.
- `raeon-python-hypervisor-0.5.0.zip`: SHA-256 `1dbae7c0ee79b52472ec8bf6af28960d09bdf6e1fddd318ae221df8dfd06c7fd`, 17404 bytes.

## Remaining OPEN scope

Whole-game status: PREPRODUCTION. All unaccepted module gates remain unchanged. HOST-RUNTIME-001 remains OPEN_QUALIFIED: native evidence used CPython 3.12.10, the default allocator and processor mask 65536. Unrestricted Windows native-runtime lifetime stability and native device/presentation tests are not claimed.

- P5-OPEN-001 — mulligan procedure.
- P5-OPEN-002 — second-player compensation timing/name.
- P5-OPEN-003 — hand overflow.
- P5-OPEN-004 — defense timer duration.
- P5-OPEN-005 — simultaneous terminal resolution.
- P5-OPEN-006 — deck exhaustion target law.
- P5-OPEN-007 — deck exhaustion stage 7+.
- P5-OPEN-008 — generic Utility timing.
- P5-OPEN-009 — temporary Configuration Space expiry.
- P5-OPEN-010 — derived-field additions and splitting.
- P5-OPEN-011 — recursive fusion/emergence.
- P5-OPEN-012 — derived/emergent production cadence.
- P5-OPEN-013 — match timer.
- P5-OPEN-014 — native presentation.
- P5-OPEN-015 — HOST-RUNTIME-001.
- P5-OPEN-016 — final Utility catalog.

`_bricked` remained read-only at `c89676fc26000ae6f5fdad66a56e118b285d9b1d`; execution used ignored dependency copies. Main was not merged. Implementation and delivery are ready for Vera's independent audit after the documented seal is pushed and its audit passes.
