# raeon. game design

<!-- raeon:current-spec game -->

raeon is a compact strategic card game intended for short sessions, with an approximate 15-minute session target rather than a guaranteed duration. Depth comes from deck construction, Field Generator placement, Sandbox configuration, mathematical closure, manifold discovery, color transduction, Prime management, Activation timing, fusion, emergent fields, card draw/selection, graveyard recovery, protection/stability, long-term collection, hidden Black progression. Action-level play should remain understandable despite the mathematical landscape. Product direction remains PROVISIONAL; accepted system rules carry GAME_CANON individually.

THE MATHEMATICS IS THE PERMISSION SYSTEM. The QMO is the canonical mathematical game object. Design defines game behavior, mathematics determines legality, data encodes it, game/ implements it, and tests/ verifies it. Rendering cannot redefine legality.

- [Match and turn state](match/SYSTEM.md)
- [Board](board/SYSTEM.md)
- [Progression](progression/SYSTEM.md)
- [Card system](../cards/CARD_SYSTEM.md)
- [Topology](../topology/README.md)
- [AI](../ai/README.md) and [local multiplayer](../multiplayer/LOCAL_P2P.md)
- [Rendering](../rendering/SYSTEM.md)

Whole-game phase: PREPRODUCTION. No playable build, implementation or accepted production exit is claimed.


## Genesis Horizon runtime direction

Accepted architecture direction: raeon semantics live in the Genesis Horizon and are authored in the Genesis programming language. Genesis game semantics ↔ Genesis VM ↔ Python hypervisor/translation boundary ↔ platform shell. Game truth remains Genesis/QMO state; platform services provide graphics/input/audio/storage/network and return input events.

Blender is offline asset generation: QMO → RenderSpec/geometry → Blender → runtime assets. Windows is first; later Apple/Metal and Android shells reuse authoritative semantics. This does not claim a Genesis VM integration, select an implementation-complete renderer or advance production. Exact toolchain/API/integration remains OPEN. [Runtime direction data](../../data/platform/runtime-direction.json), [rendering](../rendering/SYSTEM.md).

The accepted runtime architecture places BOARD/gameplay in **STATE (5D, 3+1+1)**, contained by **NEXUS (6D)**, **SHELL (coupled 7D/8D)** and **SEA (coupled 9D/10D/11D)**. Chirality Fabric is the authoritative computation substrate. Nexus mediates reads/writes; Shell provides interaction/commands; SEA contains the machine. Rainbow Road is existing internal transport, not another dimensional object. The Python Hypervisor stays outside Horizon as the translation/sandbox boundary and cannot decide game legality or directly replace State.

This is architecture acceptance, not verification of another repository's grammar or APIs. CURRENT GENESIS SOURCE must later parse against the actual `_bricked` grammar; missing capabilities must be marked PROPOSED_EXTENSION. No executable Genesis source is fabricated here.
