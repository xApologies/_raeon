# Genesis runtime execution

Current unit: W10 acceptance/regression and W11 distribution. Next exact action: run the expanded local tests and existing repository validators, correct failures, then package and verify both clean extractions. W00–W09 implementations are saved; no native-device or whole-game completion is claimed.

Task start: clean `codex/game-definition-2026-09-30` at `711ad7485c8cd58a87ec03ff59d6daf8b6498487`. Main stays `69a0030805b8c3858c877a514e2f50644421115a`. Task branch `codex/genesis-horizon-hypervisor`. No reset/clean/discard. First successfully pushed task commit: `f7406cfa1c9d7d76191b71eb9092d4f87212ad73`. Task commits are read from Git, not embedded self-referentially here.

## Source and path map

Working repository `C:/Users/rando/_raeon`; original upstream `C:/Users/rando/_bricked` remains read-only. Upstream clean `bootstrap/canonical-architecture` at `c89676fc26000ae6f5fdad66a56e118b285d9b1d`, matching remote. Writable isolated dependency is ignored `build/dependencies/bricked-runtime`.

Implementation: `game/core/genesis_horizon/src/`; bindings under `game/core/genesis_horizon/bindings/python/src/raeon_genesis_horizon/`; fence under `platform/shared/python_hypervisor/`; unit tests `tests/unit/hypervisor/`; real integration tests/application `tests/integration/genesis_horizon/`. Entry point `tools/genesis_runtime.py`; dependency/runtime authority `data/platform/genesis-runtime-lock.json`, finite profile `data/platform/genesis-horizon-profile.json`. Generated evidence stays under ignored `build/genesis_runtime/`.

Boot combines sea/Shell/Nexus instantiation/containment in `boot.gen`; fixed interface dispatch is in `road_in.gen`/`road_out.gen`; native immutable State inheritance is in `state.gen`; quiescent closure/sealing is in `lifecycle.gen`. No empty per-domain scaffolds. Python binds supported primitive operations to the actual native engines and atomically publishes their persistent graph. No new Genesis syntax.

## Executed evidence

- Upstream original Rainbow Road parse/lower/build/run: all exit 0; verified receipt `receipt-e0bbca751087ac913a9d`. GVM SHA256 `b5f96deddc738338a028802faf80a072b99070ad5b674303bd041bfab65cc041`.
- Upstream domains 1,2,3,4,5,8,9,10,13,14,15,16,17: all pass, 675 checks/tests across thirteen isolated suites. Full logs in build evidence.
- Separate System-I/O 0.6 positive executes CLOSED; relabelled graph syntax is rejected. Callable package positive resolves its actual standard-library imports, expands two calls, executes verified.
- Nine authored Genesis sources compile, verify and rebuild to identical artifacts.
- Python acceptance now includes 6 protocol unit tests and 16 integration/archive tests; the expanded run passes. Real native bytes, six-direction Road paths, rollback, duplicate/conflicting/expired retries, projection privacy/gap recovery, checkpoint restore and replay are exercised. Bounded-resource refinements also pass the complete rerun. Seven existing validators, 193 repository regressions (including five narrow amendment tests), 17 gameplay specification tests and diff checking pass. The application cannot acquire machine-domain inheritance; only the internal State commit phase can inherit State, and it cannot inherit sea, Shell or Nexus. A failed test run invalidates package eligibility. The full real headless demonstration passes, including mirror transformation, exact Port projection, duplicate recovery and restore. Original upstream remains clean at its starting SHA.

## Corrections and limitations

Git autocrlf produced different working-tree bytes in the dependency copy. Exporting the pinned Git source bytes resolved that mismatch; upstream remained untouched. First callable smoke omitted declared package imports; using the actual CallablePackageRuntime resolver fixed the harness. First altered-ID retry was incorrectly classified as committed delivery pending; fixed and covered by a negative test. No upstream test failure is being suppressed.

The native reference profile uses supplied Generic3p1p1 encoding with four separately instantiated architectural domains. Mathematical embeddings/coupling remain OPEN upstream. No public redistribution license was found in the pinned upstream Git tree; distribution is a private owner handoff, not a grant of public licensing rights. Python 3.12 and NumPy 2.3.5 are required. Native-device tests NOT_RUN. All sixteen module gates remain OPEN, whole-game PREPRODUCTION.

The historical no-Genesis-source guard is amended only for nine exact compiled source hashes under a separately pinned runtime decision. Existing accepted gameplay/data/catalog protections remain in force. No Cycle-1 mathematics or gameplay policy is changed.

## Delivery

Packaging tools are implemented. Exact upstream subset: 1,075 files, each checked against the immutable Git blob as well as SHA-256. Offline Windows x64 CPython 3.12 wheels are pinned: NumPy 2.3.5 and setuptools 84.0.0. The archives require Python itself; they do not claim to bundle an interpreter. Distribution creation and clean-extraction validation are the remaining work. Do not claim completion until those actual results are recorded.
