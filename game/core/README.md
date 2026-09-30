# Implementation boundary: core

Game-specific core status: OPEN / UNIMPLEMENTED. Generic host-reference runtime software is available below; it does not implement match rules or close a game-development gate.

- [core-game design](../../design/game/GAME_DESIGN_DOCUMENT.md) → [data](../../data/game/product.json) → [maturity](../../development/modules/core-game/README.md)
- [platform design](../../design/game/GAME_DESIGN_DOCUMENT.md) → [data](../../data/platform/targets.json) → [maturity](../../development/modules/platform/README.md)

No downstream layer may redefine accepted design or mathematical legality.

[Genesis Horizon](genesis_horizon/README.md) provides the compiled native reference runtime. [Execution evidence](../../development/modules/core-game/GENESIS_RUNTIME_EXECUTION.md) records its tested scope and distributions.
