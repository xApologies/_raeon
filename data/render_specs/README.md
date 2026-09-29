# Cycle-1 RenderSpecs

[Catalog](cycle_01/catalog.json) and all 60 base manifold RenderSpecs are exact original bytes, with [source schema](../schemas/cycle1-render-spec.schema.json). Source catalog paths `data/render_specs/M-*.json` resolve in this repository as `data/render_specs/cycle_01/M-*.json`; the manifest explicitly records that prefix mapping.

Generator and 2,034 derived-object RenderSpecs are SOURCE_IMPORT_REQUIRED. The complete QMO atlas is available independently of render coverage. QMO remains authoritative. Blender/Metal references do not constitute an implemented game renderer.

`deterministic_seed` contains unsigned integers beyond JavaScript's safe-integer range. Preserve raw JSON or use an integer-safe parser. The [read-only query](../../tools/qmo/query-cycle1.mjs) returns render JSON unchanged.
