import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {pass05,pass05Decision,projectPass05File,pass05Sources} from '../../tools/validators/pass-05-contract.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const decision=JSON.parse(fs.readFileSync(path.join(root,pass05Decision)));
test('Pass-5 authenticated authority preserves tests, source history, QMO and maturity',()=>{
  assert.equal(pass05(root).whole_game_phase,'PREPRODUCTION');
  assert.equal(Object.keys(decision.compiled_sources).length,14);
  assert.equal(Object.keys(decision.preserved_tests).length,67);
  assert.equal(decision.open_items.length,16);
});
for(const mutation of ['game/primes/nodes.py','game/match/state.py',
  'game/core/genesis_horizon/bindings/python/src/raeon_genesis_horizon/adapter.py',
  'game/core/raeon/application/manifest.json','game/core/raeon/application/defense_restore.gen',
  'data/game/pass-05-runtime.json','data/game/match.json',
  'tests/integration/genesis_horizon/fixtures/pass04-checkpoint.zip',
  'tests/integration/genesis_horizon/test_pass_04.py',
  'development/modules/core-game/PASS_04_RECEIPT.md',pass05Decision]) {
  test('Pass-5 valid complete fixture then rejects changed '+mutation,()=>{
    const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'raeon-p5-'));
    try {
      for(const file of new Set([...Object.keys(decision.sources),...Object.keys(decision.changes),
        ...Object.keys(decision.preserved_tests),...Object.keys(decision.qmo_sources),
        ...Object.keys(decision.sealed_receipts),pass05Decision])) {
        const target=path.join(tmp,file);fs.mkdirSync(path.dirname(target),{recursive:true});
        fs.copyFileSync(path.join(root,file),target);
      }
      assert.equal(pass05(tmp).starting_sha,decision.starting_sha);
      fs.appendFileSync(path.join(tmp,mutation),' ');
      assert.throws(()=>pass05(tmp),/Pass-5/);
    } finally {
      if(!path.resolve(tmp).startsWith(path.resolve(os.tmpdir())+path.sep))throw Error('Unsafe test cleanup');
      fs.rmSync(tmp,{recursive:true,force:true});
    }
  });
}
test('Pass-5 metadata cannot conceal unrelated historical-value changes',()=>{
  const file='data/game/match.json';const value=JSON.parse(fs.readFileSync(path.join(root,file)));
  const projected=projectPass05File(root,file,value);
  assert.deepEqual(projected.values,value.values);assert.equal(projected.effective_authority,undefined);
  value.effective_authority.unaccepted=true;
  assert.throws(()=>projectPass05File(root,file,value),/authority pointer/);
});
test('Pass-5 compilation amendment cannot replace an inherited source',()=>{
  const file=Object.keys(decision.compiled_sources)[0];
  assert.throws(()=>pass05Sources(root,[pass05Decision],{[file]:decision.compiled_sources[file]}),/cannot replace/);
});
