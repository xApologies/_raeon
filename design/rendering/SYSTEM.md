# Mathematical objects and visualization

<!-- raeon:current-spec rendering -->

Authority: CANON for the preserved architecture; unresolved realization stays OPEN. Source: [Block 3](../../provenance/sources/recovery-0003-block-3.txt). [Accepted state](../../data/manifests/accepted-state.json) records this direction.

QMO → deterministic RenderSpec → Blender procedural geometry → mesh → runtime GPU renderer → animated manifold. QMO defines the mathematical object; RenderSpec defines deterministic visualization instructions; Blender realizes geometry; runtime graphics animate it.

Rendering never changes mathematical legality. If visual geometry contradicts QMO state, the render is wrong; the QMO did not change. Authoritative QMO/RenderSpec/API packages remain SOURCE_IMPORT_REQUIRED.

QMO state may contain higher-dimensional information, but the displayed result is an explicit **3D projection/embedding**. Blender does not literally render five spatial dimensions. Higher-dimensional state may influence winding, phase, orientation, deformation, field-shell behavior, emissive flow, animation and topology-preserving motion. Exact projection mathematics is SOURCE_IMPORT_REQUIRED, not reconstructed here.

Windows desktop remains the primary target; iPad/iPadOS is secondary. Keep shared rules/data platform-independent where practical. No Blender generation, renderer or platform runtime is implemented.
