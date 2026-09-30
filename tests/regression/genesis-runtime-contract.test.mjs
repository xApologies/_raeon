import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';
import {runtimeDecision, validateRuntimeSources} from '../../tools/validators/genesis-runtime-contract.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const decision = JSON.parse(fs.readFileSync(path.join(root, runtimeDecision), 'utf8'));
const files = Object.keys(decision.compiled_sources);
test('real compiled Genesis source set has an exact authorized amendment', () => {
  assert.deepEqual(validateRuntimeSources(root, files), []);
});
test('historical source-free inventory remains valid', () => {
  assert.deepEqual(validateRuntimeSources(root, []), []);
});
for (const mutation of ['changed source', 'extra source', 'changed decision']) {
  test('runtime amendment rejects ' + mutation, () => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'raeon-runtime-contract-'));
    try {
      for (const file of [...files, runtimeDecision]) {
        fs.mkdirSync(path.dirname(path.join(tmp, file)), {recursive: true});
        fs.copyFileSync(path.join(root, file), path.join(tmp, file));
      }
      const inventory = [...files];
      if (mutation === 'changed source') fs.appendFileSync(path.join(tmp, files[0]), '\n// unaudited change\n');
      if (mutation === 'extra source') inventory.push('game/unauthorized.gen');
      if (mutation === 'changed decision') fs.appendFileSync(path.join(tmp, runtimeDecision), ' ');
      assert.notEqual(validateRuntimeSources(tmp, inventory).length, 0);
    } finally {
      if (!path.resolve(tmp).startsWith(path.resolve(os.tmpdir()) + path.sep)) throw new Error('Unsafe temporary cleanup');
      fs.rmSync(tmp, {recursive: true, force: true});
    }
  });
}
