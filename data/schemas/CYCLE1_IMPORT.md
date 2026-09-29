# Cycle-1 source-preserving schema mapping

Authority: recovered original Closed Playfield v1.0, atlas, Constitution v1.0 and historical Live Model. [Import manifest](../manifests/cycle1-source-import.json) is the current receipt; [file mappings](../../provenance/sources/cycle1-originals/file-mappings.json) record archive, member, destination and SHA-256 for every normalized copy.

| Source content | Repository treatment |
| --- | --- |
| FG JSON/CSV, base JSON, compatibility, derived JSON, pair JSON, SQLite, summary | Exact original bytes at manifest dataset paths |
| Complete atlas JSON | Exact original index with all 2,094 objects; full definitions are also present |
| Fusion and emergent JSON | Source derived records filtered by `type`; field names/values/order unchanged, whitespace reformatted |
| Render catalog/schema and 60 base specs | Exact bytes; catalog path prefix mapped explicitly to `data/render_specs/cycle_01/` |
| Original ZIPs, embedded reference ZIPs and manifests | Preserved; no rewriting of old manifests or record authority labels |
| Constitution, derivation, schemas, algorithms, validation and render handoff | Exact readable source copies in existing design/mathematics/data/tools boundaries |
| Live Model machine state, code, timeline and history | Source evidence under provenance, with visual references under content; not active game rules |

Identifiers stay as supplied: `card_id` is FG-001 through FG-120; `manifold_id` is M-R-01 etc.; `id` is the QMO address. The 2,094-object atlas covers 60 base + 343 fusion + 1,691 emergent objects. The 120 Generators and one closed-fractal seed are additional objects, not part of that atlas count. SQLite stores FG/base/seed in `qmos` and derived objects in `derived_qmos`.

The Constitution's [required-fields template](cycle-qmo-required-fields.json) uses future names such as `address` and cycle/derivation metadata. Legacy source records instead use `id`, `rotation_class`, `chirality_parity`, `resolution_depth`, `bandwidth_degree`, `support`, and other source fields. Those names and source status labels remain unchanged. Dataset receipt/version provenance supplies package-level context; no missing per-object field is fabricated. The Constitution's recommended future derived-address pattern does not rename existing `@qmo/raeon/derived/...` identities.

Status files now index actual record IDs with `objects_ref`. `IMPORTED_VALIDATED` means original-source identity, counts, parsing, references and cross-format consistency passed. It does not mean theoretical proof, final playable cards, balance or implemented game systems. The original full-game catalog flag remains false: Prime identities/final Utilities/card details are still OPEN.

Source RenderSpec `deterministic_seed` integers can exceed 2^53. Do not round-trip these through ordinary JavaScript numbers. The query command emits original render JSON; the validator reads the integer token as BigInt. Source render paths are mapped by the import manifest without changing original bytes. Source Markdown/code references retain their original archive namespace; use the file mapping to find their normalized counterparts.

Historical per-object `GAME_DERIVED_v0_2` and SQLite version `0.2` labels are retained under the later locked v1.0 game package. This is an authority/version distinction, not permission to relabel the source as research proof. [Reconciliation decision](../../provenance/decisions/cycle1-source-import.md) defines precedence and unresolved runtime scope.
