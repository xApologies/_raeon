import fs from 'node:fs';
import {projectGameDefinitionFile,matchesGameDefinitionAmendment} from './game-definition-contract.mjs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';
import {resolveRepositoryPath,loadDesignState} from './load-design-state.mjs';
import {loadFullMigrationContract,projectBeforeFullMigration} from './full-migration-contract.mjs';
import {readSourceZip} from './source-zip.mjs';

const S='provenance/sources/full-migration-2026-09-29';
const archiveHash='48d6ca53999cc06a27e309f3f51d4ba6cb5ed3ed65592781c6a21b5dfbb1d958';
const archiveSize=242064399;
const digest=b=>createHash('sha256').update(b).digest('hex');
export function loadFullMigration(root){
 const read=p=>JSON.parse(fs.readFileSync(resolveRepositoryPath(root,p),'utf8'));
 const manifest=read('data/manifests/full-migration-2026-09-29.json');
 return {manifest,...Object.fromEntries(Object.entries(manifest.datasets).map(([k,p])=>[k,read(p)]))};
}
export function validateFullMigrationData(s){
 const errors=[];let checks=0;
 const check=(ok,label)=>{checks++;if(!ok)errors.push(label);};
 const same=(a,b,label)=>check(isDeepStrictEqual(a,b),label);
 try{
  const p=s.prime_catalog,q=s.prime_model.values,u=s.restore_prime,c=s.configuration_spaces.values,g=s.generator_interaction.values,r=s.relationships.values,b=s.board.values,v=s.runtime.values.runtime_direction;
  same(s.manifest.counts,{field_generators:120,ordinary_primes:14,ordinary_utilities:51,ordinary_total:185,preserved_atlas:2094},'185 ordinary identities');
  same(p.expected_identities,14,'Fourteen Prime identities');same(p.objects.length,14,'Complete Prime catalog');
  const colors=['Red','Orange','Yellow','Green','Blue','Violet','White'];
  const expected=[['Restore',colors.slice(2),['RESTORE']],['Degrade',colors.slice(2),['DEGRADE']],['Universal',colors.slice(0,4),['RESTORE','DEGRADE']]].flatMap(([family,ranks,directions])=>ranks.map(rank=>({identity_key:family.toLowerCase()+'_'+rank.toLowerCase(),family,rank,rank_value:colors.indexOf(rank)+1,maximum_magnitude:colors.indexOf(rank)+1,directions,copy_limit:1})));
  same(p.objects,expected,'Prime family/rank/direction constitution');same(new Set(p.objects.map(x=>x.identity_key)).size,14,'Unique structural Prime identities');same(p.copy_limit,1,'Prime copy limit');same(p.active_positions,3,'Three active Prime positions');
  same(s.prime_model.authority,'GAME_CANON','Accepted Prime H/C constitution');
  same(q.intrinsic_maximum_health,'rank','Prime H maximum');same(q.active_charge_maximum,'rank','Prime C maximum');same(q.full_health_charge_durability,'2 * rank; rank unchanged','Prime durability and identity');same(q.identity_and_rank_change_with_charge,false,'Charge never changes Prime identity');
  same(q.friendly_restore.order,['H','C'],'Restore heals H before C');same(q.friendly_restore.charge_requires_full_intrinsic_health,true,'Full H before charge');same(q.friendly_restore.overflow,'OPEN','Restore overflow remains OPEN');
  same(q.spend.partial_allowed,true,'Partial charge spending');same(q.spend.maximum,'current C','Cannot spend unavailable charge');same(q.spend.Restore,['RESTORE'],'Restore direction');same(q.spend.Degrade,['DEGRADE'],'Degrade direction');same(q.spend.Universal,['RESTORE','DEGRADE'],'Universal direction');same(q.spend.universal_maximum_rank,'Green','Universal Green ceiling');
  same(q.hostile_degradation.order,['C','H'],'Degradation hits C before H');same(q.inactive,{condition:'H = 0',state:'INACTIVE',charge:0,remains_in_fixed_prime_position:true,moves_to_graveyard:false},'INACTIVE in fixed position');
  same(u.rank,'White','White Restore Prime');same(u.count,1,'One additive Utility');
  same(u.effect,{operation:'REACTIVATE_PRIME',target:'one INACTIVE Prime',from:{H:0,C:0},to:{H:1,C:0},position_unchanged:true,identity_unchanged:true,graveyard_recovery:false,fully_heals:false,fully_charges:false},'Restore Prime reactivation to 1/0 only');
  same(q.reactivation.from,{H:0,C:0,state:'INACTIVE'},'Prime reactivation input');same(q.reactivation.to,u.effect.to,'Prime/Utility reactivation mirror');
  for(const e of q.examples){
   const max=colors.indexOf(e.rank)+1;let {H,C}=e.before;
   if(e.operation==='RESTORE'){const h=Math.min(e.amount,max-H);H+=h;C+=Math.min(e.amount-h,max-C);}
   else if(e.operation==='DEGRADE'){const charge=Math.min(e.amount,C);C-=charge;H-=Math.min(e.amount-charge,H);}
   else if(e.operation==='SPEND')C-=e.amount;
   else check(false,'Unknown Prime design example');
   same(e.after,{H,C},'Prime numerical example: '+e.operation);check(H>=0&&H<=max&&C>=0&&C<=max,'Prime example within rank limits');
  }
  same(c.persistent_container,true,'Persistent Configuration Space');same(c.field_is_current_resolved_state,true,'Resolved field is container state');same(c.resolved_reopening,'ACCEPTED','Resolved reconfiguration accepted');same(c.within_domain_reconfiguration,true,'Within-domain reconfiguration');same(c.individual_extraction_or_transfer,false,'No individual committed extraction');
  same(c.capacity_is_maximum_not_required_count,true,'Capacity is maximum');same(c.capacity_color_independent_of_field_color,true,'Capacity and field colors independent');same(c.transitions.add_generator_to_resolved,'RESOLVED -> CONFIGURING; previous field destabilizes','Resolved addition destabilizes');
  same(g.camera,'FIXED_TOP_DOWN','Fixed top-down');same(g.position_dimensions,['x','y'],'XY placement');same(g.orientation_dimensions,3,'3D orientation');same(g.player_controlled_position_z,false,'No positional Z');same(g.orbit_camera,false,'No orbit camera');same(g.cad_navigation,false,'No CAD navigation');same(g.controls,['select','move in XY','orient/rotate'],'Simple FG controls');same(g.unrestricted_orientation_grants_legality,false,'Orientation cannot grant legality');
  same(g.zone_form,{Deck:'CARD',Hand:'CARD',Graveyard:'CARD'},'Card-to-deployed object lifecycle');same(g.partial_feedback.one_fg_forms_field,false,'One FG forms no field');same(g.partial_feedback.two_fg_may_show_compatible_relationships,true,'Two FG partial relationships');same(g.partial_feedback.presentation_only,true,'Partial feedback is presentation');same(g.partial_feedback.creates_legality,false,'Partial feedback cannot invent legality');same(g.gesture_tuning,'OPEN','Exact gestures OPEN');
  same(r.merge.composition,'C_A(m FG) + C_B(n FG) -> C_AB((m+n) FG)','Merged contents compose');same(r.merge.independent_spaces_before,2,'Merge two input spaces');same(r.merge.independent_spaces_after,1,'Merge board-width cost');same(r.merge.committed_contents_preserved,true,'Merge preserves contents');same(r.merge.reconfiguration_allowed,true,'Merged configuration can reorient');same(r.merge.count_guarantees_closure,false,'Merged count is not closure');same(r.merge.merged_capacity_ceiling,'OPEN','No invented merged capacity ceiling');same(r.merge.runtime_admission,'OPEN','Runtime admission remains OPEN');same(r.merge.example.input_counts.reduce((a,b)=>a+b,0),r.merge.example.output_count,'Merge 3 + 4 = 7');
  same(r.fusion.lookup_driven,true,'Deterministic fusion lookup');same(r.fusion.new_minigame,false,'No fusion minigame');same(r.fusion.catalog_objects,343,'Preserved fusion catalog size');same(r.emergence.automatic_on_admitted_relationship,true,'Automatic admitted emergence');same(r.emergence.separate_fg_construction,false,'No separate Emergent construction');same(r.emergence.catalog_objects,1691,'Preserved emergence catalog size');same(r.emergence.supports_remain_distinct,true,'Emergent supports remain distinct');same(r.emergence.directly_attackable,false,'Emergent not directly targetable');same(r.relation_check_timing,'OPEN','Relation timing OPEN');
  same(b.configuration_camera,g.camera,'Board/configuration camera mirror');same(b.inactive_prime_remains_in_fixed_position,true,'Inactive Prime board location');same(b.space_presentation,c.strategic_presentation,'Shared space presentation');same(b.shared_underlying_state,true,'One underlying board state');
  same(v.language,'Genesis','Genesis language direction');same(v.chain,['Genesis game semantics','Genesis VM','Python hypervisor/translation boundary','platform shell'],'Genesis runtime boundaries');same(v.game_truth,['Genesis state','QMO state'],'Authoritative runtime truth');same(v.platform_services,['graphics','input','audio','storage','network'],'Platform services');same(v.platform_returns,'input events','Platform returns events');same(v.blender_role,'offline asset generation','Blender offline');same(v.initial_target,'Windows','Windows first');same(v.later_shells,['Apple/Metal','Android'],'Later shells');same(v.rewrite_authoritative_semantics_per_platform,false,'Shared semantics across shells');same(v.implemented,false,'No runtime implementation claim');
  same(s.manifest.phase,'PREPRODUCTION','Whole-game PREPRODUCTION');same(s.manifest.mathematics_regenerated,false,'No mathematics regeneration');same(s.manifest.qmo_data_changed,false,'No imported QMO changes');same(s.manifest.gameplay_implemented,false,'No gameplay implementation');
 }catch(e){errors.push('Invalid full-migration data: '+e.message);}
 return {checks,errors};
}
export function validateFullMigrationRepository(root){
 const errors=[];let checks=0;
 const check=(ok,label)=>{checks++;if(!ok)errors.push(label);};const same=(a,b,label)=>check(isDeepStrictEqual(a,b),label);
 const file=p=>resolveRepositoryPath(root,p),bytes=p=>fs.readFileSync(file(p)),json=p=>JSON.parse(bytes(p).toString('utf8'));
 try{
  const state=loadFullMigration(root),semantic=validateFullMigrationData(state);checks+=semantic.checks;errors.push(...semantic.errors);
  const contract=loadFullMigrationContract(root);
  for(const [key,entry]of Object.entries(contract.datasets)){same(state.manifest.datasets[key],entry.path,'Canonical dataset pointer: '+key);same(projectGameDefinitionFile(root,entry.path,state[key]),entry.accepted,'Accepted full-migration dataset plus reviewed amendments: '+key);check(fs.existsSync(file(state[key].design)),'Current design home: '+key);}
  same(projectBeforeFullMigration(root,loadDesignState(root)),json('provenance/audits/full-migration-2026-09-29-before-state.json'),'Only accepted semantic amendments');
  const cards=json('data/cycles/cycle_01/card-system.json').values.cycle_01,overview=json('data/cycles/cycle_01/utilities/overview.json').values.utility_structure;
  same(cards.ordinary_cards,{field_generators:120,prime_fields:14,utilities:51,total:185},'Current 185-card structure');same(Object.values(cards.utility_domains).reduce((a,b)=>a+b,0),50,'Original fifty Utility allocation');same(cards.additional_utilities,{restore_prime:1},'Additive Utility count');same(overview.total_slots,51,'Current 51 Utilities');same(overview.additional_slots,[{count:1,definition_ref:state.manifest.datasets.restore_prime}],'Utility overview reaches actual addition');
  same(json('data/cycles/cycle_01/manifest.json').ordinary_counts,cards.ordinary_cards,'Cycle count mirror');
  const index=json('data/manifests/accepted-state.json'),map=json('data/manifests/authority-map.json');same(index.full_migration,'data/manifests/full-migration-2026-09-29.json','Accepted-state reaches full migration');same(map.full_migration,index.full_migration,'Authority map reaches full migration');
  const receipt=json(S+'/receipt.json'),archive=bytes(receipt.archive.path);
  same(receipt.archive.sha256,archiveHash,'Pinned full source identity');same(receipt.archive.bytes,archiveSize,'Pinned source size');
  const pointer=`version https://git-lfs.github.com/spec/v1\noid sha256:${archiveHash}\nsize ${archiveSize}\n`;
  let members;
  if(archive.subarray(0,80).toString().startsWith('version https://git-lfs.github.com/spec/v1'))same(archive.toString(),pointer,'Full source LFS identity');
  else{
   check(archive.length===archiveSize&&digest(archive)===archiveHash,'Hydrated full source SHA-256');
   if(digest(archive)!==archiveHash)throw Error('Full source archive was altered');
   members=readSourceZip(archive,{maxMemberBytes:256*1024*1024});
   for(const r of receipt.prior_packages){const b=members.get('RAEON_FULL_MIGRATION_2026-09-29/prior_recovery/'+r.file);check(b.length===r.bytes&&digest(b)===r.sha256,'Original nested prior package: '+r.file);}
  }
  for(const r of receipt.normalized_sources){const b=bytes(r.path);check(b.length===r.bytes&&digest(b)===r.sha256,'Copied newest source bytes: '+r.path);if(members)check(b.equals(members.get(r.member)),'Source copy matches full archive member');}
  const handoff=S+'/handoff/',delta=handoff+'current_delta/RAEON_THREAD_DELTA_2026-09-29/';
  for(const r of json(delta+'MANIFEST.json').files)check(bytes(delta+r.path).length===r.bytes&&digest(bytes(delta+r.path))===r.sha256,'Newest delta manifest: '+r.path);
  for(const r of json(handoff+'MANIFEST.json').files){if(r.path.startsWith('prior_recovery/')){const p=receipt.prior_packages.find(x=>'prior_recovery/'+x.file===r.path);check(p?.bytes===r.bytes&&p?.sha256===r.sha256,'Full manifest prior archive identity');}else check(bytes(handoff+r.path).length===r.bytes&&digest(bytes(handoff+r.path))===r.sha256,'Full handoff manifest: '+r.path);}
  const baseline=json('provenance/audits/full-migration-2026-09-29-baseline.json');same(baseline.starting_main,'dff71b9504b36b2c49496932688ba5f00c10ab10','Actual starting main');
  const originalCopies=new Set(json('provenance/sources/cycle1-originals/file-mappings.json').map(x=>x.destination));
  const families=new Set(Object.values(index.utility_families));
  for(const [p,sha]of Object.entries(baseline.sha256))if(originalCopies.has(p)||families.has(p)||p==='data/black/design.json'||p==='data/game/match.json'||p.startsWith('game/')||p.startsWith('development/checkpoints/')||(p.startsWith('provenance/')&&p!=='provenance/README.md')){
   const b=bytes(p),lfs=b.subarray(0,80).toString().startsWith('version https://git-lfs.github.com/spec/v1');
   check(lfs?b.toString().includes('\noid sha256:'+sha+'\n'):(digest(b)===sha||matchesGameDefinitionAmendment(root,p,digest(b),sha)),'Preserved source/history/original Utility/Black/runtime: '+p);
  }
 }catch(e){errors.push('Full migration validation failed: '+e.message);}
 return {checks,errors};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const r=validateFullMigrationRepository(path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..'));
 for(const e of r.errors)console.error('FAIL: '+e);
 console.log(`${r.errors.length?'FAIL':'PASS'} — ${r.checks} full-migration checks; ${r.errors.length} error(s).`);
 console.log('Scope: accepted design, source preservation and repository consistency; no runtime or theoretical mathematics claim. LFS pointers verify identity; hydrated archives verify bytes.');
 if(r.errors.length)process.exitCode=1;
}
