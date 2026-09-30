import {test} from 'node:test';
import assert from 'node:assert/strict';
import {rules,canAttachSpace,resolveExample,useField,endActive,changeFieldColor} from '../rule-model.mjs';
const field={qmo:'M-G-01',native:4,current:4,availability:'READY',state:'RESOLVED',supportIds:['fg-a','fg-b']};
test('configuration expansion stops at nine active or six additional, with admission required',()=>{
  assert.equal(canAttachSpace(8,5,true),true);assert.equal(canAttachSpace(9,6,true),false);
  assert.equal(canAttachSpace(7,6,true),false);assert.equal(canAttachSpace(3,0,false),false);
  assert.deepEqual(rules.board.configuration_region.permanent,['A','B','C']);assert.equal(rules.board.configuration_region.additional_at_boot,0);
});
test('both membership and pose gates must pass; other outcomes do not invent a field',()=>{
  for(const membership of ['VALID','TERMINATES','OPEN','UNTESTED','NOT_APPLICABLE'])for(const pose of ['VALID','TERMINATES','OPEN','UNTESTED','NOT_APPLICABLE']){
    const result=resolveExample(6,membership,pose,'M-G-01');
    assert.equal(result.state,membership==='VALID'&&pose==='VALID'?'RESOLVED':'CONFIGURING');
  }
  assert.deepEqual(resolveExample(0,'VALID','VALID','M-G-01'),{state:'EMPTY',qmo:null});
  assert.equal(rules.configuration.part_of_qmo_corpus,false);
});
test('degraded current Red output is one, becomes USED, and does not change Green topology',()=>{
  const degraded=changeFieldColor(field,-3).value;const used=useField(degraded);
  assert.equal(used.output,1);assert.equal(used.value.qmo,field.qmo);assert.equal(used.value.state,'RESOLVED');
  assert.equal(useField(used.value).status,'REJECTED');assert.equal(field.availability,'READY');
});
test('ACTIVE end preserves READY or USED into DEFENSE and leaves refresh boundary OPEN',()=>{
  assert.equal(endActive(field),field);const used=useField(field).value;assert.equal(endActive(used),used);
  assert.equal(useField(endActive(used)).status,'REJECTED');
  assert.equal(rules.configuration.field_runtime.refresh_boundary,'OPEN');
});
test('Restore caps at native color; zero destruction identifies FG routing without inventing transaction order',()=>{
  assert.equal(changeFieldColor({...field,current:1},3).value.current,4);
  assert.equal(changeFieldColor({...field,current:1},99).value.current,4);
  const destroyed=changeFieldColor(field,-4);assert.equal(destroyed.destination,'Graveyard');
  assert.deepEqual(destroyed.supportIds,field.supportIds);assert.equal(destroyed.activeFieldExposed,false);assert.equal(destroyed.ordering,'OPEN');
});
