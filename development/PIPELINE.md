# Module development pipeline

Authority: CANON. Apply all sixteen gates to every major subsystem.

| Gate | Required exit evidence |
| --- | --- |
| 00 Canon | Identify source authority, scope, conflicts, unresolved imports. |
| 01 Design | Specify player/product intent, requirements, non-goals. |
| 02 Mathematics | Import approved formal definitions and mathematical admission evidence. |
| 03 Rules | Define legal/illegal rules without changing mathematical authority. |
| 04 State Model | Define entities, invariants, lifetimes, transitions. |
| 05 Interfaces | Define versioned inputs, outputs, errors, ownership. |
| 06 Algorithms | Specify source-linked procedures and determinism. |
| 07 Visualization | Specify how authoritative objects become inspectable and visible. |
| 08 Interaction | Define actions, feedback, and constraints. |
| 09 Data & Schemas | Version schemas, IDs, manifests, migrations, validation. |
| 10 Implementation | Implement reviewed contracts without speculative rules. |
| 11 Testing | Produce meaningful evidence including negative cases. |
| 12 Integration | Demonstrate behavior with dependencies and representative data. |
| 13 Performance | Measure approved budgets on target hardware. |
| 14 Provenance | Record sources, decisions, derivation, checks, artifact lineage. |
| 15 Release | Record accepted version, limitations, checkpoint, release approval. |

Gate statuses: OPEN (not accepted), VALIDATED (reviewed evidence accepted), NOT_APPLICABLE (reviewed rationale and authority recorded). SOURCE_IMPORT_REQUIRED blocks dependent acceptance. Each gate record links evidence, source revision, reviewer/acceptance, and date. UNTESTED claims do not count as VALIDATED evidence.

States: OPEN → DESIGN → FORMALIZED → IMPLEMENTED → VALIDATED → GOLD. DESIGN means active specification; FORMALIZED requires applicable gates 00–09 accepted; IMPLEMENTED records gate 10 evidence without implying validation; VALIDATED requires applicable testing, integration, performance, and provenance gates; GOLD adds gate 15 release acceptance. Iterate earlier gates when contracts change and invalidate stale downstream evidence.

Implementation alone never means COMPLETE. Completion/GOLD requires all applicable gates accepted, justified NOT_APPLICABLE entries, closed blocking questions, and an accepted checkpoint. Module GOLD does not promote the whole game to GOLD.
