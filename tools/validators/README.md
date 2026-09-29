# Repository validators

Run all five commands in the [test index](../../tests/README.md). Node 24+ provides built-in SQLite inspection; no external Node packages are needed.

Bootstrap, design, normalization and continuity validation protect existing structure, gameplay state and historical evidence. [Cycle-1 source integrity](validate-cycle1-import.mjs) independently pins all four original archive hashes, checks nested source manifests and exact normalized member bytes, validates counts/references and compares SQLite/JSON/atlas representations. [Regression tests](../../tests/regression/cycle1-import.test.mjs) exercise corrupted and missing source data, unknown queries and integer-safe render output.

Success verifies repository consistency and source integrity, not theoretical mathematics, balance or game implementation.
