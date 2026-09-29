# Blender -> Metal production pipeline

1. Query a canonical manifold QMO.
2. Generate `RenderSpec` JSON with `render/export_render_spec.py`.
3. Feed the JSON to `blender/build_manifold.py`.
4. Blender builds editable curve/tube geometry and exports GLB.
5. Production pipeline converts/imports the asset to the Apple runtime format you choose.
6. Swift loads both:
   - static/baked geometry asset,
   - `RenderSpec` state/animation parameters.
7. Metal performs live animation:
   - energy flow,
   - field pulse,
   - color transduction,
   - glow/bloom,
   - chirality deformation,
   - Resolution-driven detail,
   - tap activation.
8. The QMO remains canonical. Blender/Metal are downstream visual adapters.

Recommended first prototype:
- Use one Yellow manifold QMO.
- Bake only anchors + tubes in Blender.
- Do energy flow entirely in Metal.
- Add implicit field shell only after performance is stable.

Why this split works:
- Blender is excellent for mesh authoring/inspection.
- Metal is excellent for runtime procedural animation.
- The game never needs Blender installed on the iPad.
- New manifolds can be batch-generated from QMO RenderSpecs.
