import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {pass03, pass03Decision} from '../../tools/validators/pass-03-contract.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const decision = JSON.parse(fs.readFileSync(path.join(root, pass03Decision)));
test('Pass-3 exact additive amendment retains earlier test sources and corpus', () => {
  assert.equal(pass03(root).status, 'PARTIAL');
});
for (const mutation of ['game/qmo/corpus.py','game/sandbox/topology.py',
  'game/core/raeon/application/set_fg_poses.gen','game/qmo/cycle1.lock.json',pass03Decision]) {
  test('Pass-3 source guard rejects modified ' + mutation, () => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(),'raeon-pass03-'));
    try {
      for (const file of new Set([...Object.keys(decision.sources),...Object.keys(decision.changes),pass03Decision])) {
        const target = path.join(tmp,file);
        fs.mkdirSync(path.dirname(target),{recursive:true});
        fs.copyFileSync(path.join(root,file),target);
      }
      fs.appendFileSync(path.join(tmp,mutation),' ');
      assert.throws(() => pass03(tmp), /Pass-3/);
    } finally {
      if (!path.resolve(tmp).startsWith(path.resolve(os.tmpdir())+path.sep)) throw new Error('Unsafe temporary cleanup');
      fs.rmSync(tmp,{recursive:true,force:true});
    }
  });
}
