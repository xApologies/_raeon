import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';
import {validateRuntimeSources} from '../../tools/validators/genesis-runtime-contract.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const inventory = JSON.parse(fs.readFileSync(path.join(root, 'data/manifests/current-files.json'))).files;
const decision = JSON.parse(fs.readFileSync(path.join(root, 'provenance/decisions/raeon-pass-02.json')));
test('Pass-2 exact source amendment retains all preceding authorities', () => {
  assert.deepEqual(validateRuntimeSources(root, inventory), []);
});
for (const file of ['game/core/raeon/application/catalog.json', 'game/core/raeon/application/draw_one.gen',
  'game/core/genesis_horizon/src/values/at_most.gen', 'provenance/decisions/raeon-pass-02.json',
  'data/cycles/cycle_01/field_generators/objects.json', 'tests/integration/genesis_horizon/pass_01_application/manifest.json']) {
  test('Pass-2 source guard rejects alteration of ' + file, () => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'raeon-pass02-guard-'));
    try {
      const required = [...inventory.filter(p => p.endsWith('.gen')), ...Object.keys(decision.package_files),
        ...Object.keys(decision.source_inputs), 'provenance/decisions/raeon-pass-02.json',
        'provenance/decisions/raeon-pass-01.json', 'provenance/decisions/genesis-runtime-build.json',
        ...inventory.filter(p => p.startsWith('tests/integration/genesis_horizon/pass_01_application/'))];
      for (const relative of new Set(required)) {
        fs.mkdirSync(path.dirname(path.join(tmp, relative)), {recursive:true});
        fs.copyFileSync(path.join(root, relative), path.join(tmp, relative));
      }
      fs.appendFileSync(path.join(tmp, file), ' ');
      assert.notEqual(validateRuntimeSources(tmp, inventory).length, 0);
    } finally {
      if (!path.resolve(tmp).startsWith(path.resolve(os.tmpdir()) + path.sep)) throw new Error('Unsafe temporary cleanup');
      fs.rmSync(tmp, {recursive:true, force:true});
    }
  });
}
