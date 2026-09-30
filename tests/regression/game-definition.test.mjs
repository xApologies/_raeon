import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {copyFixtureFile} from './fixture-files.mjs';
import {matchesGameDefinitionAmendment} from '../../tools/validators/game-definition-contract.mjs';
import {validateGameDefinition} from '../../tools/validators/validate-game-definition.mjs';
import {decisionPath, loadGameDefinitionContract, reverseAmendments, projectBeforeGameDefinition} from '../../tools/validators/game-definition-contract.mjs';
import {loadDesignState} from '../../tools/validators/load-design-state.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const read=(p)=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
test('accepted game-definition amendments preserve catalog bytes and current authority',()=>assert.deepEqual(validateGameDefinition(root).errors,[]));
test('historical projection never hides an unrelated change',()=>{
  const state=loadDesignState(root);state.cycle_01.constructed_deck_size=99;
  assert.equal(projectBeforeGameDefinition(root,state).cycle_01.constructed_deck_size,99);
});
const contract=loadGameDefinitionContract(root);
for(const [name,file,mutate] of [
  ['Hand eight','data/game/match.json',d=>d.values.match_rules.hand_normal_capacity=8],
  ['legacy OPEN Hand','data/cycles/cycle_01/utilities/draw_deck.json',d=>d.values.hand_size_maximum='OPEN'],
  ['defensive counterattack','data/game/match.json',d=>d.values.match_rules.authority_windows.DEFENSE.DEGRADE='hostile'],
  ['turn-end refresh','data/game/match.json',d=>d.values.match_rules.active_end_refreshes_fields=true],
  ['invented refresh boundary','data/game/match.json',d=>d.values.match_rules.refresh_boundary='start of turn'],
  ['restored obsolete OPEN ledger','data/manifests/accepted-state.json',d=>d.open_items.push('Hand-size maximum and overflow behavior')],
  ['charged Prime start','data/cycles/cycle_01/primes/working-model.json',d=>d.values.starting_state.C=7],
  ['damaged Prime operates','data/cycles/cycle_01/primes/working-model.json',d=>d.values.spend.requires_state='DAMAGED_NON_OPERATIONAL'],
  ['Prime tap limit','data/cycles/cycle_01/primes/working-model.json',d=>d.values.spend.once_per_turn_tap_limited=true],
  ['ten Configuration Spaces','data/topology/configuration-spaces.json',d=>d.values.maximum_active_per_player=10],
  ['Configuration Space in QMO corpus','data/topology/configuration-spaces.json',d=>d.values.part_of_qmo_corpus=true],
  ['one resolution gate enough','data/topology/configuration-spaces.json',d=>d.values.resolution_gates.both_required=false],
  ['field generates native instead of current color','data/topology/configuration-spaces.json',d=>d.values.field_runtime.ready_generates='native color'],
  ['field use unresolves','data/topology/configuration-spaces.json',d=>d.values.field_runtime.generation_unresolves_topology=true],
  ['invented destruction ordering','data/topology/configuration-spaces.json',d=>d.values.field_runtime.destruction_transaction_order='FGs first'],
  ['Emergent consumes slot','data/topology/relationships.json',d=>d.values.emergence.configuration_slots_consumed=1],
  ['merge loses FG identities','data/topology/relationships.json',d=>d.values.merge.fg_instance_identities_preserved=false],
  ['card movement recreates identity','data/board/genesis-horizon.json',d=>d.values.card_instances.movement_preserves_identity=false],
  ['board port equals container','data/board/genesis-horizon.json',d=>d.values.runtime_object.ports_distinct_from_children=false],
  ['second color bus','data/platform/runtime-direction.json',d=>d.values.runtime_direction.transport.separate_board_color_bus=true],
  ['unverified Genesis marked current','data/platform/runtime-direction.json',d=>d.values.runtime_direction.genesis_source_gate.verified_by_this_reconciliation=true],
])test('game-definition guard rejects '+name,()=>{
  const data=read(file);mutate(data);
  assert.throws(()=>reverseAmendments(data,contract.json_changes[file]),/Unapproved game-definition semantic value/);
});
for(const [name,mutate,expected] of [
  ['modified decision',dir=>fs.appendFileSync(path.join(dir,decisionPath),' '),'Reviewed game-definition amendment'],
  ['modified atlas',dir=>fs.appendFileSync(path.join(dir,'data/qmo/cycle1/atlas.json'),' '),'Unchanged catalog bytes'],
])test('repository guard rejects '+name,()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'raeon-game-definition-test-'));
  try {
    for(const file of read('data/manifests/current-files.json').files){fs.mkdirSync(path.dirname(path.join(dir,file)),{recursive:true});copyFixtureFile(root,dir,file);}
    mutate(dir);assert.ok(validateGameDefinition(dir).errors.some(e=>e.includes(expected)));
  } finally {
    assert.equal(path.dirname(path.resolve(dir)),path.resolve(os.tmpdir()));assert.ok(path.basename(dir).startsWith('raeon-game-definition-test-'));
    fs.rmSync(dir,{recursive:true,force:true});
  }
});

test('approved module contract hash is exact; changed bytes and wrong prior authority are rejected',()=>{
  const file='game/board/README.md', entry=contract.approved_file_amendments[file];
  assert.equal(matchesGameDefinitionAmendment(root,file,entry.after_sha256,entry.before_sha256),true);
  assert.equal(matchesGameDefinitionAmendment(root,file,'tampered',entry.before_sha256),false);
  assert.equal(matchesGameDefinitionAmendment(root,file,entry.after_sha256,'wrong baseline'),false);
});
