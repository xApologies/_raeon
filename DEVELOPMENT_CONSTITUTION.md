# raeon. development constitution

Authority: CANON. Apply the [project constitution](PROJECT_CONSTITUTION.md), [module gates](development/PIPELINE.md), and [contribution workflow](CONTRIBUTING.md).

## Boundaries

production/ governs lifecycle evidence; development/ governs modules, milestones, builds, and checkpoints. design/ holds player/product intent; mathematics/ formal authority; game/ executable implementation; content/ presentation assets; data/ structured project truth. tools/ holds tooling; tests/ meaningful evidence; platform/ shared, Windows, iPadOS adapters; releases/ release records; provenance/ source lineage and decisions. _inbox/ is local-only transfer storage.

## Evidence

Use all gates 00–15. NOT_APPLICABLE needs reviewed rationale. Implementation alone never means COMPLETE. Source-linked mathematics determines legality. Missing sources block mathematical validation; placeholders cannot become fake passing tests. Engine, graphics API, networking, AI, and persistence choices remain OPEN until approved.

## Data and rendering

Prefer versioned JSON, SQLite, schemas, and manifests over prose duplication. Preserve QMO identity/derivation across deterministic RenderSpec → Blender geometry → mesh → GPU animation. Visual output does not authorize mathematical relationships. Version schema/interface changes and preserve provenance.

## Acceptance

Run repository validation and relevant real subsystem/integration/performance checks. Record exact command, result, scope, revision and limitations in the relevant commit, review or durable evidence record. Numbered checkpoints are reserved for substantive accepted design, source, mathematical, milestone or migration evidence; ordinary commits and Git housekeeping do not require one. Review Git status/staged changes, exclude inbox/cache/binary material, commit on a branch, and submit for acceptance. Never claim unrun tests or completed phases.
