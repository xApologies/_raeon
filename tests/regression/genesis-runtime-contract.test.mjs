import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';
import {runtimeDecision, validateRuntimeSources, matchesRuntimeNavigation} from '../../tools/validators/genesis-runtime-contract.mjs';

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

test('runtime navigation accepts only its exact before/after hashes', () => {
  assert.equal(matchesRuntimeNavigation('game/core/README.md', 'f24c2020fe41df0e889f093dcbd8e19424fd3931d273897641ce048376885a44', 'b160d475b108a6edac295e76dada06ac36037e5c771ff20168574b63119e3562'), true);
});
test('runtime navigation rejects unrelated or altered content', () => {
  assert.equal(matchesRuntimeNavigation('game/core/README.md', '0'.repeat(64), 'b160d475b108a6edac295e76dada06ac36037e5c771ff20168574b63119e3562'), false);
  assert.equal(matchesRuntimeNavigation('game/other.md', 'f24c2020fe41df0e889f093dcbd8e19424fd3931d273897641ce048376885a44', 'b160d475b108a6edac295e76dada06ac36037e5c771ff20168574b63119e3562'), false);
});
test('runtime navigation does not rewrite a different historical baseline', () => {
  assert.equal(matchesRuntimeNavigation('game/core/README.md', 'f24c2020fe41df0e889f093dcbd8e19424fd3931d273897641ce048376885a44', '0'.repeat(64)), false);
});
