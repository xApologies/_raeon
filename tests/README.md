# Validation and system tests

Repository validators are implemented; game-system tests remain UNTESTED boundaries. No placeholder claims to test gameplay.

```sh
node tools/validators/validate-bootstrap.mjs
node tools/validators/validate-design-state.mjs
node tools/validators/validate-normalization.mjs
node tools/validators/validate-continuity.mjs
node tools/validators/validate-cycle1-import.mjs
node --test tests/regression/*.test.mjs
```

System boundaries: unit, integration, regression, gameplay/cards, gameplay/sandbox, gameplay/manifolds, gameplay/transduction, gameplay/primes, gameplay/utilities, qmo, rendering, multiplayer, adversarial and performance. [Authority map](../data/manifests/authority-map.json) links each to upstream design/data. Checks do not validate QMO mathematics, balance, final timing, rendering, AI or multiplayer correctness.
