import fs from 'node:fs';
import {loadDesignState} from './load-design-state.mjs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';

// This checks bootstrap claims, not the external mathematics or game systems.
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const failures = [];
let checks = 0;
function check(condition, message) { checks++; if (!condition) failures.push(message); }
function read(p) { return fs.readFileSync(path.join(root, p), 'utf8'); }
function json(p) { return JSON.parse(read(p)); }
function same(actual, expected, label) { check(isDeepStrictEqual(actual, expected), label); }
function git(args) {
  const result = spawnSync('git', ['-C', root, ...args], {encoding: 'utf8', windowsHide: true});
  if (result.error) throw result.error;
  return result;
}
const rootFiles = ['README.md','PROJECT_CONSTITUTION.md','DEVELOPMENT_CONSTITUTION.md','CONTRIBUTING.md','CHANGELOG.md','.gitignore','.gitattributes'];
const groups = {
  production: ['00_concept','01_preproduction','02_prototype','03_vertical_slice','04_production','05_content_complete','06_alpha','07_beta','08_release_candidate','09_certification','10_gold','11_postlaunch'],
  development: ['modules','milestones','builds','checkpoints'],
  'development/modules': ['core-game','turn-engine','board','sandbox-domains','card-system','field-generators','qmo-engine','chirality-fabric','propagation-engine','manifold-closure','fusion','emergent-fields','transduction','prime-fields','utilities','deck-construction','collection','card-shop','black-rank','ai','multiplayer','rendering','blender-pipeline','gpu-runtime','ui-ux','persistence','platform'],
  'development/builds': ['prototype','development','nightly','alpha','beta','release-candidate'],
  design: ['game','cards','systems','progression','economy','ai','multiplayer','ui-ux'],
  mathematics: ['genesis','chirality','propagation','qmo','closure','manifolds','transduction'],
  game: ['core','state','rules','cards','board','sandbox','qmo','manifold','transduction','primes','utilities','deck','collection','shop','ai','multiplayer','rendering','ui','persistence'],
  content: ['cards','blender','meshes','materials','shaders','vfx','ui','icons','audio','reference'],
  data: ['cycles','cycles/cycle_01','cards','cards/generators','cards/primes','cards/utilities','qmo','manifolds','manifolds/base','manifolds/fusion','manifolds/emergent','transduction','closure','balance','render-specs','ai','schemas','manifests'],
  tools: ['validators','generators','qmo','blender','rendering','data','provenance'],
  tests: ['unit','integration','regression','gameplay','qmo','rendering','multiplayer','adversarial','performance'],
  platform: ['shared','windows','ipados'],
  provenance: ['decisions','sources','checkpoints','audits'],
  releases: [],
};
const boundaries = new Set(['design/cards/cycle_01']);
for (const [base, children] of Object.entries(groups)) {
  boundaries.add(base);
  for (const child of children) boundaries.add(`${base}/${child}`);
}
const extras = ['development/PIPELINE.md','production/phases.json','production/03_vertical_slice/EXIT_CRITERIA.md','design/cards/CYCLE_PRODUCTION.md','design/game/ACCEPTED_RULES.md','data/cycles/cycle_01/manifest.json','data/manifests/accepted-state.json','data/manifests/bootstrap-inventory.json','provenance/decisions/0001-repository-bootstrap.md','provenance/audits/bootstrap-inventory.md','provenance/checkpoints/0001-bootstrap.md','development/checkpoints/0001-bootstrap.md','provenance/sources/bootstrap-request.txt','provenance/sources/bootstrap-request.json','tools/validators/validate-bootstrap.mjs','tests/regression/bootstrap-validator.test.mjs'];
const required = [...rootFiles, ...[...boundaries].map(p => `${p}/README.md`), ...extras];
try {
  for (const p of required) check(fs.existsSync(path.join(root,p)) && fs.statSync(path.join(root,p)).isFile(), `Required file missing: ${p}`);
  const inventory = json('data/manifests/bootstrap-inventory.json');
  check(Array.isArray(inventory.files), 'Inventory files must be an array');
  same(inventory.file_count, inventory.files.length, 'Inventory file_count');
  same(new Set(inventory.files).size, inventory.files.length, 'Inventory contains duplicate paths');
  for (const p of required) check(inventory.files.includes(p), `Inventory omits required file: ${p}`);
  for (const p of inventory.files) {
    const valid = typeof p === 'string' && !path.isAbsolute(p) && !p.includes('\\') && !p.split('/').some(x=>['..','.git','_inbox',''].includes(x));
    check(valid, `Invalid inventory path: ${p}`);
    if (valid) check(fs.existsSync(path.join(root,p)), `Inventory file missing: ${p}`);
  }
  same([...inventory.required_boundaries].sort(), [...boundaries].sort(), 'Inventory boundary list');
  const gitRoot = git(['rev-parse','--show-toplevel']);
  check(gitRoot.status === 0 && path.resolve(gitRoot.stdout.trim()).toLowerCase() === root.toLowerCase(), 'Validator must run in its own Git repository');
  check(read('.gitignore').split(/\r?\n/).includes('/_inbox/'), 'Root /_inbox/ ignore rule missing');
  const ignored = git(['check-ignore','--no-index','_inbox/bootstrap-probe.txt','_inbox/nested/probe.txt']);
  check(ignored.status === 0 && ignored.stdout.trim().split(/\r?\n/).length === 2, '_inbox is not effectively ignored');
  const tracked = git(['ls-files','-z','--','_inbox']);
  check(tracked.status === 0 && tracked.stdout.length === 0, '_inbox content is tracked');
  // Git cannot preserve the empty inbox; new checkouts create it locally after ignore validation.
  if (ignored.status === 0) fs.mkdirSync(path.join(root,'_inbox'), {recursive:true});
  check(fs.statSync(path.join(root,'_inbox')).isDirectory(), 'Local inbox directory missing');
  const s = loadDesignState(root);
  same(s.authority,'GAME_CANON','Accepted state authority');
  same(s.production.phase,'PREPRODUCTION','Current whole-game phase must be PREPRODUCTION');
  same(s.production.vertical_slice_complete,false,'Vertical Slice cannot be complete');
  const c=s.cycle_01;
  same(c.ordinary_cards,{field_generators:120,prime_fields:30,utilities:50,total:200},'Cycle-1 card counts');
  same(c.ordinary_cards.field_generators+c.ordinary_cards.prime_fields+c.ordinary_cards.utilities,c.ordinary_cards.total,'Cycle arithmetic: 120 + 30 + 50 = 200');
  same(c.constructed_deck_size,60,'Constructed deck size');
  same(c.normal_copy_limits,{field_generator:2,utility:3},'Normal copy limits');
  same(c.prime_identity,'unique','Prime identity uniqueness');
  same(c.active_prime_positions,3,'Active Prime positions');
  same(c.catalog_status,'STRUCTURE_ACCEPTED_DETAILS_OPEN','Utility structure accepted; final details remain OPEN');
  same(c.utility_domains,{transduction:18,activation:7,sandbox_activation:6,draw_deck:7,graveyard_recovery:6,stability_protection:6},'Utility allocation');
  same(Object.values(c.utility_domains).reduce((a,b)=>a+b,0),50,'Utility arithmetic: 18 + 7 + 6 + 7 + 6 + 6 = 50');
  same(s.colors,{none:0,Red:1,Orange:2,Yellow:3,Green:4,Blue:5,Violet:6,White:7,Black:8},'Color magnitudes');
  same(s.field_generators,{maximum_rank:'White',black_allowed:false},'Black Field Generators prohibited');
  for (const [key,value] of Object.entries({permanent_start:3,permanent_minimum:3,temporary_domains_allowed:true,independent_extraction_after_commitment:false,whole_domain_merge_fusion_allowed:true,topology_basis:'participating Generator geometry, not Sandbox provenance'})) same(s.sandbox[key],value,`Preserved Sandbox invariant: ${key}`);
  same(s.local_manifold.closure_required_before_color,true,'Closure must precede color');
  same(s.local_manifold.closed_generator_count_to_color,{'3':'Red','4':'Orange','5':'Yellow','6':'Green','7':'Blue','8':'Violet'},'Local Manifold ladder');
  same(s.local_manifold.base_basis,{Red:15,Orange:13,Yellow:11,Green:9,Blue:7,Violet:5},'Base Manifold basis');
  same(Object.values(s.local_manifold.base_basis).reduce((a,b)=>a+b,0),60,'Base arithmetic: 15 + 13 + 11 + 9 + 7 + 5 = 60');
  same(s.local_manifold.base_total,60,'Base total');
  same(s.local_manifold.basis_is_complete_recursive_closure,false,'Basis must not claim complete recursive closure');
  same(s.qmo_inventory,{status:'SOURCE_IMPORT_REQUIRED',base_local_manifolds:60,fusion_derived_local_manifolds:343,emergent_fields:1691,total_render_relevant:2094,objects_imported:false},'External QMO inventory claim');
  same(s.qmo_inventory.base_local_manifolds+s.qmo_inventory.fusion_derived_local_manifolds+s.qmo_inventory.emergent_fields,2094,'QMO arithmetic: 60 + 343 + 1691 = 2094');
  same(s.mathematical_api,{outcomes:['VALID','TERMINATES','NOT_APPLICABLE','OPEN','UNTESTED'],missing_data_is_termination:false},'Mathematical API outcomes and missing-data distinction');
  same(s.black.rank,8,'Black rank');
  same(s.black.field_generators_exist,false,'Black Generator absence');
  same(s.black.ordinary_deck_legal,true,'Black ordinary deck legality');
  same(s.black.prime_identities,3,'Exactly three Black Prime identities');
  same(s.black.utilities_exist,true,'Black Utilities exist');
  same(s.black.all_black_deck,{primes:3,utilities:57,total:60},'All-Black deck composition');
  same(s.black.all_black_deck.primes+s.black.all_black_deck.utilities,60,'All-Black arithmetic: 3 + 57 = 60');
  same(s.black.legal_all_black_unlocks_hidden_mode,true,'Black Mode unlock');
  same(s.black.fourth_prime,{kind:'emergent/supported Prime',deck_card:false,availability:'true while all three supporting Black Primes remain alive; false if any dies',detailed_behavior:'OPEN'},'Fourth Prime support/OPEN behavior');
  same(s.platforms,{priority:'WINDOWS DESKTOP',secondary:'iPad / iPadOS'},'Platform priorities');
  check(s.source_import_required.length >= 10 && s.open_items.length >= 10,'Source import and OPEN lists must remain explicit');
  const phases=json('production/phases.json');
  same(phases.current_phase,'PREPRODUCTION','Phase registry current phase');
  same(phases.phases.map(p=>p.directory),groups.production,'Phase registry directories');
  for (const p of phases.phases) {
    same(p.complete,false,`Phase must not be complete: ${p.directory}`);
    same(p.status,p.directory==='01_preproduction'?'ACTIVE':p.directory==='00_concept'?'UNTESTED':'OPEN',`Phase status: ${p.directory}`);
    const doc=read(`production/${p.directory}/README.md`);
    for (const h of ['Purpose','Entry criteria','Required deliverables','Exit criteria','Prohibited premature claims','Current status']) check(doc.includes(`## ${h}`),`Phase heading ${h}: ${p.directory}`);
    check(doc.includes('NOT COMPLETE'),`Phase non-completion declaration: ${p.directory}`);
  }
  const slice=read('production/03_vertical_slice/EXIT_CRITERIA.md');
  same((slice.match(/^- \[ \]/gm)||[]).length,16,'Sixteen unchecked slice criteria required');
  check(!/^- \[[xX]\]/m.test(slice),'Slice criteria must not be marked complete');
  const gateNames=['Canon','Design','Mathematics','Rules','State Model','Interfaces','Algorithms','Visualization','Interaction','Data & Schemas','Implementation','Testing','Integration','Performance','Provenance','Release'];
  for (const name of groups['development/modules']) {
    const doc=read(`development/modules/${name}/README.md`);
    for(const h of ['Purpose','Current status','Authority','Inputs','Outputs','Dependencies','Development gates','OPEN questions','Validation requirements']) check(doc.includes(`## ${h}`),`Module heading ${h}: ${name}`);
    check(doc.includes(name === 'utilities' ? 'DESIGN — DESIGN STRUCTURE ACCEPTED' : 'OPEN — intentionally unimplemented'),`Module status mismatch: ${name}`);
    for(const [i,g] of gateNames.entries()) check(doc.includes(`| ${String(i).padStart(2,'0')} ${g} | OPEN |`),`Module gate ${i}: ${name}`);
  }
  const cycle=json('data/cycles/cycle_01/manifest.json');
  same(cycle.production_pipeline,['SEED','GENERATE','FORMALIZE','BALANCE','RENDER','INTEGRATE','TEST','RELEASE'],'Cycle pipeline');
  same(cycle.card_definitions_imported,false,'No fabricated card catalog');
  const source=json('provenance/sources/bootstrap-request.json');
  same(createHash('sha256').update(fs.readFileSync(path.join(root,'provenance/sources/bootstrap-request.txt'))).digest('hex'),source.sha256,'Bootstrap source integrity');
  // Check local Markdown links; this does not fetch any external repository.
  for(const p of inventory.files.filter(p=>p.endsWith('.md'))) {
    for(const match of read(p).matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
      const dest=match[1].split('#')[0];
      if(!dest || /^[a-z]+:/i.test(dest)) continue;
      check(fs.existsSync(path.resolve(root,path.dirname(p),dest)),`Broken local link in ${p}: ${dest}`);
    }
  }
} catch (error) {
  failures.push(`Validation could not complete: ${error.message}`);
}
console.log('Scope: repository/bootstrap invariants only.');
console.log('Does NOT validate: Genesis mathematics; Chirality mathematics; QMO closure correctness; gameplay balance; Blender geometry; GPU rendering; multiplayer correctness; AI correctness.');
if(failures.length) {
  for(const failure of failures) console.error(`FAIL: ${failure}`);
  console.error(`FAIL — ${failures.length} failure(s), ${checks} checks evaluated.`);
  process.exitCode=1;
} else console.log(`PASS — ${checks} bootstrap checks; whole-game phase PREPRODUCTION; no phase complete.`);
