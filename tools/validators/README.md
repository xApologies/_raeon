# Repository validators

Run validate-bootstrap.mjs for preserved scaffold/numerical checks; validate-design-state.mjs for all checkpoint-0003 design invariants loaded from normalized datasets; validate-normalization.mjs for authority, pointers, links, history integrity and lossless migration. load-design-state.mjs is a read-only adapter used by validators/tests.

These tools are not game runtime. See [tests](../../tests/README.md) for commands and scope.

Continuity verification: `node tools/validators/validate-continuity.mjs` checks recovered structure and source integrity, not external mathematics.
