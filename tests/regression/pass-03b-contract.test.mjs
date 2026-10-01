import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {pass03b, pass03bDecision} from '../../tools/validators/pass-03b-contract.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const decision = JSON.parse(fs.readFileSync(path.join(root, pass03bDecision)));
test('Pass-3B exact amendment preserves all earlier tests and source datasets', () => {
  assert.equal(pass03b(root).whole_game_phase, 'PREPRODUCTION');
});
for (const mutation of ['game/qmo/realization.py', 'game/sandbox/topology.py',
  'data/game/configuration_realization/v1/BASE_MANIFOLD_WITNESSES.json',
  'data/game/configuration_realization/v1/ROTATION_CLASS_TABLE.json',
  'game/core/raeon/application/resolve_configuration.gen', pass03bDecision]) {
  test('Pass-3B guard rejects changed ' + mutation, () => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'raeon-p3b-'));
    try {
      for (const file of new Set([...Object.keys(decision.sources), ...Object.keys(decision.changes),
        ...Object.keys(decision.preserved_tests), pass03bDecision])) {
        const target = path.join(tmp, file);
        fs.mkdirSync(path.dirname(target), {recursive: true});
        fs.copyFileSync(path.join(root, file), target);
      }
      fs.appendFileSync(path.join(tmp, mutation), ' ');
      assert.throws(() => pass03b(tmp), /Pass-3B/);
    } finally {
      if (!path.resolve(tmp).startsWith(path.resolve(os.tmpdir()) + path.sep)) throw new Error('Unsafe test cleanup');
      fs.rmSync(tmp, {recursive: true, force: true});
    }
  });
}
