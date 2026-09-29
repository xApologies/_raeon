import {test} from 'node:test';
import {projectBeforeFullMigration} from '../../tools/validators/full-migration-contract.mjs';
import {projectBeforeCycle1Import} from '../../tools/validators/cycle1-status.mjs';
import {copyFixtureFile} from './fixture-files.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {loadDesignState} from '../../tools/validators/load-design-state.mjs';
import {validateNormalization} from '../../tools/validators/validate-normalization.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const read=(dir,p)=>JSON.parse(fs.readFileSync(path.join(dir,p),'utf8'));
function edit(dir,p,fn){const value=read(dir,p);fn(value);fs.writeFileSync(path.join(dir,p),JSON.stringify(value));}
test('normalized state preserves unamended checkpoint-0003 values with reviewed design/source amendments',()=>{const actual=projectBeforeCycle1Import(projectBeforeFullMigration(root,loadDesignState(root))),expected=read(root,'provenance/audits/0004-before-state.json');actual.schema_version=expected.schema_version;actual.current_design_checkpoint=expected.current_design_checkpoint;assert.deepEqual(actual,expected);});
const cases=[
 ['accepts normalized repository',()=>{},null],
 ['rejects fabricated QMO source objects',d=>edit(d,'data/qmo/fusion/status.json',v=>v.objects=[{id:'invented'}]),'Unfabricated source/catalog boundary'],
 ['rejects undeclared inline current rules',d=>edit(d,'data/manifests/accepted-state.json',v=>v.gameplay={new_rule:true}),'High-level index has only declared metadata/pointers'],
 ['rejects changed family payload',d=>edit(d,'data/cycles/cycle_01/utilities/transduction.json',v=>v.values.restore[0].charge_delta=2),'Lossless migration'],
 ['rejects escaped dataset pointer',d=>edit(d,'data/manifests/accepted-state.json',v=>v.datasets.cards.path='../outside.json'),'Unsafe repository pointer'],
 ['rejects duplicate encoded keys',d=>edit(d,'data/manifests/accepted-state.json',v=>v.datasets.duplicate=v.datasets.cards),'Duplicate/unsafe semantic key'],
 ['rejects mismatched Utility family',d=>edit(d,'data/cycles/cycle_01/utilities/recovery.json',v=>v.family='draw_deck'),'Utility family identity mismatch'],
 ['rejects duplicate current specification',d=>fs.appendFileSync(path.join(d,'design/cards/README.md'),'\n<!-- raeon:current-spec utilities -->\n'),'Competing current authority'],
 ['rejects disconnected module dashboard',d=>{const p=path.join(d,'development/modules/utilities/README.md');fs.writeFileSync(p,fs.readFileSync(p,'utf8').replaceAll('../../../design/cards/cycle_01/utilities/SYSTEM.md','missing-spec.md'));},'Dashboard upstream/downstream link'],
 ['rejects missing runtime boundary',d=>fs.unlinkSync(path.join(d,'game/cards/primes/README.md')),'Runtime boundary: cards/primes'],
 ['rejects historical checkpoint modification',d=>fs.appendFileSync(path.join(d,'provenance/checkpoints/0003-cumulative-recovery.md'),'changed'),'Historical bytes / authorized governance hash'],
 ['rejects family data reintroduced in overview',d=>edit(d,'data/cycles/cycle_01/utilities/overview.json',v=>v.values.utility_structure.families={}),'Utility overview must not duplicate'],
 ['rejects broken local link',d=>fs.appendFileSync(path.join(d,'design/cards/README.md'),'\n[broken](absent.md)\n'),'Broken Markdown link'],
 ['rejects loss of original family prose',d=>{const p=path.join(d,'design/cards/cycle_01/utilities/draw_deck/SYSTEM.md');fs.writeFileSync(p,fs.readFileSync(p,'utf8').replace('Raw draw cannot exceed Draw 3','Raw draw can exceed Draw 3'));},'Original Utility prose retained'],
];
for(const [name,mutate,expected]of cases)test(name,()=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'raeon-normalization-test-'));
 try{
  for(const p of read(root,'data/manifests/current-files.json').files){fs.mkdirSync(path.dirname(path.join(dir,p)),{recursive:true});copyFixtureFile(root,dir,p);}
  const init=spawnSync('git',['init',dir],{encoding:'utf8',windowsHide:true});assert.equal(init.status,0,init.stderr);
  mutate(dir);const result=validateNormalization(dir);if(expected)assert.ok(result.errors.some(x=>x.includes(expected)),JSON.stringify(result.errors));else assert.deepEqual(result.errors,[]);
 }finally{const resolved=path.resolve(dir);assert.equal(path.dirname(resolved),path.resolve(os.tmpdir()));assert.ok(path.basename(resolved).startsWith('raeon-normalization-test-'));fs.rmSync(resolved,{recursive:true,force:true});}
});
