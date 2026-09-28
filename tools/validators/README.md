# Repository and design validators

`node tools/validators/validate-bootstrap.mjs` checks the preserved architecture and current accepted baseline invariants. It recreates local ignored _inbox on fresh checkouts.

`node tools/validators/validate-design-state.mjs` checks the 50-slot structure, explicit rules/OPEN states, source integrity and checkpoint inventory. Both use Node built-ins; bootstrap also uses Git.

Run both validator regression suites as described in [tests](../../tests/README.md). These are data-consistency checks, not game implementations or mathematical/gameplay correctness tests. Other tooling remains OPEN.
