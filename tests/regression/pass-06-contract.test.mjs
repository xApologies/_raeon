import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {pass06,matchesPass06,pass06Sources} from '../../tools/validators/pass-06-contract.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
test('Pass-6 exact amendment preserves sixty compiled predecessors and every inherited test',()=>{
  const d=pass06(root);
  assert.equal(d.starting_sha,'388a241ba5674c157131601aad677ab52350f2c6');
  assert.equal(d.compiled_total,74);assert.equal(Object.keys(d.compiled_sources).length,14);
  assert.equal(d.open_items.length,12);assert.equal(d.whole_game_phase,'PREPRODUCTION');
  assert.equal(d.pass07_implemented,false);
});
test('Pass-6 amendment rejects unrelated paths and either altered endpoint',()=>{
  const d=pass06(root);
  for (const [file,pair] of Object.entries(d.changes)) {
    assert.equal(matchesPass06(root,file,pair.after_sha256,pair.before_sha256),true);
    assert.equal(matchesPass06(root,file,'0'.repeat(64),pair.before_sha256),false);
    assert.equal(matchesPass06(root,file,pair.after_sha256,'0'.repeat(64)),false);
  }
  assert.equal(matchesPass06(root,'data/qmo/invented.json','0'.repeat(64),'0'.repeat(64)),false);
});
test('Pass-6 exact pairs support minimal historical fixtures without accepting arbitrary bytes',()=>{
  const workspaceBuild=path.resolve(root,'build');
  const temp=fs.mkdtempSync(path.join(workspaceBuild,'raeon-pass06-pairs-'));
  try {
    for (const [file,pair] of Object.entries(pass06(root).changes)) {
      assert.equal(matchesPass06(temp,file,pair.after_sha256,pair.before_sha256),true);
      assert.equal(matchesPass06(temp,file,'f'.repeat(64),pair.before_sha256),false);
    }
  } finally {
    assert.ok(path.resolve(temp).startsWith(workspaceBuild+path.sep));
    fs.rmSync(temp,{recursive:true,force:true});
  }
});
test('Pass-6 compiled amendment cannot replace inherited Genesis source authority',()=>{
  const d=pass06(root);const first=Object.keys(d.compiled_sources)[0];
  assert.throws(()=>pass06Sources(root,['provenance/decisions/raeon-pass-06.json'],{[first]:d.compiled_sources[first]}),/cannot replace/);
});
