import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {copyFixtureFile} from './fixture-files.mjs';
import {validateCycle1Import} from '../../tools/validators/validate-cycle1-import.mjs';
import {queryCycle1} from '../../tools/qmo/query-cycle1.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const json=(r,p)=>JSON.parse(fs.readFileSync(path.join(r,p),'utf8'));
const edit=(r,p,fn)=>{const v=json(r,p);fn(v);fs.writeFileSync(path.join(r,p),JSON.stringify(v));};
test('recovered source archives and all normalized representations agree',()=>assert.deepEqual(validateCycle1Import(root).errors,[]));
test('read-only queries expose catalog and preserve explicit unknown outcomes',()=>{
 assert.equal(queryCycle1(root,'fg','FG-120').card_id,'FG-120');
 assert.equal(queryCycle1(root,'base','M-R-01').generator_count,3);
 assert.equal(queryCycle1(root,'atlas').counts.total,2094);
 assert.deepEqual(queryCycle1(root,'pair','M-B-01','M-B-02'),queryCycle1(root,'pair','M-B-02','M-B-01'));
 assert.equal(queryCycle1(root,'pair','missing','M-B-01').status,'OPEN');
 assert.equal(queryCycle1(root,'fg','FG-121').status,'OPEN');
 assert.equal(queryCycle1(root,'render','../../outside').status,'OPEN');
});
test('RenderSpec query preserves every original 64-bit seed token',()=>{
 for(const row of json(root,'data/render_specs/cycle_01/catalog.json')){
  const raw=fs.readFileSync(path.join(root,'data/render_specs/cycle_01',row.manifold_id+'.json'),'utf8');
  assert.equal(queryCycle1(root,'render',row.manifold_id),raw);
  const seed=raw.match(/"deterministic_seed":\s*(\d+)/)[1];
  assert.ok(BigInt(seed)>BigInt(Number.MAX_SAFE_INTEGER));
 }
});
for(const [name,mutate,label]of [
 ['archive tampering',d=>fs.appendFileSync(path.join(d,'provenance/sources/cycle1-originals/authoritative_sources/RAEON_COMPLETE_QMO_ATLAS_CYCLE1.zip'),'bad'),'Original archive SHA-256'],
 ['missing FG',d=>edit(d,'data/cycles/cycle_01/field_generators/objects.json',v=>v.pop()),'Exact field_generators count'],
 ['duplicate FG ID',d=>edit(d,'data/cycles/cycle_01/field_generators/objects.json',v=>v[0].card_id=v[1].card_id),'Unique FG IDs'],
 ['broken support',d=>edit(d,'data/qmo/cycle1/derived_qmos.json',v=>v[0].support[0]='M-ABSENT'),'Support manifold resolves'],
 ['missing pair',d=>edit(d,'data/qmo/cycle1/manifold_pair_relations.json',v=>v.pop()),'Complete 60-choose-2 pair space'],
 ['rewritten outcome',d=>edit(d,'data/qmo/cycle1/manifold_pair_relations.json',v=>v[0].fusion_status='UNKNOWN'),'Explicit relation vocabulary'],
 ['altered atlas',d=>edit(d,'data/qmo/cycle1/atlas.json',v=>v.base[0].generators[0]='FG-120'),'Atlas Generators'],
 ['fabricated replacement and rewritten copy receipt',d=>{const p='data/cycles/cycle_01/field_generators/objects.json';edit(d,p,v=>v[0].rotation_class=999);edit(d,'provenance/sources/cycle1-originals/file-mappings.json',v=>v.find(x=>x.destination===p).sha256='0'.repeat(64));},'Normalized bytes equal original ZIP member'],
 ['cleared unrelated missing source',d=>edit(d,'data/manifests/accepted-state.json',v=>v.source_import_required.shift()),'Current source requirements'],
 ['malformed machine data',d=>fs.writeFileSync(path.join(d,'data/qmo/cycle1/atlas.json'),'{'),'Cycle-1 import validation failed']
])test('source import rejects '+name,()=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'raeon-cycle1-test-'));
 try {
  for(const p of json(root,'data/manifests/current-files.json').files){fs.mkdirSync(path.dirname(path.join(dir,p)),{recursive:true});copyFixtureFile(root,dir,p);}
  mutate(dir);const r=validateCycle1Import(dir);assert.ok(r.errors.some(e=>e.includes(label)),r.errors.join('\n'));
 }finally{
  assert.equal(path.dirname(path.resolve(dir)),path.resolve(os.tmpdir()));assert.ok(path.basename(dir).startsWith('raeon-cycle1-test-'));
  fs.rmSync(dir,{recursive:true,force:true});
 }
});
