import {test} from 'node:test';
import assert from 'node:assert/strict';
import {moveCard,rules} from '../rule-model.mjs';
const card = n => ({id:'instance-'+n,kind:'CARD_GEOMETRIC',definition:'FG-001'});
test('admitted seventh Hand card preserves persistent identity, definition and source order',()=>{
  const source=[card(0),card(1)],hand=Array.from({length:6},(_,i)=>card(i+2));
  const result=moveCard(source,hand,source[0].id,'Hand',true);
  assert.equal(result.destination.length,7);assert.equal(result.destination.at(-1),source[0]);
  assert.deepEqual(result.source,[source[1]]);assert.equal(source.length,2);
});
test('eighth Hand admission fails atomically; no overflow or discard invented',()=>{
  const source=[card(0)],hand=Array.from({length:7},(_,i)=>card(i+1));
  const result=moveCard(source,hand,source[0].id,'Hand',true);
  assert.equal(result.status,'REJECTED');assert.equal(result.source,source);assert.equal(result.destination,hand);
  assert.equal(rules.match.match_rules.hand_overflow,'OPEN');
});
test('container moves reject noncards, duplicate instance IDs and unadmitted requests',()=>{
  for(const [source,dest,admitted] of [[[{...card(0),kind:'FIELD'}],[],true],[[card(0)],[card(0)],true],[[card(0)],[],false]]){
    const result=moveCard(source,dest,'instance-0','Hand',admitted);assert.equal(result.status,'REJECTED');assert.equal(result.source,source);
  }
});
