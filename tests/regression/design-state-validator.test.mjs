import {test} from 'node:test';
import {loadDesignState} from '../../tools/validators/load-design-state.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateDesignState,validateDesignRepository} from '../../tools/validators/validate-design-state.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const baseline=loadDesignState(root);
const family=s=>s.utility_structure.families;
// These tests exercise data-validation failures; none asserts executable gameplay.
test('accepts supplied fifty-slot design with unresolved details',()=>assert.deepEqual(validateDesignState(baseline).errors,[]));
const cases=[
 ['rejects utility override of closure',s=>s.governing_law.utilities_override_closure=true,'Mathematics permission rule'],
 ['rejects color uniqueness',s=>s.cycle_01.additional_color_uniqueness_rule=true,'No color uniqueness rule'],
 ['rejects working rank interpreted as mandatory cost',s=>s.color_interpretation.rank_always_equals_resource_cost=true,'Charge versus Utility rank'],
 ['rejects Universal with no flexibility penalty',s=>family(s).transduction.universal[0].magnitude=2,'Universal rank/magnitude'],
 ['rejects Activation creating color',s=>family(s).activation.creates_color=true,'Activation creates no color'],
 ['rejects invented Activation detail',s=>family(s).activation.per_rank_behavior='FINAL','Activation details remain OPEN'],
 ['rejects permanent Sandbox colored-capacity restriction',s=>s.sandbox.permanent_uses_temporary_colored_capacity=true,'Permanent Sandbox capacity exemption'],
 ['rejects capacity used as closure proof',s=>s.sandbox.capacity_guarantees_closure=true,'Capacity cannot guarantee closure'],
 ['rejects wrong temporary capacity',s=>s.sandbox.temporary_capacity.Red=4,'Temporary Sandbox capacities'],
 ['rejects raw Draw 4',s=>family(s).draw_deck.slots[2].effect.count=4,'draw_deck slot 3'],
 ['rejects invented hand-size limit',s=>family(s).draw_deck.hand_size_maximum=7,'Hand size remains OPEN'],
 ['rejects working ranks silently promoted to final canon',s=>family(s).draw_deck.slots[0].working_rank.authority='GAME_CANON','draw_deck slot 1'],
 ['rejects unrestricted Deep Survey tutor',s=>family(s).draw_deck.slots[6].effect.unrestricted_exact_card_tutor=true,'draw_deck slot 7'],
 ['rejects Exchange granting extra cards',s=>family(s).draw_deck.slots[5].effect.net_hand_count_change=1,'draw_deck slot 6'],
 ['rejects ordinary Prime recovery',s=>family(s).graveyard_recovery.slots[5].effect.card_type='Prime','graveyard_recovery slot 6'],
 ['rejects automatic manifold reconstruction',s=>family(s).graveyard_recovery.automatically_reconstructs_manifold=true,'Recovery cannot reconstruct manifolds'],
 ['rejects Shield Lock below Blue',s=>family(s).stability_protection.slots[3].minimum_working_rank='Green','Shield Lock Blue floor'],
 ['rejects Anchor bypassing closure',s=>family(s).stability_protection.slots[4].effect.bypasses_closure=true,'Structural Anchor lethal-to-Red'],
 ['rejects Amplification above Violet',s=>family(s).stability_protection.slots[5].effect.maximum_charge=7,'Amplification cap/support restrictions'],
 ['rejects support-loss survival',s=>family(s).stability_protection.slots[5].effect.preserves_after_support_loss=true,'Amplification cap/support restrictions'],
 ['rejects direct Emergent targeting',s=>s.emergent_fields.independently_targetable=true,'Emergent support and targeting'],
 ['rejects Coupling Stabilizer replacing sixth slot',s=>family(s).stability_protection.slots[5].concept='Coupling Stabilizer','Six Stability concepts'],
 ['rejects claimed fifty slots with a missing slot',s=>family(s).activation.ranks.pop(),'Actual structural slot counts'],
 ['rejects premature Utility FORMALIZED',s=>s.utility_structure.module_status='FORMALIZED','No premature Utility FORMALIZED/GOLD'],
 ['rejects Fourth Prime as deck card',s=>s.black.fourth_prime.deck_card=true,'Fourth Prime support rule'],
 ['rejects player-to-player wagering',s=>s.long_term_direction.player_to_player_credit_wagering=true,'Economy boundary: player_to_player_credit_wagering'],
 ['rejects finalization of economy direction',s=>s.long_term_direction.authority='GAME_CANON','Economy direction authority'],
 ['rejects invented match duration',s=>s.product_intent.exact_match_duration=10,'No invented match duration'],

 ['rejects premature implementation-ready catalog',s=>s.utility_structure.implementation_ready=true,'No implementation-ready catalog'],
 ['rejects arbitrary final Utility IDs',s=>s.utility_structure.identifier_direction.assigned_ids=['UT-001'],'No arbitrary final Utility IDs'],
 ['rejects invented Amplification overflow',s=>s.utility_clarifications.emergent_amplification_overflow='wrap to Red','Utility clarification constraints'],
 ['rejects Black bypass of QMO legality',s=>s.black.design_philosophy.bypasses_qmo_legality=true,'Black legality and separate catalog'],
 ['rejects printed-card claims for Black concepts',s=>s.black.working_concepts[0].final_printed_card=true,'Black concepts remain provisional and legal'],
 ['rejects Shield changing Prime identity',s=>s.black.working_concepts[0].concept.prime_identity_unchanged=false,'Black concepts remain provisional and legal'],
 ['rejects invented Topaz QMO',s=>s.black.working_concepts[1].target_qmo='invented-qmo','Black concepts remain provisional and legal'],
 ['rejects OR support condition',s=>s.black.fourth_prime_condition.operator='OR','Fourth Prime requires ALL three alive flags'],
 ['rejects missing support flag',s=>s.black.fourth_prime_condition.required_alive_flags.pop(),'Fourth Prime requires ALL three alive flags'],
 ['rejects Fourth Prime automatically destroyed',s=>s.black.fourth_prime_condition.false_result_requires_destruction=true,'Fourth Prime requires ALL three alive flags'],
 ['rejects restoration direction authorizing resurrection',s=>s.black.fourth_prime_condition.authorizes_prime_resurrection=true,'Fourth Prime requires ALL three alive flags'],
 ['rejects Black Mode visible onboarding bar',s=>s.black_mode.ordinary_onboarding_progress_bar=true,'Hidden Black Mode and honest AI challenge'],
 ['rejects exact store price',s=>s.long_term_direction.exact_store_price=0.99,'Economy OPEN field: exact_store_price'],
 ['rejects purchased credit bundles',s=>s.long_term_direction.gameplay_credit_bundles=true,'Product boundary: gameplay_credit_bundles'],
 ['rejects session target as guarantee',s=>s.product_intent.hard_duration_guarantee=true,'Session target is not a duration guarantee'],
 ['rejects claimed adaptive AI',s=>s.ai_direction.adaptive_player_modeling.implemented=true,'AI direction with no implementation or ML selection'],
 ['rejects selected ML architecture',s=>s.ai_direction.adaptive_player_modeling.ml_architecture='selected','AI direction with no implementation or ML selection'],
 ['rejects selected transport',s=>s.multiplayer_direction.transport='Bluetooth','Local P2P direction without transport selection'],
 ['rejects rendered frames as gameplay state',s=>s.multiplayer_direction.transmits_rendered_frames_as_gameplay_state=true,'Local P2P direction without transport selection'],
 ['rejects literal five-dimensional Blender rendering',s=>s.rendering_direction.blender_literally_renders_five_spatial_dimensions=true,'Rendering projection and mathematical authority'],
 ['rejects renders changing legality',s=>s.rendering_direction.rendering_changes_mathematical_legality=true,'Rendering projection and mathematical authority'],
 ['rejects invented camera',s=>s.board_presentation.camera='fixed orbit','Board presentation with OPEN UI details'],
 ['rejects invented starting hand size',s=>s.turn_match_open.starting_hand_size=5,'Unresolved turn/match rules remain OPEN'],
 ['rejects invented victory condition',s=>s.turn_match_open.victory_condition='destroy all Primes','Unresolved turn/match rules remain OPEN'],
 ['rejects fabricated Cycle source import',s=>s.cycle_production_direction.existing_source_package='IMPORTED','Cycle flow and missing authoritative source'],
 ['rejects missing projection import requirement',s=>s.source_import_required.pop(),'Source import requirements retained and expanded'],
];
for(const [name,mutate,expected]of cases)test(name,()=>{const state=structuredClone(baseline);mutate(state);const result=validateDesignState(state);assert.ok(result.errors.some(x=>x.includes(expected)),JSON.stringify(result));});
test('rejects malformed design data without throwing',()=>assert.ok(validateDesignState({}).errors.length));
for(const [name,file,mutation,expected]of [
 ['rejects altered recovery 0003 source','provenance/sources/recovery-0003-block-3.txt',p=>fs.appendFileSync(p,'altered'),'Recovery 0003 block 3 integrity'],
 ['rejects altered recovery source','provenance/sources/current-state-recovery-0002.txt',p=>fs.appendFileSync(p,'altered'),'Recovery source integrity'],
 ['rejects development constitution replacement','DEVELOPMENT_CONSTITUTION.md',p=>fs.appendFileSync(p,'altered'),'Protected baseline unchanged'],
 ['rejects constitution replacement','PROJECT_CONSTITUTION.md',p=>fs.appendFileSync(p,'altered'),'Protected baseline unchanged'],
 ['rejects missing design document','design/cards/cycle_01/utilities/SYSTEM.md',p=>fs.unlinkSync(p),'Inventory file exists']
])test(name,()=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'raeon-design-test-'));
 try {
  const inventory=JSON.parse(fs.readFileSync(path.join(root,'data/manifests/design-checkpoint-0004.json'),'utf8'));
  for(const p of inventory.files){fs.mkdirSync(path.dirname(path.join(dir,p)),{recursive:true});fs.copyFileSync(path.join(root,p),path.join(dir,p));}
  mutation(path.join(dir,file));assert.ok(validateDesignRepository(dir).errors.some(x=>x.includes(expected)));
 } finally {
  const resolved=path.resolve(dir);assert.equal(path.dirname(resolved),path.resolve(os.tmpdir()));assert.ok(path.basename(resolved).startsWith('raeon-design-test-'));fs.rmSync(resolved,{recursive:true,force:true});
 }
});
