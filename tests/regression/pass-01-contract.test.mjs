import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {runtimeDecision, validateRuntimeSources} from '../../tools/validators/genesis-runtime-contract.mjs';
import {passDecision} from '../../tools/validators/pass-01-contract.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const base = JSON.parse(fs.readFileSync(path.join(root, runtimeDecision)));
const pass = JSON.parse(fs.readFileSync(path.join(root, passDecision)));
const sources = [...Object.keys(base.compiled_sources), ...Object.keys(pass.compiled_sources)];
const files = [...new Set([...sources, ...Object.keys(pass.package_files), runtimeDecision, passDecision])];

function copyHistorical(tmp) {
  for (const file of files) {
    fs.mkdirSync(path.dirname(path.join(tmp, file)), {recursive: true});
    const original = file.startsWith('game/core/raeon/application/')
      ? file.replace('game/core/raeon/application/', 'tests/integration/genesis_horizon/pass_01_application/') : file;
    fs.copyFileSync(path.join(root, original), path.join(tmp, file));
  }
}
test('Pass-1 exact package and compiled sources are authorized together', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'raeon-pass01-historical-'));
  try { copyHistorical(tmp); assert.deepEqual(validateRuntimeSources(tmp, files), []); }
  finally {
    if (!path.resolve(tmp).startsWith(path.resolve(os.tmpdir()) + path.sep)) throw new Error('Unsafe temporary cleanup');
    fs.rmSync(tmp, {recursive:true, force:true});
  }
});
test('original diplomatic pouch is preserved byte for byte', () => {
  const bytes = fs.readFileSync(path.join(root, 'provenance/sources/raeon-pass-01/diplomatic-pouch.zip'));
  assert.equal(createHash('sha256').update(bytes).digest('hex'), pass.pouch_sha256);
});
for (const mutation of ['source', 'manifest', 'definitions', 'decision', 'missing source', 'extra source']) {
  test('Pass-1 integrity rejects ' + mutation, () => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'raeon-pass01-contract-'));
    try {
      copyHistorical(tmp);
      const inventory = [...files];
      const target = {source:'game/core/raeon/application/raeon_realize.gen', manifest:'game/core/raeon/application/manifest.json',
        definitions:'game/core/raeon/application/definitions.json', decision:passDecision}[mutation];
      if (target) fs.appendFileSync(path.join(tmp, target), ' ');
      if (mutation === 'missing source') inventory.splice(inventory.indexOf('game/core/raeon/application/raeon_realize.gen'), 1);
      if (mutation === 'extra source') inventory.push('game/core/raeon/application/unapproved.gen');
      assert.notEqual(validateRuntimeSources(tmp, inventory).length, 0);
    } finally {
      if (!path.resolve(tmp).startsWith(path.resolve(os.tmpdir()) + path.sep)) throw new Error('Unsafe temporary cleanup');
      fs.rmSync(tmp, {recursive:true, force:true});
    }
  });
}
