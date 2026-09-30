import fs from 'node:fs';
import {projectGameDefinitionFile,projectGameDefinitionText} from './game-definition-contract.mjs';
import {projectBeforeFullMigration} from './full-migration-contract.mjs';
import {projectBeforeCycle1Import,remainingCycle1Sources} from './cycle1-status.mjs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';
import {spawnSync} from 'node:child_process';
import {loadDesignState,resolveRepositoryPath,matchesProtectedHash} from './load-design-state.mjs';

export function validateNormalization(root) {
 const errors=[];let checks=0;
 const check=(ok,label)=>{checks++;if(!ok)errors.push(label);};
 const read=p=>fs.readFileSync(resolveRepositoryPath(root,p),'utf8').replaceAll('\r\n','\n');
 const json=p=>JSON.parse(read(p));
 const exists=p=>{try{return fs.statSync(resolveRepositoryPath(root,p)).isFile();}catch{return false;}};
 try {
  const index=json('data/manifests/accepted-state.json'),map=json('data/manifests/authority-map.json');
  check(index.schema_version===4&&index.current_design_checkpoint==='0004','Schema/checkpoint must be 4/0004');
  check(!('utility_structure'in index)&&!('black'in index)&&!('cycle_01'in index),'High-level state must point to detailed datasets');
  check(isDeepStrictEqual(Object.keys(index).sort(),['schema_version','current_design_checkpoint','authority','source','sources','production','source_import_required','open_items','authority_map','datasets','utility_families','migration','continuity_import','cycle1_source_import','full_migration','game_definition_reconciliation'].sort()),'High-level index has only declared metadata/pointers');
  const snapshot=json('provenance/audits/0004-before-state.json');
  const state=loadDesignState(root);const compared=projectBeforeCycle1Import(projectBeforeFullMigration(root,state));
  compared.schema_version=snapshot.schema_version;compared.current_design_checkpoint=snapshot.current_design_checkpoint;
  check(isDeepStrictEqual(compared,snapshot),'Lossless migration: accepted semantic state differs from checkpoint 0003');
  check(state.production.phase==='PREPRODUCTION','Production phase remains PREPRODUCTION');
  check(isDeepStrictEqual(map.flow,['DESIGN','DATA','GAME','TESTS']),'Authority chain');
  const expectedSpecs=['game','match','board','progression','card-system','cycle-01','field-generators','prime-fields','utilities','utility-transduction','utility-activation','utility-sandbox_activation','utility-draw_deck','utility-recovery','utility-stability','utility-restore-prime','black','black-primes','black-utilities','black-mode','sandbox','generator-geometry','manifolds','fusion','emergent-fields','transduction','collection','economy','ai','multiplayer','rendering','ui-ux'];
  check(isDeepStrictEqual(Object.keys(map.current_specs).sort(),expectedSpecs.sort()),'All expected current-specification homes');
  const manifest=json('data/manifests/current-files.json');
  const markers=new Map();
  for(const p of manifest.files.filter(x=>x.startsWith('design/')&&x.endsWith('.md'))){
   if(!exists(p)){check(false,`Missing design file: ${p}`);continue;}
   for(const m of read(p).matchAll(/<!-- raeon:current-spec ([\w-]+) -->/g)){
    check(!markers.has(m[1]),`Competing current authority: ${m[1]}`);markers.set(m[1],p);
    check(map.current_specs[m[1]]===p,`Unregistered current authority: ${p}`);
   }
  }
  for(const [id,p]of Object.entries(map.current_specs)){check(exists(p),`Current specification exists: ${p}`);check(markers.get(id)===p,`Unique authority marker: ${id}`);}
  check(map.modules.length===27&&new Set(map.modules.map(x=>x.module)).size===27,'Twenty-seven module dashboards');
  for(const row of map.modules){
   check(map.current_specs[row.system]===row.design,`Module current design: ${row.module}`);
   for(const field of ['design','data','mathematics','implementation','tests','development','provenance'])check(exists(row[field]),`Module ${row.module} ${field} boundary missing`);
   if(exists(row.development)){
    const text=read(row.development);
    for(const field of ['design','data','mathematics','implementation','tests','provenance'])check(text.includes(path.posix.relative(path.posix.dirname(row.development),row[field])),`Dashboard upstream/downstream link: ${row.module} ${field}`);
    check(row.status===(row.module==='utilities'?'DESIGN':'OPEN'),`Unchanged maturity: ${row.module}`);
    check(!/## (?:Cumulative checkpoint|Design checkpoint)/.test(text),`Dashboard must not accumulate duplicate design notes: ${row.module}`);
   }
  }
  const rootDirs=['production','development','design','mathematics','game','content','data','tools','tests','platform','releases','provenance'];
  for(const d of rootDirs)check(exists(d+'/README.md'),`Root spine: ${d}`);
  for(const p of ['README.md','PROJECT_CONSTITUTION.md','DEVELOPMENT_CONSTITUTION.md','CONTRIBUTING.md','CHANGELOG.md'])check(exists(p),`Root governance: ${p}`);
  const runtime=['core','match','state','rules','board','cards/generators','cards/primes','cards/utilities','sandbox','qmo','manifolds','transduction','collection','ai','multiplayer','rendering','ui','persistence'];
  const tests=['unit','integration','regression','gameplay/cards','gameplay/sandbox','gameplay/manifolds','gameplay/transduction','gameplay/primes','gameplay/utilities','qmo','rendering','multiplayer','adversarial','performance'];
  for(const p of runtime)check(exists(`game/${p}/README.md`),`Runtime boundary: ${p}`);
  for(const p of tests)check(exists(`tests/${p}/README.md`),`Test boundary: ${p}`);
  const names=['transduction','activation','sandbox_activation','draw_deck','graveyard_recovery','stability_protection'];
  check(isDeepStrictEqual(Object.keys(index.utility_families).sort(),names.sort()),'Six normalized Utility family pointers');
  for(const [name,p]of Object.entries(index.utility_families)){
   const data=json(p),mirror=map.utility_families[name];
   check(data.design===mirror.design&&p===mirror.data,`Family DESIGN/DATA mirror: ${name}`);
   check(exists(data.design)&&read(data.design).includes(path.posix.relative(path.posix.dirname(data.design),p)),`Family specification links to data: ${name}`);
   check(data.family===name&&isDeepStrictEqual(projectGameDefinitionFile(root,p,data).values,snapshot.utility_structure.families[name]),`Unchanged family payload: ${name}`);
  }
  for(const pointer of Object.values(index.datasets)){const data=json(pointer.path);check(exists(data.design),`Dataset upstream specification: ${pointer.path}`);}
  check(isDeepStrictEqual(state.source_import_required,remainingCycle1Sources),'Scoped remaining source requirements');
  check(state.qmo_inventory.status==='IMPORTED_VALIDATED'&&state.qmo_inventory.objects_imported===true,'Verified QMO import transition');
  check(state.rendering_direction.qmo_renderspec_api_packages==='CYCLE1_BASE_IMPORTED_DERIVED_OPEN','Scoped RenderSpec import transition');
  check(state.cycle_production_direction.existing_source_package==='IMPORTED_VALIDATED','Constitution import transition');
  const prime=json('data/cycles/cycle_01/primes/status.json');
  check(prime.status==='STRUCTURE_ACCEPTED_DETAILS_OPEN'&&prime.objects.length===14&&new Set(prime.objects.map(x=>x.identity_key)).size===14&&prime.expected_identities===14,'Unfabricated Prime catalog boundary');
  for(const [p,count,key]of [['data/qmo/manifolds/status.json',60,'id'],['data/qmo/fusion/status.json',343,'id'],['data/qmo/emergent/status.json',1691,'id'],['data/qmo/generators/status.json',120,'card_id'],['data/cycles/cycle_01/field_generators/status.json',120,'card_id']]){
   const d=json(p),objects=json(d.objects_ref);
   check(d.status==='IMPORTED_VALIDATED'&&objects.length===count&&isDeepStrictEqual(d.objects,objects.map(x=>x[key])),'Unfabricated source/catalog boundary: '+p);
  }
  check(json('data/render_specs/direction.json').render_specs.length===60,'Sixty supplied RenderSpecs');
  const original=json('provenance/audits/0004-before-inventory.json');
  const history=original.files.filter(x=>(x.path.startsWith('provenance/')&&x.path!=='provenance/README.md')||x.path.startsWith('development/checkpoints/')||['PROJECT_CONSTITUTION.md','DEVELOPMENT_CONSTITUTION.md','development/PIPELINE.md','production/phases.json'].includes(x.path));
  for(const f of history)check(exists(f.path)&&matchesProtectedHash(f.path,createHash('sha256').update(fs.readFileSync(path.join(root,f.path))).digest('hex'),f.sha256),`Historical bytes / authorized governance hash: ${f.path}`);
  for(const r of map.redirects)check(exists(r.from)&&read(r.from).startsWith('# Relocated')&&read(r.from).includes(path.posix.relative(path.posix.dirname(r.from),r.to)),`Legacy redirect: ${r.from}`);
  const source=json('provenance/sources/0004-handoff.json');
  check(createHash('sha256').update(fs.readFileSync(path.join(root,'provenance/sources/0004-CODEX_PROMPT.md'))).digest('hex')===source.directive_sha256,'Handoff directive integrity');
  const previousDesign=json('provenance/audits/0004-before-design.json').files['design/cards/cycle_01/UTILITIES.md'];
  const sections=Object.fromEntries(previousDesign.split(/^## /m).slice(1).map(x=>{const i=x.indexOf('\n');return[x.slice(0,i).trim(),x.slice(i+1).trim()];}));
  for(const [dir,heading]of [['transduction','Transduction — 18'],['activation','Activation — 7'],['sandbox_activation','Sandbox Activation — 6'],['draw_deck','Draw / Deck — 7'],['recovery','Graveyard / Recovery — 6'],['stability','Stability / Protection — 6']])check(projectGameDefinitionText(root,`design/cards/cycle_01/utilities/${dir}/SYSTEM.md`,read(`design/cards/cycle_01/utilities/${dir}/SYSTEM.md`)).includes(sections[heading]),`Original Utility prose retained: ${dir}`);
  for(const p of manifest.files){
   check(exists(p),`Inventory file exists: ${p}`);
   if(exists(p)&&p.endsWith('.md'))for(const m of read(p).matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){
    const dest=m[1].split('#')[0];if(!dest||/^[a-z]+:/i.test(dest))continue;
    check(fs.existsSync(path.resolve(root,path.posix.dirname(p),dest)),`Broken Markdown link: ${p} → ${dest}`);
   }
  }
  const tracked=spawnSync('git',['-C',root,'ls-files','-z','--','_inbox'],{encoding:'utf8',windowsHide:true});
  check(tracked.status===0&&!tracked.stdout,'Inbox must remain untracked');
  const ignored=spawnSync('git',['-C',root,'check-ignore','--no-index','_inbox/probe.txt'],{encoding:'utf8',windowsHide:true});check(ignored.status===0,'Inbox must remain ignored');
 }catch(error){errors.push(`Normalization validation failed: ${error.message}`);}
 return {errors,checks};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const result=validateNormalization(path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..'));
 for(const error of result.errors)console.error(`FAIL: ${error}`);
 console.log(`${result.errors.length?'FAIL':'PASS'} — ${result.checks} normalization checks; ${result.errors.length} error(s).`);
 console.log('Scope: repository, data migration, links and history only; NOT QMO mathematics, gameplay balance, final timing, rendering, AI or multiplayer correctness.');
 if(result.errors.length)process.exitCode=1;
}
