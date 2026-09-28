# Future card-effect schema direction

Authority: PROVISIONAL / WORKING DESIGN; source [Block 3](../../provenance/sources/recovery-0003-block-3.txt). This is a schema proposal, not an executable runtime schema or final catalog.

Cards should eventually have human-readable rules text and machine-readable effects. Possible fields: id, family, rank_color, operator, magnitude, target_type, timing, duration, constraints, authority, status. The existing [accepted state](../manifests/accepted-state.json) records structural design; do not infer missing runtime values from it.

Illustrative accepted examples:

| Family | Operator | Rank color | Magnitude |
| --- | --- | --- | --- |
| TRANSDUCTION | RESTORE | YELLOW | 3 |
| DRAW_DECK | DRAW | VIOLET | 3 |

Utility identifiers are planned as UT-001 through UT-050. Assignment and deterministic ordering are OPEN; no IDs are assigned in this checkpoint. Future assignment must document order, preserve family counts, distinguish working names from final names and retain unresolved fields. Unknown targeting, timing, duration, cost and rank remain OPEN, not implicit defaults.
