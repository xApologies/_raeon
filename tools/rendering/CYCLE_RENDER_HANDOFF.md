# Render Handoff

## Principle

**The math tells Blender what exists. Blender makes it visible. Metal makes it alive.**

## QMO → RenderSpec

The RenderSpec is deterministic and derived from the QMO.

It should contain:
- control anchors,
- topology graph,
- spline/curve controls,
- tube/filament parameters,
- chirality/winding,
- Resolution/detail parameters,
- Bandwidth/thickness or transport parameters,
- implicit-shell parameters,
- projection law from higher-dimensional state,
- semantic color state,
- animation constants,
- deterministic seed.

## RenderSpec → Blender

Blender:
- builds/editable curves and mesh,
- preserves QMO ID in metadata,
- never invents legal topology,
- may add art-direction detail only within the permitted render grammar,
- exports mesh asset.

Recommended development order:
1. prototype one Yellow manifold,
2. freeze visual grammar,
3. batch-generate base manifolds,
4. batch-generate derived manifolds,
5. batch-generate 120 Generator-card visuals.

## Blender → Metal

Metal:
- loads mesh,
- loads runtime QMO/RenderSpec state,
- animates energy flow,
- color transduction,
- field activation,
- shield state,
- deformation,
- particles,
- bloom/glow,
- tap pulses.

Blender is not required at runtime on iPad.
