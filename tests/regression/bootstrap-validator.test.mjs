import {test} from 'node:test';
import {copyFixtureFile} from './fixture-files.mjs';
import {loadDesignState} from '../../tools/validators/load-design-state.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';

// Temporary fixtures derive only from this repository; they contain no game tests.
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
function fixture() {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'raeon-bootstrap-test-'));
  for(const file of JSON.parse(fs.readFileSync(path.join(root,'data/manifests/current-files.json'),'utf8')).files) {
    fs.mkdirSync(path.dirname(path.join(dir,file)),{recursive:true});
    copyFixtureFile(root,dir,file);
  }
  const init=spawnSync('git',['init',dir],{encoding:'utf8',windowsHide:true});
  assert.equal(init.status,0,init.stderr);
  return dir;
}
function run(dir) {return spawnSync(process.execPath,[path.join(dir,'tools/validators/validate-bootstrap.mjs')],{encoding:'utf8',windowsHide:true});}
function change(dir,fn){
 const p=path.join(dir,'data/manifests/accepted-state.json');const index=JSON.parse(fs.readFileSync(p,'utf8'));const data=loadDesignState(dir);fn(data);
 for(const key of ['authority','source','sources','production','source_import_required','open_items'])index[key]=data[key];
 fs.writeFileSync(p,JSON.stringify(index));
 for(const pointer of Object.values(index.datasets)){const f=path.join(dir,pointer.path);const dataset=JSON.parse(fs.readFileSync(f,'utf8'));for(const key of pointer.keys){dataset.values[key]=structuredClone(data[key]);if(key==='utility_structure')delete dataset.values[key].families;}fs.writeFileSync(f,JSON.stringify(dataset));}
 for(const [name,file]of Object.entries(index.utility_families)){const f=path.join(dir,file);const dataset=JSON.parse(fs.readFileSync(f,'utf8'));dataset.values=data.utility_structure.families[name];fs.writeFileSync(f,JSON.stringify(dataset));}
}
const cases=[
 ['accepts baseline and creates untracked local inbox',null,null],
 ['rejects missing required module',d=>fs.unlinkSync(path.join(d,'development/modules/qmo-engine/README.md')),'Required file missing'],
 ['rejects compensating Cycle count changes',d=>change(d,s=>{s.cycle_01.ordinary_cards.field_generators--;s.cycle_01.ordinary_cards.utilities++;}),'Cycle-1 card counts'],
 ['rejects Black Field Generators',d=>change(d,s=>s.field_generators.black_allowed=true),'Black Field Generators prohibited'],
 ['rejects fabricated QMO import claims',d=>change(d,s=>s.qmo_inventory.objects_imported=true),'External QMO inventory claim'],
 ['rejects premature production promotion',d=>change(d,s=>s.production.phase='PROTOTYPE'),'Current whole-game phase'],
 ['rejects completed slice criteria',d=>{const p=path.join(d,'production/03_vertical_slice/EXIT_CRITERIA.md');fs.writeFileSync(p,fs.readFileSync(p,'utf8').replace('- [ ]','- [x]'));},'Slice criteria must not be marked complete'],
 ['rejects missing inbox ignore rule',d=>fs.writeFileSync(path.join(d,'.gitignore'),''),'Root /_inbox/ ignore rule missing'],
 ['rejects force-tracked inbox files',d=>{fs.mkdirSync(path.join(d,'_inbox'));fs.writeFileSync(path.join(d,'_inbox/handoff.txt'),'local only');const add=spawnSync('git',['-C',d,'add','-f','_inbox/handoff.txt'],{encoding:'utf8',windowsHide:true});assert.equal(add.status,0,add.stderr);},'_inbox content is tracked'],
 ['rejects altered source evidence',d=>fs.appendFileSync(path.join(d,'provenance/sources/bootstrap-request.txt'),'changed'),'Bootstrap source integrity'],
];
for(const [name,mutate,expected]of cases)test(name,()=>{
 const dir=fixture();
 try {if(mutate)mutate(dir); const result=run(dir);assert.equal(result.status,expected?1:0,result.stdout+result.stderr);if(expected)assert.ok(result.stderr.includes(expected),result.stderr);else assert.ok(fs.existsSync(path.join(dir,'_inbox')));}
 finally {const resolved=path.resolve(dir);assert.equal(path.dirname(resolved),path.resolve(os.tmpdir()));assert.ok(path.basename(resolved).startsWith('raeon-bootstrap-test-'));fs.rmSync(resolved,{recursive:true,force:true});}
});
