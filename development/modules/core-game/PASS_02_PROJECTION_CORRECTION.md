# Pass-2 Vera projection correction

Finding: V-P2-01. Status: LOCAL_VALIDATION_PASSED; fresh distribution and delivery checks pending. Date: 2026-09-30.
Branch: `codex/raeon-pass-02`. Starting local/remote SHA:
`8a20961b97b0bbb6e2e257d3c3ff62992ea6d839`.
Main must remain `69a0030805b8c3858c877a514e2f50644421115a`, unmerged.
Whole-game phase remains PREPRODUCTION; host-reference scope only.

## Reproduction and correction

The unchanged submitted audit ZIP is preserved in
`provenance/imports/raeon-pass-02/vera-audit/`. Its SHA-256 is
`f905881398b527f76221e2a7c3fa0fc423b3a55969432f23dbda4d8d6dd4ead4`.
All ten payload files matched the package manifest before execution.
The audit's historical excerpt probes remain historical evidence, not native tests.

Three new production-package integration methods reproduced all three failures
against the starting binding code: three methods, six failed player subcases,
zero errors, expected failing test exit 1. The preserved reproduction transcript and
JSON are alongside the ZIP (LF line endings, trailing whitespace removed; raw
runtime log retained under the ignored baseline directory). Previous complete-suite evidence remains separately
under `build/genesis_runtime/vera-pre-correction/`; its green mapped acceptance
did not cover or disprove these privacy defects.

Both application and live-collection projection now use the selected manifest
view's effective private owner. A private-capable actor selecting `public`
receives a public projection. Both relationship passes use the same predicate,
including the `private_to` recipient restriction. Public dynamic spaces, card
copies and their admitted containment edges continue to appear.

Inspections retain actor and semantic revision checks and now store and match
application, selected view and owner scope. An inspection requires a private
recipient context at admission; a rejected public request does not consume its
grant or alter State. Unscoped records cannot be projected. Normal private
inspection, reconnect, corrected checkpoint restore and later-revision expiry
are exercised. Observation does not mutate semantic State, root, revision or
authoritative collection values; normal native observation routing remains.

Only `application.py` and `collections.py` change runtime behavior. Genesis,
the RAEON application package, Hypervisor and canonical design/data remain
unchanged. The additive exact-source amendment is
`provenance/decisions/raeon-pass-02-projection-correction.json`; earlier source
decisions and acceptance specifications are retained verbatim.

Existing checkpoint integrity binds exact Python source. Older nonempty
checkpoints therefore fail the pre-existing binding-contract check on the
corrected runtime; no automatic migration or invented inspection scope is
claimed. Corrected-runtime checkpoints retain their authorized scope.

## Verification

Eight separate real integration regressions cover both roles, owner/opponent/
public projections, trusted actors with multiple views, non-private public
sessions after inspection, HELLO/SNAPSHOT, SYNC_REQUEST, DELTA, reconnect,
checkpoint restore, later-revision expiry, and public geometry controls.
Four additional repository regressions verify the correction integrity record
and reject modified bindings, evidence or decision bytes. All previous tests
and the runtime 74 / Pass-2 83 acceptance denominators are retained.

Verified so far: all eight new integration methods; all seven repository
validators; 215 repository regressions (211 retained + four correction integrity
cases); 17 gameplay-design tests; 36 compiled sources with deterministic rebuild;
and the established mixed-dialect positive/negative checks. All 55 existing
test files and both original acceptance specifications are byte-for-byte unchanged.
The 36-source build evidence equals the pre-correction build evidence.

Full tests now pass: six unit and 64 integration (all 56 previous methods plus
eight correction regressions), with zero failures/errors. All 13 pinned upstream
suites pass. Fresh distribution verification, artifact hashes and final
local/remote commit evidence remain pending. Generated evidence is under `build/genesis_runtime/evidence/`.
No native device/SDK execution, architecture redesign, new gameplay policy,
Cycle-1 mathematics or main merge is authorized or claimed by this correction.
