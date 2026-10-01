import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {pass04, pass04Decision} from '../../tools/validators/pass-04-contract.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const decision = JSON.parse(fs.readFileSync(path.join(root, pass04Decision)));
test('Pass-4 exact source amendment preserves prior tests, QMOs and PREPRODUCTION', () => {
  assert.equal(pass04(root).whole_game_phase, 'PREPRODUCTION');
});
for (const mutation of ['game/primes/state.py', 'game/sandbox/topology.py',
  'game/core/genesis_horizon/bindings/python/src/raeon_genesis_horizon/native.py',
  'game/core/raeon/application/generate_field.gen', 'game/core/raeon/application/spend_prime.gen',
  'data/game/pass-04-runtime.json', 'data/cycles/cycle_01/primes/status.json',
  'development/modules/core-game/HOST_RUNTIME_RISKS.json', pass04Decision]) {
  test('Pass-4 guard rejects changed ' + mutation, () => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'raeon-p4-'));
    try {
      for (const file of new Set([...Object.keys(decision.sources), ...Object.keys(decision.changes),
        ...Object.keys(decision.preserved_tests), ...Object.keys(decision.qmo_sources), pass04Decision])) {
        const target = path.join(tmp, file);
        fs.mkdirSync(path.dirname(target), {recursive:true});
        fs.copyFileSync(path.join(root, file), target);
      }
      fs.appendFileSync(path.join(tmp, mutation), ' ');
      assert.throws(() => pass04(tmp), /Pass-4/);
    } finally {
      if (!path.resolve(tmp).startsWith(path.resolve(os.tmpdir()) + path.sep)) throw new Error('Unsafe test cleanup');
      fs.rmSync(tmp, {recursive:true,force:true});
    }
  });
}
