# Tests

Only repository/bootstrap checks exist today. Run `node tools/validators/validate-bootstrap.mjs`, then `node --test tests/regression/bootstrap-validator.test.mjs`. Node and Git are required. The regression suite checks that invalid repository states are rejected using temporary copies of this bootstrap.

Unit, integration, gameplay, QMO, rendering, multiplayer, adversarial, and performance directories reserve future meaningful system evidence. No fake passing game tests exist.

These checks do not validate Genesis or Chirality mathematics, QMO closure correctness, gameplay balance, Blender geometry, GPU rendering, multiplayer correctness, or AI correctness. Follow [CONTRIBUTING.md](../CONTRIBUTING.md).
