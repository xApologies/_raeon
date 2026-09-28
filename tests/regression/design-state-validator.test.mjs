import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateDesignState,validateDesignRepository} from '../../tools/validators/validate-design-state.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const baseline=JSON.parse(fs.readFileSync(path.join(root,'data/manifests/accepted-state.json'),'utf8'));
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
];
for(const [name,mutate,expected]of cases)test(name,()=>{const state=structuredClone(baseline);mutate(state);const result=validateDesignState(state);assert.ok(result.errors.some(x=>x.includes(expected)),JSON.stringify(result));});
test('rejects malformed design data without throwing',()=>assert.ok(validateDesignState({}).errors.length));
for(const [name,file,mutation,expected]of [
 ['rejects altered recovery source','provenance/sources/current-state-recovery-0002.txt',p=>fs.appendFileSync(p,'altered'),'Recovery source integrity'],
 ['rejects constitution replacement','PROJECT_CONSTITUTION.md',p=>fs.appendFileSync(p,'altered'),'Protected baseline unchanged'],
 ['rejects missing design document','design/cards/cycle_01/UTILITIES.md',p=>fs.unlinkSync(p),'Inventory file exists']
])test(name,()=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'raeon-design-test-'));
 try {
  const inventory=JSON.parse(fs.readFileSync(path.join(root,'data/manifests/design-checkpoint-0002.json'),'utf8'));
  for(const p of inventory.files){fs.mkdirSync(path.dirname(path.join(dir,p)),{recursive:true});fs.copyFileSync(path.join(root,p),path.join(dir,p));}
  mutation(path.join(dir,file));assert.ok(validateDesignRepository(dir).errors.some(x=>x.includes(expected)));
 } finally {
  const resolved=path.resolve(dir);assert.equal(path.dirname(resolved),path.resolve(os.tmpdir()));assert.ok(path.basename(resolved).startsWith('raeon-design-test-'));fs.rmSync(resolved,{recursive:true,force:true});
 }
});
