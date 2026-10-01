# Pass-2 Vera projection correction

Finding: V-P2-01. Status: VERIFIED_SOFTWARE_SCOPE_COMPLETE. Date: 2026-09-30.
Branch: `codex/raeon-pass-02`. Starting local/remote SHA:
`8a20961b97b0bbb6e2e257d3c3ff62992ea6d839`.
Implementation/archive local/remote SHA (verified pushed): `7a9f073959af7bb41dd60bf5ddbb1e7176c7803b`.
Closing documentation SHA: current Git HEAD, independently recorded after final
push in `build/genesis_runtime/evidence/remote.json` and `pass-02-acceptance.json`.
The closing documentation commit preserves the executable/data identity below.
Main before/after: `69a0030805b8c3858c877a514e2f50644421115a`; unmerged.
Whole-game phase: PREPRODUCTION. Supported scope: Windows x64 Python host reference.
Native SDK/device execution: NOT_RUN; no such support is claimed.

## Reproduction and correction

The original submitted ZIP is preserved byte-for-byte at
`provenance/imports/raeon-pass-02/vera-audit/RAEON_PASS_02_VERA_AUDIT_2026-09-30.zip`.
SHA-256: `f905881398b527f76221e2a7c3fa0fc423b3a55969432f23dbda4d8d6dd4ead4`.
All ten payload files matched its manifest. Its excerpt probes remain historical
source-review evidence, not Genesis/GVM execution evidence.

Three actual CardFixture/Horizon/Hypervisor integration methods reproduced all
three reported failures against the starting production bindings: three methods,
six failed player subcases, zero errors, expected failing test exit 1. The
reproduction JSON, baseline binding hashes and transcript are preserved alongside
the ZIP. Transcript/JSON text uses LF and strips trailing whitespace; raw output
and previous complete-suite JSON remain under `build/genesis_runtime/vera-pre-correction/`.
The earlier green mapped acceptance did not cover or disprove these defects.

1. Application and live-collection projection now share the selected manifest
   view's effective private owner. A private-capable actor selecting public
   cannot reveal either player's Hand contents, identities or card objects.
2. Private inspection records retain actor/revision checks and additionally
   match application, selected view and owner context. Public inspection admission
   fails atomically without consuming its grant. Unscoped records cannot be projected.
   Normal owner inspection, reconnect, corrected checkpoint restore and expiry at
   a later semantic revision remain functional.
3. Both relationship passes use the same endpoint and `private_to` recipient
   predicate. The final live merge cannot restore private relationships filtered
   by the application stage. Public dynamic spaces, committed copies and their
   admitted containment edges remain visible and update through DELTA.

Only `application.py` and `collections.py` change runtime behavior. Genesis,
production RAEON package and Hypervisor code remain unchanged. Observation
preserves semantic State, root, revision and authoritative collection values;
normal native observation routing still executes.

The additive exact-source amendment is
`provenance/decisions/raeon-pass-02-projection-correction.json`. All previous
Genesis source decisions and original acceptance specifications are byte-for-byte
unchanged. Existing exact binding-contract checks reject pre-correction nonempty
checkpoints; no automatic migration or invented inspection scope is claimed.
Corrected-runtime checkpoints retain their authorized inspection scope.

## Validation and evidence

Executable/data identity: `3d2ce089938d06fee9ba607fe9e4bbd66e7c687f2890cf266da7fb703f84fc57`.
All 55 pre-existing test files remain byte-for-byte unchanged. The original
runtime 74 and Pass-2 83 denominators are preserved; the correction is a separate
8/8 result. Eight new integration methods exercise both player roles, owner/
opponent/public views, trusted multiview actors, non-private public sessions,
HELLO/SNAPSHOT, SYNC_REQUEST, DELTA, reconnect, checkpoint restore, revision expiry,
atomic refusal and public geometry controls. Four new repository cases validate
exact corrected source/evidence and reject modified bindings, evidence and decisions.

Commands use CPython 3.12.14 with `-X utf8 -B`, NumPy 2.3.5 and setuptools 84.0.0.
The entry point is `python tools/genesis_runtime.py` unless shown otherwise.

| Command | Verified result |
| --- | --- |
| `verify` | PASS: 36 compiled sources; native verification and deterministic rebuild; original build evidence unchanged |
| `dialect-test` | PASS: established positive and mixed-dialect negative cases |
| `test` | PASS: 6 unit + 64 integration (56 retained + 8 new); 575 upstream checks in 13 suites |
| `repository-test` | PASS: 7 validators, 215 repository regressions (211 retained + 4 new), 17 gameplay-design tests, whitespace check |
| `demo --headless` | PASS: original conformance scenario |
| `demo --headless --application raeon` | PASS: current empty board and historical Pass-1 package |
| `demo --headless --application raeon --scenario cards` | PASS: two-player native cards, nine spaces, checkpoint/restart |
| `package` | PASS: matching archives from clean committed source |
| `verify-distributions` | PASS: fresh offline installation, rebuild, demos, 6 unit + 64 integration, isolation probes and missing-dependency negative |
| `audit` | PASS: runtime 74/74, Pass 2 83/83, separate correction 8/8 |
| `git diff --check` / `git diff --cached --check` | PASS |

All 1,075 pinned upstream files verify. `_bricked` remains clean at
`c89676fc26000ae6f5fdad66a56e118b285d9b1d`; execution uses the ignored dependency copy.
No mandatory failure, NOT_RUN or BLOCKED remains. Nine existing policy gates in
`PASS_02_POLICY_GATES.json` remain unchanged and are not mandatory test waivers.

## Fresh distributions

Both archives bind source commit `7a9f073959af7bb41dd60bf5ddbb1e7176c7803b`. Their manifests verify all 1,394
payload entries (1,378 Horizon and 18 Hypervisor archive members including manifests).
Hypervisor source is unchanged; its archive metadata identifies the matching source commit.

| Component | Archive | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| horizon | `genesis-horizon-0.2.0.zip` | 17,853,473 | `b4a7ef24a65213e52853bded0a270c87d8ec976896aa96bad181ceeb3b276b61` |
| hypervisor | `raeon-python-hypervisor-0.2.0.zip` | 17,294 | `c9c0f392479092434284c11e253e8d0c8a323611a377bb486951a9e5184c7e3c` |

Artifacts and `.sha256` sidecars are under `build/genesis_runtime/distributions/`.
Fresh verification extracted to `C:\Users\rando\_raeon\build\RAEON clean extraction siovvnrg` using `TEMP=TMP` set to
`C:\Users\rando\_raeon\build`, so every write stayed inside the authorized repository.
Independent Python audit interception enforced the fresh file closure and denied
network/DNS, Git and external-checkout probes. It recorded 329,538 events with
zero unexpected denials. This is interception for trusted pinned reference engines,
not an OS sandbox for arbitrary native code. Python 3.12 remains a prerequisite.
Bytecode was identical after relocation. Missing dependency intentionally exited 1
with the required missing-source diagnostic; no fetch occurred.

The first extraction attempt used a longer temporary path and hit Windows' path
limit before tests. A shorter ignored build path resolved extraction. The first
complete fresh run passed 63/64 methods, including all three audited cases; a
new checkpoint test exceeded the path limit when its second player reused the
first player's restored storage root. Commit `7a9f073959af7bb41dd60bf5ddbb1e7176c7803b` isolates each role's real
fixture while retaining every assertion. The isolated diagnostic passed, followed
by complete local and fresh reruns. No runtime workaround or validator suppression
was introduced. Logs of the failed run and diagnostic remain in generated evidence.
Initial staging also caught transcript whitespace; normalization was followed by
exact staged-byte hash checks and full source-bound validation.

## Changes and retained boundaries

Nine added files: this receipt; the JSON amendment; audit ZIP, baseline binding
hashes, reproduction JSON and transcript; the integration regression file; the
repository integrity regression file; and the separate correction audit helper.
Eight modified files: the two projection bindings; current inventory; current
execution record; historical receipt annotation; runtime command dispatcher;
distribution inclusion list; and existing Pass-2 integrity validator.
No files deleted, moved or renamed relative to the starting commit.

The completed Pass-2 implementation, all historical tests and provenance remain.
No Genesis source, Hypervisor game logic, canonical design, source-backed 120 Field
Generators, 2,094-object atlas or mathematics changed. No architecture redesign,
new gameplay policy, Pass-2 restart, native-device execution or main merge is claimed.
Pass 3 still requires its own authorized request.
