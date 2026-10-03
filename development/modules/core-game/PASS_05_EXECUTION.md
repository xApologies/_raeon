# Pass-05 execution

Branch: `codex/raeon-pass-05`. Exact sealed base: `63771ab37dfec9a0c9de907c60f6f8b2f7a3f670`. Main remains `69a0030805b8c3858c877a514e2f50644421115a` and is not merged.

Pouch SHA-256: `d0c8a763eb0a4901a118611742a8abfd0075227f4f0ad1b3bba4784eead8830a`. The archive and bundled verifier were independently checked after the interrupted entry. See [imported authority](../../../provenance/imports/raeon-pass-05/handoff/CODEX_EXECUTION_PLAN.md), [140 mandatory cases](../../../provenance/imports/raeon-pass-05/handoff/PASS_05_ACCEPTANCE.json), and [fresh entry evidence](../../../provenance/imports/raeon-pass-05/entry.json).

## Fresh entry gate

The checkout was clean at the exact sealed Pass-04 SHA. No prior Pass-05 branch or substantive changes existed. Verify, full tests, dialect checks, repository checks, fresh offline distribution verification, and final audit all exited zero before any tracked edit. Acceptance totals: runtime74/74, Pass2 83/83, privacy8/8, Pass3 98/98, Pass3B85/85, Pass4 108/108. Local and offline suites each passed 6 unit and 121 integration cases, including actual execution of all60 manifold witnesses. Repository checks passed 238 regressions and17 gameplay specifications. The inherited 67 test/fixture hashes and all11 QMO source hashes were captured.

## Current implementation contract

Current authority lives in [pass-05-runtime.json](../../../data/game/pass-05-runtime.json). Named canonical records link explicitly to it; their old values remain historical conformance inputs for unchanged tests. The source-derived 185 ordinary records and all51 Utility slots are preserved. Current adopted matches use H/N/R and reject old bounded-C/manual-refresh/authority bypasses.

Fourteen new Genesis handlers retain the established source syntax and real admission/transform/closure paths. `nodes.py` implements the pinned value ABI over verified native INT programs; `game/match/state.py` binds those declarations to the existing atomic State candidate. Color and card transport use the native Rainbow Road unit. Hypervisor remains game-agnostic.

Own-turn admission selects the owned live ordinary USED Fields, then invokes the preserved trusted Pass-04 refresh primitive. READY Fields, opponent Fields, intrinsic health, charge and topology are unchanged by that refresh.

Explicit checkpoint upgrade preserves the verified historical native root before a separate compiled migration. The self-contained migration fixture is a real checkpoint made by sealed Pass4, independently verified before implementation. Default checkpoint restore is not relaxed.

Generic Utility cost is zero. Real Hand source, effect-specific timing, target legality and mathematics remain required. No general Utility or compensation timing, mulligan procedure, overflow disposition, defense seconds, exhaustion target, post-Violet continuation, or simultaneous-terminal law is invented.

## Validation and delivery

The first implementation snapshot `b188a1bc569c25f4fdca6b4206774ccef5a4ac4e` passed the full local gate, but its fresh offline exhaustion scenario hit the unchanged 256 MiB native-storage bound after a committed action. Delivery and teardown reported backpressure. The deeper extraction path increased retained native resource metadata. That failed archive run is retained and is not final acceptance evidence. The new exhaustion fixture now accumulates admitted three-card transfers within the actual predecessor Hand capacity and retires those cards together; Pass-05 setup subsequently applies capacity ten. An initial fixture adjustment assuming capacity ten before setup was correctly rejected by the inherited capacity-seven guard and was corrected before final validation. Every card still moves through real native operations; every gameplay assertion, inherited test, runtime storage limit, and game rule is preserved. The corrected fixture requires fresh validation.

The corrected implementation then passed all six local unit tests, 135 integration cases, 575 upstream tests, and the complete fresh offline gate under the qualified host. Its exit audit identified legacy Pass-2/3 checks that rejected every changed path under broad design/data prefixes, including the five explicitly authorized Pass-05 authority pointers. The audit correction permits only those five exact before/after SHA-256 pairs, with sealed ancestry and the verified pouch required; all other protected paths remain forbidden. A new negative regression exercises wrong before/after hashes, case-altered paths, and corpus/design paths outside the amendment. Every inherited test remains unchanged. Archive review identified three design authority documents required by that regression; they were added to the exact bundle manifest before final validation. The preliminary local run was stopped and its partial output retained; it is not final PASS evidence. The revised audit tooling requires a new frozen-source validation and 136 integration cases.

Implementation validation is in progress. No Pass-05 case is claimed PASS by this execution description. Actual suites, compiler identities, per-case acceptance, changed-file hashes, implementation commit and final remote evidence will be recorded in [progress](PASS_05_PROGRESS.json) and [receipt](PASS_05_RECEIPT.md).

Whole game remains PREPRODUCTION. HOST-RUNTIME-001 remains OPEN_QUALIFIED under CPython3.12.10, default allocator and processor mask65536. No native device/presentation or unrestricted host-lifetime closure is claimed. `_bricked` remains read-only; all upstream tools execute only from ignored dependency copies.
