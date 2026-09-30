# Validation and system tests

Repository validators and focused gameplay specification examples are implemented. Production game-system integration remains OPEN / UNTESTED; the example model is not a Genesis runtime.

```sh
node tools/validators/validate-bootstrap.mjs
node tools/validators/validate-design-state.mjs
node tools/validators/validate-normalization.mjs
node tools/validators/validate-continuity.mjs
node tools/validators/validate-cycle1-import.mjs
node tools/validators/validate-full-migration.mjs
node tools/validators/validate-game-definition.mjs
node --test tests/regression/*.test.mjs
node --test tests/gameplay/cards/*.test.mjs tests/gameplay/primes/*.test.mjs tests/gameplay/sandbox/*.test.mjs tests/gameplay/manifolds/*.test.mjs
```

System boundaries: unit, integration, regression, gameplay/cards, gameplay/sandbox, gameplay/manifolds, gameplay/transduction, gameplay/primes, gameplay/utilities, qmo, rendering, multiplayer, adversarial and performance. [Authority map](../data/manifests/authority-map.json) links each to upstream design/data. Checks do not validate QMO mathematics, balance, final timing, rendering, AI or multiplayer correctness.
