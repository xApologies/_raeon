import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';
import {resolveRepositoryPath} from './load-design-state.mjs';

export function loadContinuity(root) {
 const json=p=>JSON.parse(fs.readFileSync(resolveRepositoryPath(root,p),'utf8'));
 const index=json('data/manifests/accepted-state.json');
 const manifest=json(index.continuity_import);
 const data=Object.fromEntries(Object.entries(manifest.datasets).map(([key,p])=>[key,json(p)]));
 return {manifest,...data};
}
export function validateContinuityData(s) {
 const errors=[];let checks=0;
 const check=(ok,label)=>{checks++;if(!ok)errors.push(label);};
 const same=(actual,expected,label)=>check(isDeepStrictEqual(actual,expected),label);
 try {
 const m=s.manifest,c=s.configuration_spaces.values,g=s.generator_interaction.values,b=s.board.values,r=s.relationships.values;
 same(m.phase,'PREPRODUCTION','Continuity cannot advance production');same(m.gameplay_implemented,false,'No gameplay implementation claim');
 same(m.propagation.r88_status,'OPEN','R88 stays OPEN');same(m.propagation.selected_branch,null,'R88 branches remain unselected');
 same(m.propagation.integration_status,'UNTESTED','Source claims are not local mathematical validation');same(m.propagation.game_catalogs_imported,false,'Research source does not import game catalogs');same(m.propagation.raeon_generator_mapping,'OPEN','Research-to-Generator mapping remains OPEN');
 same(c.general_term,'Configuration Space','Configuration Space terminology');same(c.permanent_ids,['A','B','C'],'Permanent identities');same(c.permanent_universal,true,'Permanent spaces universal');
 same(c.minimum_states,['EMPTY','CONFIGURING','RESOLVED'],'Configuration states');same(c.transitions,{first_commitment:'EMPTY -> CONFIGURING',valid_closure:'CONFIGURING -> RESOLVED'},'Closure-gated state transition');
 same(c.configuring_is_active,true,'Unresolved configuration remains active');same(c.failed_closure_auto_graveyard,false,'No failed-closure Graveyard penalty');same(c.screen_position_is_identity,false,'Coordinates are not identity');
 for(const key of ['resolved_reopening','temporary_expiry','fusion_permanent_base_accounting'])same(c[key],'OPEN','Unresolved Configuration Space rule: '+key);
 same(c.graveyard_requires_separate_accepted_rule,true,'Graveyard requires an accepted routing rule');
 same(g.object_kind,'QMO / mathematical configuration object','First-class Generator QMO');same(g.derivation,['Chirality Fabric','Propagation Engine','QMO landscape','Field Generator catalog'],'Generator derivation intent');
 same(g.configuration_notation.authority,'WORKING DESIGN','Notation not a completed mathematical operator');same(g.orientation_permission,'Generator/domain/QMO-admitted states','Admissible orientation');
 same(g.arbitrary_free_xyz_rotation,false,'No arbitrary free XYZ rotation');same(g.orientation_changes_mathematical_state,true,'Orientation changes actual configuration');same(g.individual_committed_extraction,false,'No individual extraction');
 same(g.closure_before_color,true,'Closure before color');same(g.count_alone_authorizes_closure,false,'Count is not mathematical permission');same(g.outcomes,['VALID','TERMINATES','NOT_APPLICABLE','OPEN','UNTESTED'],'Explicit outcomes');same(g.missing_data_is_termination,false,'Missing data is not termination');same(g.failed_closure_auto_graveyard,false,'No invented closure penalty');same(g.catalog_status,'SOURCE_IMPORT_REQUIRED','Generator catalog missing');same(g.objects,[],'No fabricated Generators');
 same(b.center_divider,'Genesis Horizon','Board divider');same(b.infrastructure,['Deck','Hand','Graveyard'],'Only accepted infrastructure zones');same(b.discard_pile,false,'No discard pile');same(b.exile_zone,false,'No exile zone');same(b.prime_positions,3,'Three Prime positions');same(b.prime_positions_fixed,true,'Fixed Prime positions');same(b.opponent_hand_hidden,true,'Opponent hand hidden');
 same(b.starting_spaces,c.permanent_ids,'Board/space identity mirror');same(b.identity_persists_on_reposition,true,'Space identity persists');same(b.screen_coordinates_are_presentation,true,'Coordinates are presentation');same(b.views,['strategic','configuration'],'Two views');same(b.shared_underlying_state,true,'Views share one state');same(b.configuring_space_visible,true,'Unresolved field visible');same(b.exact_layout_camera_controls,'OPEN','Exact UI remains open');
 same(r.fusion.requires_mathematical_admission,true,'Fusion permission');same(r.fusion.result,'DerivedLocalManifoldQMO','Fusion result');same(r.fusion.resolved_spaces_before,2,'Fusion input');same(r.fusion.derived_spaces_after,1,'Fusion derived space');same(r.fusion.supports_independently_operational,false,'Fused supports not independent');same(r.fusion.permanent_base_identity_accounting,'OPEN','Do not silently resolve permanent-base conflict');
 same(r.emergence.requires_mathematical_admission,true,'Emergence permission');same(r.emergence.supports_remain_distinct,true,'Emergent supports remain');same(r.emergence.directly_attackable,false,'Emergence not targetable');same(r.emergence.independently_destroyable,false,'Emergence not independently destroyable');same(r.emergence.required_support_loss,'removed/inaccessible','Support-loss consequence');same(r.emergence.amplification_changes_support_rule,false,'Amplification preserves support');same(r.relation_check_timing,'OPEN','Relation timing remains open');
 same(s.prime_working_model.authority,'PROVISIONAL','Prime model remains provisional');same(s.prime_working_model.values.catalog,'OPEN','Prime catalog remains open');same(s.prime_working_model.values.exact_operators,'OPEN','Prime operators remain open');
 } catch(error){errors.push('Malformed continuity: '+error.message);}
 return {errors,checks};
}
export function validateContinuityRepository(root) {
 const result={errors:[],checks:0};const check=(ok,label)=>{result.checks++;if(!ok)result.errors.push(label);};
 const file=p=>resolveRepositoryPath(root,p),json=p=>JSON.parse(fs.readFileSync(file(p),'utf8'));
 const hash=p=>createHash('sha256').update(fs.readFileSync(file(p))).digest('hex');
 try {
  const state=loadContinuity(root),semantic=validateContinuityData(state);result.errors.push(...semantic.errors);result.checks+=semantic.checks;
  for(const [name,p]of Object.entries(state.manifest.datasets)){
   const d=json(p);check(d.schema_version===1,'Dataset schema: '+p);check(fs.existsSync(file(d.design)),'Dataset design home: '+name);
  }
  const index=json('data/manifests/accepted-state.json');check(isDeepStrictEqual(state.manifest.source_import_required,index.source_import_required),'Source requirements retained with partial-receipt distinction');
  const authority=json('data/manifests/authority-map.json');check(authority.continuity_import===index.continuity_import,'Current authority map reaches continuity');
  for(const p of Object.values(authority.supplemental_data))check(fs.existsSync(file(p)),'Authority supplemental dataset: '+p);
  const source='provenance/sources/final-continuity',receipt=json(source+'/receipt.json');
  const archive=receipt.propagation_archive,bytes=fs.readFileSync(file(archive.path));
  if(bytes.subarray(0,80).toString().startsWith('version https://git-lfs.github.com/spec/v1')) {
   check(bytes.toString()===`version https://git-lfs.github.com/spec/v1\noid sha256:${archive.sha256}\nsize ${archive.bytes}\n`,'LFS pointer matches received archive');
  } else check(bytes.length===archive.bytes&&createHash('sha256').update(bytes).digest('hex')===archive.sha256,'Full Propagation archive integrity');
  const outer=json(source+'/handoff/MANIFEST.json');
  for(const entry of outer.files){const p=source+'/handoff/'+entry.path;if(p===archive.path)continue;check(fs.statSync(file(p)).size===entry.bytes&&hash(p)===entry.sha256,'Received source bytes unchanged: '+entry.path);}
  for(const entry of json(source+'/extracted-files.json'))check(hash(entry.path)===entry.sha256,'Extracted source integrity: '+entry.path);
  const before=json('provenance/audits/final-continuity-baseline.json').sha256;
  for(const [p,expected]of Object.entries(before))if((p.startsWith('provenance/')&&p!=='provenance/README.md')||p.startsWith('development/checkpoints/')||p.startsWith('game/'))check(hash(p)===expected,'Historical evidence/runtime boundary preserved: '+p);
  const inventory=json('data/manifests/current-files.json');check(inventory.files.length===inventory.file_count,'Current inventory count');
  const visited=new Set();for(const p of inventory.files){check(!visited.has(p),'Unique current file: '+p);visited.add(p);check(fs.existsSync(file(p)),'Current file exists: '+p);}
 }catch(error){result.errors.push('Continuity repository validation failed: '+error.message);}
 return result;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
 const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..'),r=validateContinuityRepository(root);
 for(const e of r.errors)console.error('FAIL: '+e);
 console.log(`${r.errors.length?'FAIL':'PASS'} — ${r.checks} continuity checks; ${r.errors.length} error(s).`);
 console.log('Scope: recovered structure, source integrity and preservation; NOT mathematical proof, game balance or runtime verification. LFS pointers validate identity; a hydrated archive validates all source bytes.');
 if(r.errors.length)process.exitCode=1;
}
