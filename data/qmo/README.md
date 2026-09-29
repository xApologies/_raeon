# Queryable Cycle-1 QMO data

Status: IMPORTED_VALIDATED from the four recovered original artifacts. [Import manifest](../manifests/cycle1-source-import.json) gives paths, counts and remaining source gaps; [schema mapping](../schemas/CYCLE1_IMPORT.md) documents source-preserving normalization.

| Dataset | Records | Direct data |
| --- | ---: | --- |
| Field Generators | 120 | [FG-001…FG-120](../cycles/cycle_01/field_generators/objects.json) |
| Base Local Manifolds | 60 | [Definitions and memberships](manifolds/objects.json) |
| Fusion-derived Local Manifolds | 343 | [Definitions](fusion/objects.json) |
| Emergent Fields | 1,691 | [Definitions and supports](emergent/objects.json) |
| Complete manifold/field atlas | 2,094 | [Atlas index](cycle1/atlas.json) |
| Base-manifold pairs | 1,770 | [Explicit outcomes](cycle1/manifold_pair_relations.json) |
| FG compatibility pairs | 2,482 | [Face matches](generators/compatibility.json) |
| Base RenderSpecs | 60 | [Catalog](../render_specs/cycle_01/catalog.json) |

[Original SQLite database](cycle1/qmo.sqlite) is a directly queryable byte-identical copy. FG/base/seed definitions are in `qmos`; the 2,034 derived definitions are in `derived_qmos`. The 2,094-object atlas excludes the 120 FG objects and source seed.

```sh
node tools/qmo/query-cycle1.mjs counts
node tools/qmo/query-cycle1.mjs fg FG-001
node tools/qmo/query-cycle1.mjs base M-R-01
node tools/qmo/query-cycle1.mjs pair M-R-01 M-Y-01
node tools/qmo/query-cycle1.mjs qmo @qmo/raeon/derived/fusion/m-o-01+m-o-02
node tools/qmo/query-cycle1.mjs render M-R-01
```

From any SQLite reader:

```sql
SELECT card_id, address, occupancy, void_sites FROM generator_cards ORDER BY card_id;
SELECT address, definition_json FROM qmos WHERE qmo_type = 'LocalManifoldQMO'
UNION ALL SELECT address, definition_json FROM derived_qmos;
SELECT pair_key, fusion_status, emergent_status FROM manifold_pair_relations;
```

Queries read stored source records without regenerating or inferring relations. Unknown IDs/pairs return OPEN, never TERMINATES. Runtime instance rules, unimported theoretical operators and full game integration remain OPEN.
