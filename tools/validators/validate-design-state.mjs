import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {isDeepStrictEqual} from 'node:util';
import {createHash} from 'node:crypto';

// Validates the recorded design, never executes card effects or QMO mathematics.
export function validateDesignState(s) {
  const errors=[];
  let checks=0;
  const check=(ok,label)=>{checks++;if(!ok)errors.push(label);};
  const same=(a,b,label)=>check(isDeepStrictEqual(a,b),label);
  const ordinary=['Red','Orange','Yellow','Green','Blue','Violet','White'];
  const low=ordinary.slice(0,6);
  try {
    same(s.schema_version,2,'Accepted-state schema version');
    same(s.current_design_checkpoint,'0002','Current design checkpoint');
    same(s.production.phase,'PREPRODUCTION','Whole-game phase');
    same(s.governing_law,{statement:'THE MATHEMATICS IS THE PERMISSION SYSTEM.',qmo_determines_mathematical_legality:true,utilities_override_closure:false,rendering_determines_legality:false},'Mathematics permission rule');
    same(s.cycle_01.catalog_status,'STRUCTURE_ACCEPTED_DETAILS_OPEN','Catalog structural status');
    same(s.cycle_01.utility_domains,{transduction:18,activation:7,sandbox_activation:6,draw_deck:7,graveyard_recovery:6,stability_protection:6},'Utility domain allocation');
    same(s.cycle_01.normal_copy_limits,{field_generator:2,utility:3},'Identity copy limits');
    same(s.cycle_01.copy_rule_scope,'card identity','Copy rule scope');
    same(s.cycle_01.additional_color_uniqueness_rule,false,'No color uniqueness rule');
    same(s.color_interpretation,{zero:'no active color / zero charge',direct_effects:'literal numerical magnitude',non_color_utilities:'may express approximate rank / rarity / strategic power',rank_always_equals_resource_cost:false},'Charge versus Utility rank');
    same(s.sandbox.permanent_universal,true,'Permanent Sandboxes universal');
    same(s.sandbox.permanent_uses_temporary_colored_capacity,false,'Permanent Sandbox capacity exemption');
    same(s.sandbox.temporary_capacity,{Red:3,Orange:4,Yellow:5,Green:6,Blue:7,Violet:8},'Temporary Sandbox capacities');
    for(const rank of low) same(s.sandbox.temporary_capacity[rank],s.colors[rank]+2,`Capacity = charge + 2: ${rank}`);
    same(s.sandbox.capacity_guarantees_closure,false,'Capacity cannot guarantee closure');
    same(s.sandbox.over_capacity_commitment_allowed,false,'Over-capacity commitment prohibited');
    same(s.sandbox.temporary_destruction_expiry,'OPEN','Temporary expiry remains OPEN');
    same(s.emergent_fields,{directly_attackable:false,directly_destroyable:false,independently_targetable:false,required_support_loss:'inaccessible / gone according to support relation',amplification_preserves_support_dependency:true},'Emergent support and targeting');
    const u=s.utility_structure,f=u.families;
    same(u.authority,'GAME_CANON','Utility structure authority');
    same(u.status,'DESIGN STRUCTURE ACCEPTED','Utility structure accepted');
    same(u.module_status,'DESIGN','No premature Utility FORMALIZED/GOLD');
    same(u.total_slots,50,'Fifty structural slots');
    same(u.final_card_catalog,false,'No final card catalog claim');
    same(u.final_ids,'OPEN','No fabricated final IDs');
    same(u.remaining_work,['Final names','Final flavor','Final IDs','Exact wording','Unresolved ranks','Exact targeting','Exact timing','Exact duration','Balance testing','Implementation','Integration','Gameplay testing','Performance where applicable','Final release validation'],'Unfinished work retained');
    same(Object.keys(f).sort(),Object.keys(s.cycle_01.utility_domains).sort(),'Only six accepted Utility families');
    for(const [name,count] of Object.entries(s.cycle_01.utility_domains))same(f[name].count,count,`Family count: ${name}`);
    same(f.transduction.restore,low.map((rank,i)=>({rank,charge_delta:i+1})),'Dedicated Restore ladder');
    same(f.transduction.degrade,low.map((rank,i)=>({rank,charge_delta:-(i+1)})),'Dedicated Degrade ladder');
    same(f.transduction.universal,ordinary.slice(1).map((rank,i)=>({rank,magnitude:i+1,choices:['RESTORE','DEGRADE'],choice_time:'resolution'})),'Universal rank/magnitude ladder and choice');
    same(f.transduction.red_universal,false,'No Red Universal');
    same(f.transduction.dedicated_white_restore_degrade,false,'No dedicated White Transduction');
    same(f.activation.ranks,ordinary,'Seven Activation ranks');
    same(f.activation.ordinary_use,{from:'READY',to:'USED'},'Ordinary use transition');
    same(f.activation.normal_refresh,{from:'USED',to:'READY',timing:'OPEN'},'Normal refresh transition');
    same(f.activation.effect,{from:'USED',to:'READY',timing:'early',eligibility:'already-earned legal resource/object; exact eligibility OPEN'},'Activation early availability');
    same(f.activation.creates_color,false,'Activation creates no color');
    same(f.activation.creates_qmo_legality,false,'Activation creates no legality');
    same(f.activation.per_rank_behavior,'OPEN','Activation details remain OPEN');
    same(f.sandbox_activation,{count:6,ranks:low,capacity_ref:'sandbox.temporary_capacity',permanent_exempt:true,identity_copy_limit_ref:'cycle_01.normal_copy_limits.utility',color_uniqueness_rule:false,destruction_expiry:'OPEN'},'Sandbox Activation structure');
    const expectedDraw=[
      ['Draw 1','Orange',{operation:'draw',count:1}],['Draw 2','Green',{operation:'draw',count:2}],['Draw 3','Violet',{operation:'draw',count:3}],
      ['Survey','Yellow',{operation:'survey',look_top:3,return_to:'deck top',order:'any',direct_card_advantage:0}],
      ['Selection','Green',{operation:'select',look_top:3,take_to_hand:1,remainder_to:'deck bottom',remainder_order:'OPEN'}],
      ['Exchange','Blue',{operation:'exchange',discard_from:'hand',discard_count:'any number',draw_count:'same number discarded',net_hand_count_change:0,interacts_with_recovery:true}],
      ['Deep Survey','White',{operation:'deep_survey',look_top:7,take_to_hand:1,remainder:'shuffle back into deck',unrestricted_exact_card_tutor:false}]
    ];
    const expectedRecovery=[
      ['Recover 1 Field Generator','Yellow',{card_type:'Field Generator',count:1,destination:'hand'}],
      ['Recover 2 Field Generators','Blue',{card_type:'Field Generator',count:2,destination:'hand'}],
      ['Recover 3 Field Generators','White',{card_type:'Field Generator',count:3,destination:'hand'}],
      ['Recover 1 Utility','Green',{card_type:'Utility',count:1,destination:'hand'}],
      ['Recover 1 non-Prime','Blue',{card_type:'non-Prime',count:1,destination:'hand'}],
      ['Recover up to 3 to deck','Violet',{card_type:'non-Prime',maximum_count:3,destination:'deck top',order:'any chosen'}]
    ];
    for(const [name,expected] of [['draw_deck',expectedDraw],['graveyard_recovery',expectedRecovery]]) {
      same(f[name].slots.length,expected.length,`${name} slot count`);
      expected.forEach(([concept,rank,effect],i)=>same(f[name].slots[i],{concept,working_rank:{value:rank,authority:'PROVISIONAL',acceptance:'accepted current working design'},effect},`${name} slot ${i+1} working rank/effect`));
    }
    same(f.draw_deck.simple_rank_ladder,false,'Draw family is not a rank ladder');
    same(f.draw_deck.raw_draw_maximum,3,'Raw draw capped at 3');
    same(f.draw_deck.graveyard_retrieval,false,'Draw cannot retrieve Graveyard');
    same(f.draw_deck.hand_size_maximum,'OPEN','Hand size remains OPEN');
    same(f.draw_deck.overflow_behavior,'OPEN','Overflow remains OPEN');
    same(f.graveyard_recovery.source,'Graveyard','Recovery source');
    same(f.graveyard_recovery.prime_recovery_allowed,false,'No ordinary Prime recovery');
    same(f.graveyard_recovery.automatically_reconstructs_manifold,false,'Recovery cannot reconstruct manifolds');
    same(f.graveyard_recovery.recovered_generators_require_normal_use_and_legal_topology,true,'Recovered Generators need normal topology construction');
    same(f.stability_protection.restores_lost_color,false,'Protection is distinct from Restoration');
    const stability=f.stability_protection.slots;
    same(stability.map(x=>x.concept),['Color Guard','Prime Guard','Manifold Guard','Shield Lock','Structural Anchor','Emergent Amplification'],'Six Stability concepts; no Coupling Stabilizer');
    same(f.stability_protection.excluded_concepts,['Coupling Stabilizer'],'Rejected Coupling Stabilizer');
    same(stability[0],{concept:'Color Guard',rank:'OPEN',effect:{operation:'absorb_next_degradation',amount:'OPEN'}},'Color Guard effect/OPEN magnitude');
    same(stability[1],{concept:'Prime Guard',rank:'OPEN',duration:'OPEN',timing:'OPEN',effect:{operation:'protect_next_eligible_degradation',object:'one Prime'}},'Prime Guard effect/OPEN details');
    same(stability[2],{concept:'Manifold Guard',rank:'OPEN',duration:'OPEN',timing:'OPEN',effect:{operation:'protect_next_eligible_degradation',object:'one Local Manifold'}},'Manifold Guard effect/OPEN details');
    same(stability[3],{concept:'Shield Lock',rank:'OPEN',minimum_working_rank:'Blue',duration:'OPEN',effect:{operation:'temporarily_prevent_degradation',object:'existing Prime shield'}},'Shield Lock Blue floor/OPEN final rank');
    same(stability[4],{concept:'Structural Anchor',rank:'OPEN',effect:{operation:'survive_next_otherwise_lethal_degradation',object:'one already-valid Local Manifold',survival_color:'Red',survival_charge:1,bypasses_closure:false}},'Structural Anchor lethal-to-Red');
    same(stability[5],{concept:'Emergent Amplification',rank:'OPEN',effect:{operation:'increase_active_emergent_charge',charge_delta:1,maximum_color:'Violet',maximum_charge:6,creates_field:false,changes_support_relation:false,makes_targetable:false,preserves_after_support_loss:false}},'Amplification cap/support restrictions');
    const counts=[f.transduction.restore.length+f.transduction.degrade.length+f.transduction.universal.length,f.activation.ranks.length,f.sandbox_activation.ranks.length,f.draw_deck.slots.length,f.graveyard_recovery.slots.length,stability.length];
    same(counts,[18,7,6,7,6,6],'Actual structural slot counts');
    same(counts.reduce((a,b)=>a+b,0),50,'All fifty slots accounted for');
    same(s.black.fourth_prime,{kind:'emergent/supported Prime',deck_card:false,availability:'true while all three supporting Black Primes remain alive; false if any dies',detailed_behavior:'OPEN'},'Fourth Prime support rule');
    same(s.long_term_direction.authority,'PROVISIONAL','Economy direction authority');
    for(const key of ['long_term_collection','earn_progression_and_credits_through_play','future_cycles_possible','duplicates_have_long_term_value_including_black_crafting'])same(s.long_term_direction[key],true,`Collection direction: ${key}`);
    for(const key of ['purchase_of_gameplay_credits_required','player_to_player_credit_wagering','monetization_implemented'])same(s.long_term_direction[key],false,`Economy boundary: ${key}`);
    same(s.long_term_direction.open_details,['Crafting recipes','Credit values','Pack probabilities','Economy rates','Release pricing','Exact PvP rewards'],'Economy details remain OPEN');
    same(s.long_term_direction.pvp_rewards,'may grant game-generated progression/credits; exact rewards OPEN','PvP rewards direction');
    same(s.product_intent.authority,'PROVISIONAL','Product intent authority');
    same(s.product_intent.exact_match_duration,'OPEN','No invented match duration');
    same(s.product_intent.depth_sources,['deck construction','Field Generator topology','hidden mathematical closure relationships','Sandbox management','color transduction','Prime management','fusion','emergent fields'],'Supplied depth sources');
    same(s.qmo_inventory.status,'SOURCE_IMPORT_REQUIRED','Missing QMO artifacts remain missing');
    same(s.qmo_inventory.objects_imported,false,'No fabricated QMO import');
  } catch(error) {errors.push(`Invalid design data: ${error.message}`);}
  return {errors,checks};
}

export function validateDesignRepository(root) {
  let checks=0;const errors=[];
  const check=(ok,label)=>{checks++;if(!ok)errors.push(label);};
  const read=p=>fs.readFileSync(path.join(root,p),'utf8');
  try {
    const result=validateDesignState(JSON.parse(read('data/manifests/accepted-state.json')));
    checks+=result.checks;errors.push(...result.errors);
    const source=JSON.parse(read('provenance/sources/current-state-recovery-0002.json'));
    const hash=p=>createHash('sha256').update(fs.readFileSync(path.join(root,p))).digest('hex');
    check(hash('provenance/sources/current-state-recovery-0002.txt')===source.sha256,'Recovery source integrity');
    const inventory=JSON.parse(read('data/manifests/design-checkpoint-0002.json'));
    check(inventory.file_count===inventory.files.length,'Current inventory count');
    check(new Set(inventory.files).size===inventory.files.length,'Current inventory duplicates');
    const baseline=JSON.parse(read('data/manifests/bootstrap-inventory.json'));
    for(const p of baseline.files)check(inventory.files.includes(p),`Preserved bootstrap file: ${p}`);
    const required=['design/cards/cycle_01/UTILITIES.md','provenance/sources/current-state-recovery-0002.txt','provenance/sources/current-state-recovery-0002.json','provenance/decisions/0002-current-game-design.md','provenance/checkpoints/0002-game-design.md','development/checkpoints/0002-game-design.md','tools/validators/validate-design-state.mjs','tests/regression/design-state-validator.test.mjs','data/manifests/design-checkpoint-0002.json'];
    for(const p of required)check(inventory.files.includes(p),`Design inventory includes ${p}`);
    for(const [p,expected]of Object.entries(inventory.preserved_sha256))check(hash(p)===expected,`Protected baseline unchanged: ${p}`);
    for(const p of inventory.files) {
      const valid=typeof p==='string'&&!path.isAbsolute(p)&&!p.includes('\\')&&!p.split('/').some(x=>['..','.git','_inbox',''].includes(x));
      check(valid,`Safe inventory path: ${p}`);
      if(!valid)continue;
      check(fs.existsSync(path.join(root,p)),`Inventory file exists: ${p}`);
      if(p.endsWith('.md'))for(const match of read(p).matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
        const dest=match[1].split('#')[0];if(!dest||/^[a-z]+:/i.test(dest))continue;
        check(fs.existsSync(path.resolve(root,path.dirname(p),dest)),`Local link in ${p}: ${dest}`);
      }
    }
    const cycle=JSON.parse(read('data/cycles/cycle_01/manifest.json'));
    check(cycle.utility_structure_status==='DESIGN STRUCTURE ACCEPTED','Cycle structure status');
    check(cycle.utility_structure_ref==='../../manifests/accepted-state.json#/utility_structure','Cycle points to single accepted-state model');
    check(cycle.card_definitions_imported===false,'Cycle does not claim final runtime catalog');
    check(read('development/modules/utilities/README.md').includes('DESIGN — DESIGN STRUCTURE ACCEPTED'),'Utility module design status');
  }catch(error){errors.push(`Repository validation could not complete: ${error.message}`);}
  return {errors,checks};
}

if(process.argv[1] && path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
  const {errors,checks}=validateDesignRepository(root);
  console.log('Scope: supplied design-data consistency, provenance and repository records only.');
  console.log('Does NOT validate mathematical legality/QMO closure, gameplay balance, runtime effects, Blender/GPU geometry/rendering, AI or multiplayer correctness.');
  if(errors.length){for(const error of errors)console.error(`FAIL: ${error}`);process.exitCode=1;}
  console.log(`${errors.length?'FAIL':'PASS'} — ${checks} design checks; ${errors.length} error(s).`);
}
