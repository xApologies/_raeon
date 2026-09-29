# Current design index

raeon is a compact strategic card game whose mathematical QMO layer governs legality. Current whole-game phase: PREPRODUCTION.

## Start with current specifications

- [Game Design Document](game/GAME_DESIGN_DOCUMENT.md): product intent and system navigation
- [Card System](cards/CARD_SYSTEM.md), [Cycle 1](cards/cycle_01/CYCLE.md), [Utility families](cards/cycle_01/utilities/SYSTEM.md), [Black cards](cards/black/SYSTEM.md)
- [Topology](topology/README.md), [transduction](transduction/SYSTEM.md), [collection](collection/SYSTEM.md), [economy](economy/README.md)
- [AI](ai/README.md), [multiplayer](multiplayer/LOCAL_P2P.md), [rendering](rendering/SYSTEM.md), [UI/UX](ui_ux/SYSTEM.md)

GAME_CANON is explicitly accepted rules/structures. PROVISIONAL / WORKING DESIGN includes stated working ranks, Black concepts and product direction. Utility architecture is structurally defined; exact catalog only partially formalized.

OPEN: IDs, final catalogs, unresolved targets/timing/duration/ranks, turn/match sequencing, balance, engine, transport, AI, economy values and UI detail. IMPORTED_VALIDATED: original Cycle-1 Generator/QMO catalog, complete atlas, pair/compatibility data, Constitution and 60 base RenderSpecs. SOURCE_IMPORT_REQUIRED: broader mathematics/APIs, Generator/derived RenderSpecs and geometry references, and projection mathematics. The [state index](../data/manifests/accepted-state.json) retains the exact lists.

Implemented: repository/data validation tooling only. No game/AI/network/renderer implementation, gameplay tests or production completion claimed. Next design task: foundational turn/match design; Utility ordering/IDs remain OPEN.

[Authority map](../data/manifests/authority-map.json) maps DESIGN → DATA → GAME → TESTS; [development](../development/README.md) tracks maturity and [provenance](../provenance/README.md) retains history. Sources do not substitute for current specifications.

## Originating-thread continuity

Current [Generator interaction](topology/field_generators/SYSTEM.md) and [Genesis Horizon board](game/board/SYSTEM.md) preserve recovered state. [Propagation evidence](../mathematics/propagation/README.md) is imported with R88 OPEN. Next foundational workshop: [turn/match design](game/match/SYSTEM.md), then victory/loss and Prime catalog; Utility finalization follows.


The [2026-09-29 accepted delta](../data/manifests/full-migration-2026-09-29.json) now fixes 185 ordinary identities, 14 Prime H/C identities, 51 Utilities, mutable Configuration Spaces, fixed top-down XY + 3D orientation and Genesis runtime direction. Exact timing, victory, gestures, balance and implementation remain OPEN.
