# Runtime build task

Continue the [build order](development/modules/core-game/GENESIS_RUNTIME_BUILD_ORDER.md) from the [execution record](development/modules/core-game/GENESIS_RUNTIME_EXECUTION.md). Recover actual Git state before editing; preserve completed design reconciliation.

Only this repository is writable. The work order explicitly permits read-only `_bricked` source access for this runtime integration, overriding the earlier general isolation rule only within that scope. Run upstream tools in ignored `build/dependencies/` copies. Keep source authority unchanged.

Use `tools/genesis_runtime.py` as implemented; record actual compiler/runtime evidence. Do not substitute fake runtime tests for integration, invent Genesis syntax, regenerate QMO catalogs, or merge main without authorization. Whole-game PREPRODUCTION and unaccepted module gates remain unchanged.

Verified predecessor: [Pass-2 execution record](development/modules/core-game/PASS_02_EXECUTION.md) and its completed projection privacy correction at `d991278`. Preserve all preceding tests and source history.

Current Pass-3 work: [execution record](development/modules/core-game/PASS_03_EXECUTION.md). Continue `codex/raeon-pass-03` from corrected Pass 2 (`d991278`). Preserve its privacy regressions; main stays unmerged.

Current Pass-3B continuation: [execution record](development/modules/core-game/PASS_03B_EXECUTION.md). Inherit completed Pass 3 at `33f4139` on `codex/raeon-pass-03b`. Preserve prior tests and privacy correction; do not merge main. The new realization authority closes the named historical pose/fusion/emergence gaps, without regenerating QMO sources.

Current Pass-4 continuation: [execution record](development/modules/core-game/PASS_04_EXECUTION.md). Inherit completed Pass 3B at `d644a36` on `codex/raeon-pass-04`. Preserve all prior tests, privacy, QMO authority and HOST-RUNTIME-001 qualification. No main merge or invented refresh/scheduler rules.
