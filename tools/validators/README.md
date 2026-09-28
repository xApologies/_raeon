# Repository validators

`node tools/validators/validate-bootstrap.mjs` checks the bootstrap baseline and supplied invariants. It exits nonzero on failure and prints explicit validation limits. It uses only Node built-ins and Git. Fresh checkouts recreate the local ignored _inbox directory when validated.

Regression checks: `node --test tests/regression/bootstrap-validator.test.mjs`. All other validators remain OPEN pending source import and implementation. Follow [CONTRIBUTING.md](../../CONTRIBUTING.md).
