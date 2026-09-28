# Tests

Only repository/design-data validators exist; these are not game-system tests.

```sh
node tools/validators/validate-bootstrap.mjs
node tools/validators/validate-design-state.mjs
node --test tests/regression/bootstrap-validator.test.mjs tests/regression/design-state-validator.test.mjs
```

Requires Node and Git. Bootstrap regressions use temporary copies of this repository; design regressions mutate structured data to verify rejection of contradictory rules and false completion. No fake gameplay tests exist. Mathematics, QMO closure, balance, Blender/GPU, AI and multiplayer correctness remain unvalidated. See [CONTRIBUTING.md](../CONTRIBUTING.md).
