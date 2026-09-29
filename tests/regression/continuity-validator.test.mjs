import {test} from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {loadContinuity,validateContinuityData,validateContinuityRepository} from '../../tools/validators/validate-continuity.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const baseline=loadContinuity(root);
test('accepts reconciled continuity and source integrity',()=>assert.deepEqual(validateContinuityRepository(root).errors,[]));
for(const [name,change,label] of [
 ['arbitrary rotation',s=>s.generator_interaction.values.arbitrary_free_xyz_rotation=true,'No arbitrary free XYZ'],
 ['count as closure',s=>s.generator_interaction.values.count_alone_authorizes_closure=true,'Count is not'],
 ['closure graveyard penalty',s=>s.configuration_spaces.values.failed_closure_auto_graveyard=true,'No failed-closure'],
 ['unresolved slot hidden',s=>s.board.values.configuring_space_visible=false,'Unresolved field visible'],
 ['discard pile',s=>s.board.values.infrastructure.push('Discard'),'Only accepted infrastructure'],
 ['exile',s=>s.board.values.exile_zone=true,'No exile'],
 ['moving Prime positions',s=>s.board.values.prime_positions_fixed=false,'Fixed Prime'],
 ['coordinate identity',s=>s.configuration_spaces.values.screen_position_is_identity=true,'Coordinates are not'],
 ['duplicate view state',s=>s.board.values.shared_underlying_state=false,'Views share'],
 ['independent fused supports',s=>s.relationships.values.fusion.supports_independently_operational=true,'Fused supports'],
 ['destroyed emergent supports',s=>s.relationships.values.emergence.supports_remain_distinct=false,'Emergent supports'],
 ['resolved permanent conflict',s=>s.relationships.values.fusion.permanent_base_identity_accounting='destroy base','Do not silently resolve'],
 ['selected R88 branch',s=>s.manifest.propagation.selected_branch='A','R88 branches'],
 ['research as validated math',s=>s.manifest.propagation.integration_status='VALID','Source claims'],
 ['competing Generator catalog',s=>s.generator_interaction.values.objects=[{id:'FG-001'}],'No competing'],
 ['Prime model promoted',s=>s.prime_working_model.authority='GAME_CANON','Prime model remains'],
 ['invented expiry',s=>s.configuration_spaces.values.temporary_expiry='turn end','Unresolved Configuration Space'],
 ['missing data termination',s=>s.generator_interaction.values.missing_data_is_termination=true,'Missing data is not'],
 ['phase promotion',s=>s.manifest.phase='PROTOTYPE','Continuity cannot advance'],
])test('rejects '+name,()=>{const state=structuredClone(baseline);change(state);assert.ok(validateContinuityData(state).errors.some(x=>x.includes(label)));});
