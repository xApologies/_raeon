# platform

Windows desktop is the initial priority; iPad/iPadOS is secondary. Keep shared logic independent of adapters.

Status: OPEN — intentionally reserved; no implementation or completion claimed.

Add only reviewed material appropriate to this boundary. Placeholder documentation is not implementation or validation evidence.

Follow [CONTRIBUTING.md](../CONTRIBUTING.md) and the relevant module gates. Record source, authority, validation, and checkpoint references.


[Accepted runtime direction](../data/platform/runtime-direction.json): Genesis semantics ↔ Genesis VM ↔ Python translation boundary ↔ platform shell. Windows first; later Apple/Metal and Android shells. Platform graphics/input/audio/storage/network return events to authoritative Genesis/QMO state. No platform runtime is implemented.
