# Runtime build task

Continue the [build order](development/modules/core-game/GENESIS_RUNTIME_BUILD_ORDER.md) from the [execution record](development/modules/core-game/GENESIS_RUNTIME_EXECUTION.md). Recover actual Git state before editing; preserve completed design reconciliation.

Only this repository is writable. The work order explicitly permits read-only `_bricked` source access for this runtime integration, overriding the earlier general isolation rule only within that scope. Run upstream tools in ignored `build/dependencies/` copies. Keep source authority unchanged.

Use `tools/genesis_runtime.py` as implemented; record actual compiler/runtime evidence. Do not substitute fake runtime tests for integration, invent Genesis syntax, regenerate QMO catalogs, or merge main without authorization. Whole-game PREPRODUCTION and unaccepted module gates remain unchanged.
