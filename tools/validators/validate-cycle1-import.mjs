import fs from 'node:fs';
import {matchesGameDefinitionAmendment} from './game-definition-contract.mjs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';
import {DatabaseSync} from 'node:sqlite';
import {resolveRepositoryPath} from './load-design-state.mjs';
import {remainingCycle1Sources} from './cycle1-status.mjs';
import {readSourceZip} from './source-zip.mjs';

const S='provenance/sources/cycle1-originals';
const originalHashes={
 'RAEON_CLOSED_PLAYFIELD_API_v1_0.zip':'18282091bffbf8ae51a600f23a359e0a0d13f3109287db6e80fbabf3253d266e',
 'RAEON_COMPLETE_QMO_ATLAS_CYCLE1.zip':'abc2b1e18f58b77184483923b0bbccc11886462f1cd6d7bdc5b73b044792ebcd',
 'RAEON_CYCLE_GENERATION_CONSTITUTION_v1_0.zip':'5e39897b70a52e0cdf5a74f80cece2cc6eae69cb880c0f50f06aebd0cd63cc9c',
 'RAEON_LIVE_MODEL_v0_1_2026-09-13.zip':'ba5758c7ab5fc9a6e1f9c634f8a0ac82432344bbf7234b601093f721978d3edf'
};
const counts={field_generators:120,base:60,fusion:343,emergent:1691,atlas:2094,pairs:1770,compatibility:2482,render_specs:60};
const hash=b=>createHash('sha256').update(b).digest('hex');
const tally=(rows,key)=>rows.reduce((a,r)=>(a[r[key]]=(a[r[key]]??0)+1,a),{});
const sorted=x=>[...x].sort();
const key=(a,b)=>[a,b].sort().join('__');

export function validateCycle1Import(root) {
 const errors=[];let checks=0;const check=(ok,label)=>{checks++;if(!ok)errors.push(label);};
 const same=(a,b,label)=>check(isDeepStrictEqual(a,b),label);
 const file=p=>resolveRepositoryPath(root,p),bytes=p=>fs.readFileSync(file(p));
 const json=p=>JSON.parse(bytes(p).toString('utf8'));
 const unique=(rows,field,label)=>check(new Set(rows.map(x=>x[field])).size===rows.length,'Unique '+label);
 try {
  const archives=new Map();
  function visit(name,b) {const entries=readSourceZip(b);archives.set(name,entries);for(const [p,v] of entries)if(p.endsWith('.zip'))visit(name+'!/'+p,v);}
  for(const [name,sha]of Object.entries(originalHashes)){
   const b=bytes(S+'/authoritative_sources/'+name);
   check(hash(b)===sha,'Original archive SHA-256: '+name);
   // Never process an archive that does not match the supplied original identity.
   if(hash(b)!==sha)throw Error('Changed source archive: '+name);
   visit(name,b);
  }
  const receipt=json(S+'/receipt.json');
  same(Object.fromEntries(receipt.archives.map(x=>[x.file,x.sha256])),originalHashes,'Receipt pins all four originals');
  for(const r of receipt.archives)check(bytes(r.path).length===r.bytes&&hash(bytes(r.path))===r.sha256,'Receipt source bytes: '+r.file);
  for(const r of json(S+'/MANIFEST.json').files)check(bytes(S+'/'+r.path).length===r.bytes&&hash(bytes(S+'/'+r.path))===r.sha256,'Handoff manifest: '+r.path);
  const inventory=json(S+'/source-inventory.json');
  same(inventory.length,408,'Full source member inventory');
  same([...archives.values()].reduce((n,m)=>n+m.size,0),inventory.length,'No omitted nested source members');
  unique(inventory.map(x=>({id:x.archive+'!/'+x.path})),'id','source member paths');
  for(const r of inventory){const b=archives.get(r.archive)?.get(r.path);check(b?.length===r.bytes&&hash(b)===r.sha256,'Source member integrity: '+r.path);if(r.path.endsWith('.json'))JSON.parse(b.toString('utf8'));}
  for(const r of json(S+'/internal-manifest-results.json')){
   const entries=archives.get(r.archive),b=entries.get(r.manifest),prefix=path.posix.dirname(r.manifest).replace(/\/provenance$/,'')+'/';
   let rows;
   if(r.manifest.endsWith('.txt'))rows=b.toString().trim().split(/\r?\n/).map(line=>{const m=line.match(/^([a-f0-9]{64})\s+\*?(.+)$/);if(!m)throw Error('Malformed source hash list');return{sha256:m[1],path:m[2]};});
   else {const value=JSON.parse(b.toString());rows=Array.isArray(value)?value:value.files;}
   const failed=rows.filter(x=>{const v=entries.get(prefix+x.path);return !v||hash(v)!==x.sha256||(x.bytes!==undefined&&v.length!==x.bytes);}).map(x=>x.path);
   same(rows.length,r.checks,'Internal manifest coverage: '+r.archive+' '+r.manifest);
   same(sorted(failed),sorted(r.failures),'Internal manifest results: '+r.archive+' '+r.manifest);
   if(/LOCKED_v1_0|CONSTITUTION_v1_0\/MANIFEST|MANIFEST_SHA256/.test(r.manifest))same(failed,[],'Latest source manifest matches: '+r.manifest);
  }
  const mappings=json(S+'/file-mappings.json');unique(mappings,'destination','normalized destinations');
  for(const m of mappings){
   const b=bytes(m.destination);check(hash(b)===m.sha256,'Normalized file SHA-256: '+m.destination);
   const original=m.archive==='handoff'?bytes(S+'/'+m.member):archives.get(m.archive)?.get(m.member);
   if(m.mapping==='byte-identical')check(b.equals(original),'Normalized bytes equal original ZIP member: '+m.destination);
   else same(JSON.parse(b),JSON.parse(original).filter(x=>x.type===m.type),'Filtered records unchanged: '+m.destination);
  }
  const m=json('data/manifests/cycle1-source-import.json'),data=Object.fromEntries(Object.entries(m.datasets).filter(([k])=>k!=='database').map(([k,p])=>[k,json(p)]));
  same(m.counts,counts,'Import manifest counts');same(m.remaining_source_import_required,remainingCycle1Sources,'Remaining absent sources');
  same(json('data/manifests/accepted-state.json').source_import_required,remainingCycle1Sources,'Current source requirements');
  check(m.no_regeneration===true&&m.runtime_implemented===false&&m.production_phase==='PREPRODUCTION','Import scope');
  const {field_generators:fg,base,fusion,emergent,derived,atlas,pairs,compatibility:compat,summary,render_catalog:catalog}=data;
  for(const k of ['field_generators','base','fusion','emergent','pairs','compatibility'])same(data[k].length,counts[k],'Exact '+k+' count');
  same(derived.length,2034,'Exact derived count');same(catalog.length,60,'Exact RenderSpec count');
  same(fusion,derived.filter(x=>x.type==='DerivedLocalManifoldQMO'),'Fusion is exact source subset');
  same(emergent,derived.filter(x=>x.type==='EmergentFieldQMO'),'Emergent is exact source subset');
  unique(fg,'card_id','FG IDs');unique(base,'manifold_id','base IDs');unique([...fg,...base,...derived],'id','all QMO IDs');
  same(sorted(fg.map(x=>x.card_id)),Array.from({length:120},(_,i)=>'FG-'+String(i+1).padStart(3,'0')),'FG-001 through FG-120');
  same(tally(base,'native_color'),{RED:15,ORANGE:13,YELLOW:11,GREEN:9,BLUE:7,VIOLET:5},'Base color distribution');
  const fgMap=new Map(fg.map(x=>[x.card_id,x])),baseMap=new Map(base.map(x=>[x.manifold_id,x]));
  const qmos=new Map([...fg,...base,...derived].map(x=>[x.id,x]));
  const compatibilitySet=new Set(compat.map(x=>key(x.a,x.b)));
  same(compatibilitySet.size,2482,'Unique compatibility pairs');
  for(const edge of compat){
   check(fgMap.has(edge.a)&&fgMap.has(edge.b)&&edge.a!==edge.b,'Compatibility FG references');
   for(const match of edge.matches)check(Object.hasOwn(fgMap.get(edge.a).faces,match.a_face)&&Object.hasOwn(fgMap.get(edge.b).faces,match.b_face),'Compatibility face references');
  }
  for(const g of fg){
   unique(g.compatible_generators.map(id=>({id})),'id','FG compatibility memberships');
   for(const other of g.compatible_generators)check(fgMap.has(other)&&compatibilitySet.has(key(g.card_id,other))&&fgMap.get(other).compatible_generators.includes(g.card_id),'Symmetric FG compatibility');
   same(sorted(g.compatible_generators),sorted(compat.filter(x=>x.a===g.card_id||x.b===g.card_id).map(x=>x.a===g.card_id?x.b:x.a)),'Complete FG compatibility index');
   same(sorted(g.manifold_memberships),sorted(base.filter(x=>x.generators.includes(g.card_id)).map(x=>x.manifold_id)),'FG base membership references');
  }
  for(const q of [...base,...derived]){
   for(const id of q.generators??[])check(fgMap.has(id),'Object FG reference: '+q.id+' '+id);
   if(q.generators){same(q.generator_count,q.generators.length,'Generator count: '+q.id);unique(q.generators.map(id=>({id})),'id','object Generators');}
   for(const id of q.support??[])check(baseMap.has(id),'Support manifold resolves: '+q.id);
   for(const edge of q.cross_interface_edges??[])check(edge.length===2&&edge.every(id=>fgMap.has(id))&&compatibilitySet.has(key(...edge)),'Emergent cross-interface reference');
  }
  unique(pairs,'pair_key','pair relations');
  same(sorted(pairs.map(x=>x.pair_key)),sorted(base.flatMap((a,i)=>base.slice(i+1).map(b=>key(a.manifold_id,b.manifold_id)))),'Complete 60-choose-2 pair space');
  for(const p of pairs){
   check(baseMap.has(p.a_manifold)&&baseMap.has(p.b_manifold),'Pair base references');same(p.pair_key,key(p.a_manifold,p.b_manifold),'Canonical pair identity');
   for(const id of p.shared_generators)check(fgMap.has(id)&&baseMap.get(p.a_manifold).generators.includes(id)&&baseMap.get(p.b_manifold).generators.includes(id),'Shared FG reference');
   for(const edge of p.cross_edges)check(edge.length===2&&edge.every(id=>fgMap.has(id))&&compatibilitySet.has(key(...edge)),'Pair cross-edge reference');
   for(const [status,address,color,type]of [['fusion_status','fusion_result_qmo','fusion_result_color','DerivedLocalManifoldQMO'],['emergent_status','emergent_qmo','emergent_color','EmergentFieldQMO']]){
    check(['VALID','TERMINATES','NOT_APPLICABLE','OPEN','UNTESTED'].includes(p[status]),'Explicit relation vocabulary');
    if(p[status]==='VALID') {const q=qmos.get(p[address]);check(q?.type===type,'Pair result QMO resolves');if(q){same(sorted(q.support),sorted([p.a_manifold,p.b_manifold]),'Pair result support');same(q.native_color,p[color],'Pair result color');}}
    else same(p[address],null,'Non-VALID result not fabricated');
   }
  }
  same(tally(pairs,'fusion_status'),{VALID:343,TERMINATES:825,NOT_APPLICABLE:602},'Fusion outcome totals');
  same(tally(pairs,'emergent_status'),{VALID:1691,TERMINATES:79},'Emergent outcome totals');
  same(summary.fusion_status_counts,tally(pairs,'fusion_status'),'Fusion source summary');same(summary.emergent_status_counts,tally(pairs,'emergent_status'),'Emergent source summary');
  same(summary.fusion_color_counts,tally(fusion,'native_color'),'Fusion source colors');same(summary.emergent_color_counts,tally(emergent,'native_color'),'Emergent source colors');
  same(summary.pair_space,pairs.length,'Source pair-space summary');same(summary.derived_qmos,derived.length,'Source derived summary');
  const redYellow=pairs.filter(p=>sorted([baseMap.get(p.a_manifold).native_color,baseMap.get(p.b_manifold).native_color]).join(',')==='RED,YELLOW');
  same(redYellow.length,summary.red_yellow_pairs,'Red/Yellow pair coverage');
  for(const [status,name]of [['VALID','valid'],['TERMINATES','terminates'],['NOT_APPLICABLE','not_applicable']])same(redYellow.filter(x=>x.fusion_status===status).length,summary['red_yellow_fusion_'+name],'Red/Yellow '+status);
  same(atlas.counts,{base_local_manifolds:60,fusion_derived_local_manifolds:343,emergent_fields:1691,total:2094},'Atlas declared counts');
  unique([...atlas.base,...atlas.fusion,...atlas.emergent],'qmo','atlas QMO IDs');
  for(const [rows,source]of [[atlas.base,base],[atlas.fusion,fusion],[atlas.emergent,emergent]]){
   same(sorted(rows.map(x=>x.qmo)),sorted(source.map(x=>x.id)),'Atlas source object coverage');
   for(const row of rows){const q=qmos.get(row.qmo);same(row.color,q.native_color,'Atlas color');if(row.generators)same(row.generators,q.generators,'Atlas Generators');if(row.support)same(row.support,q.support,'Atlas supports');if(row.cross_interface_edges)same(row.cross_interface_edges,q.cross_interface_edges,'Atlas cross interfaces');if(row.coupling_score!==undefined)same(row.coupling_score,q.coupling_score,'Atlas coupling score');}
  }
  const db=new DatabaseSync(file(m.datasets.database),{readOnly:true});
  try {
   same(db.prepare('PRAGMA integrity_check').get().integrity_check,'ok','SQLite integrity');
   const rows=t=>db.prepare('SELECT * FROM '+t).all();
   for(const [t,n]of Object.entries({qmos:181,edges:11550,generator_cards:120,manifold_qmos:60,manifold_pair_relations:1770,derived_qmos:2034}))same(rows(t).length,n,'SQLite '+t+' rows');
   const all=rows('qmos'),allAddresses=new Set([...all,...rows('derived_qmos')].map(x=>x.address));
   for(const r of [...all,...rows('derived_qmos')]){const def=JSON.parse(r.definition_json);if(qmos.has(r.address))same(def,qmos.get(r.address),'SQLite exact definition: '+r.address);else check(r.address==='@qmo/raeon/cycle1/closed_fractal_seed','Only extra QMO is source seed');}
   for(const r of rows('edges')){check(allAddresses.has(r.src)&&allAddresses.has(r.dst),'SQLite edge QMO references');JSON.parse(r.metadata_json);}
   const pairMap=new Map(pairs.map(x=>[x.pair_key,x]));
   for(const r of rows('manifold_pair_relations')){const d=Object.fromEntries(Object.entries(r).map(([k,v])=>k.endsWith('_json')?[k.slice(0,-5),JSON.parse(v)]:[k,v]));same(d,pairMap.get(r.pair_key),'SQLite exact pair: '+r.pair_key);}
   for(const r of rows('generator_cards')){const q=fgMap.get(r.card_id);check(q?.id===r.address,'SQLite FG identity');for(const k of ['rotation_class','chirality_parity','fractal_address','resolution_depth','bandwidth_degree'])same(r[k],q[k],'SQLite FG '+k);same(JSON.parse(r.occupancy),q.occupancy,'SQLite occupancy');same(JSON.parse(r.void_sites),q.void,'SQLite void');}
   for(const r of rows('manifold_qmos')){const q=baseMap.get(r.manifold_id);check(q?.id===r.address,'SQLite base identity');same(JSON.parse(r.generators_json),q.generators,'SQLite base Generators');same(r.native_color,q.native_color,'SQLite base color');}
  }finally{db.close();}
  same(sorted(catalog.map(x=>x.manifold_id)),sorted(base.map(x=>x.manifold_id)),'Render catalog base coverage');
  for(const row of catalog){
   const p='data/render_specs/cycle_01/'+row.manifold_id+'.json',raw=bytes(p).toString();
   const spec=JSON.parse(raw,(k,v,context)=>k==='deterministic_seed'?BigInt(context.source):v),q=baseMap.get(row.manifold_id);
   same(row.render_spec,'data/render_specs/'+row.manifold_id+'.json','Source render path retained');
   check(spec.qmo_address===q.id&&row.qmo_address===q.id&&spec.manifold_id===q.manifold_id,'Render QMO resolves');
   same(spec.generators,q.generators,'Render Generators');same(spec.anchors.map(x=>x.generator),q.generators,'Render anchors');
   check(typeof spec.deterministic_seed==='bigint','Exact integer render seed');
   for(const edge of spec.topological_edges)check(edge.length===2&&edge.every(i=>Number.isInteger(i)&&i>=0&&i<q.generators.length),'Render topology indices');
   for(const edge of spec.spline_edges)check([edge.a,edge.b].every(i=>Number.isInteger(i)&&i>=0&&i<q.generators.length),'Render spline indices');
  }
  const before=json('provenance/audits/cycle1-source-import-baseline.json');
  same(before.starting_main,'2e81478055483f1b86abff278b3cbc9109e61c9d','Starting main provenance');
  for(const [p,sha]of Object.entries(before.sha256))if((p.startsWith('provenance/')&&p!=='provenance/README.md')||p.startsWith('development/checkpoints/')||p.startsWith('game/'))check(hash(bytes(p))===sha||matchesGameDefinitionAmendment(root,p,hash(bytes(p)),sha),'Preserved previous history/runtime: '+p);
  check(fs.existsSync(file(m.constitution)),'Readable Constitution exists');
  for(const p of json('data/manifests/current-files.json').files.filter(p=>p.endsWith('.json')))JSON.parse(bytes(p).toString());
 }catch(e){errors.push('Cycle-1 import validation failed: '+e.message);}
 return {checks,errors};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const r=validateCycle1Import(path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..'));
 for(const e of r.errors)console.error('FAIL: '+e);
 console.log(`${r.errors.length?'FAIL':'PASS'} — ${r.checks} Cycle-1 source-integrity checks; ${r.errors.length} error(s).`);
 console.log('Scope: exact original sources, catalog consistency and references; not theoretical proof, game balance or runtime implementation.');
 if(r.errors.length)process.exitCode=1;
}
