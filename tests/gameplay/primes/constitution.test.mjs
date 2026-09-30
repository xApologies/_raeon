import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {rules,startPrime,primeState,restorePrime,degradePrime,reactivatePrime,spendPrime} from '../rule-model.mjs';
const catalog = JSON.parse(fs.readFileSync(new URL('../../../data/cycles/cycle_01/primes/status.json',import.meta.url),'utf8')).objects;
const green = {id:'prime-instance',slot:2,family:'Universal',rank:4,H:4,C:3};
test('all fourteen ordinary identities start healthy, uncharged and fixed in their supplied slot',()=>{
  assert.equal(catalog.length,14);
  for(const entry of catalog){const p=startPrime(entry,entry.identity_key,2);assert.equal(p.H,entry.rank_value);assert.equal(p.C,0);assert.equal(primeState(p),'HEALTHY_UNCHARGED');assert.equal(p.slot,2);}
});
test('four Prime operational states include damaged health with no operating permission',()=>{
  for(const [H,C,state] of [[4,0,'HEALTHY_UNCHARGED'],[4,3,'OPERATIONAL_CHARGED'],[1,0,'DAMAGED_NON_OPERATIONAL'],[0,0,'INACTIVE']])assert.equal(primeState({...green,H,C}),state);
  assert.equal(spendPrime({...green,H:2},1,'RESTORE','ACTIVE','friendly',true).status,'REJECTED');
  assert.throws(()=>primeState({...green,H:0,C:1}),/Invalid ordinary/);
});
test('Restore heals before charging; overflow remains unresolved without partial mutation',()=>{
  const input={...green,rank:6,H:4,C:0};const result=restorePrime(input,4);
  assert.deepEqual(result.value,{...input,H:6,C:2});assert.equal(input.H,4);
  assert.equal(restorePrime(green,7).status,'OPEN_OVERFLOW');
  assert.deepEqual(restorePrime(green,7).value,green);
});
test('Degrade consumes shield before health and preserves identity/slot at INACTIVE',()=>{
  assert.deepEqual(degradePrime(green,6),{...green,H:1,C:0});
  assert.deepEqual(degradePrime(green,99),{...green,H:0,C:0});
});
test('White reactivation is 1/0; rank-one is healthy uncharged, higher rank remains damaged',()=>{
  for(const rank of [1,4,7]){
    const inactive={...green,rank,H:0,C:0};assert.equal(restorePrime(inactive,1).status,'EXPLICIT_REACTIVATION_REQUIRED');
    const revived=reactivatePrime(inactive);assert.deepEqual(revived,{...inactive,H:1});
    assert.equal(primeState(revived),rank===1?'HEALTHY_UNCHARGED':'DAMAGED_NON_OPERATIONAL');
    assert.equal(spendPrime(revived,1,'RESTORE','DEFENSE','friendly',true).status,'REJECTED');
  }
});
test('all families intersect direction with ACTIVE/DEFENSE and target side',()=>{
  const admitted=new Set(['Restore/RESTORE/ACTIVE/friendly','Restore/RESTORE/DEFENSE/friendly','Degrade/DEGRADE/ACTIVE/hostile','Universal/RESTORE/ACTIVE/friendly','Universal/RESTORE/DEFENSE/friendly','Universal/DEGRADE/ACTIVE/hostile']);
  for(const family of ['Restore','Degrade','Universal'])for(const operation of ['RESTORE','DEGRADE'])for(const window of ['ACTIVE','DEFENSE'])for(const side of ['friendly','hostile']){
    const key=[family,operation,window,side].join('/');
    assert.equal(spendPrime({...green,family},1,operation,window,side,true).status,admitted.has(key)?'VALID_EXAMPLE':'REJECTED',key);
  }
});
test('multiple partial Prime spends retain shield, do not tap or alter H, and cannot overspend',()=>{
  const first=spendPrime(green,1,'RESTORE','ACTIVE','friendly',true).value;
  const second=spendPrime(first,1,'RESTORE','DEFENSE','friendly',true).value;
  assert.deepEqual(second,{...green,C:1});assert.equal(degradePrime(second,2).H,3);
  assert.equal(spendPrime(second,2,'RESTORE','ACTIVE','friendly',true).status,'REJECTED');
  assert.equal(spendPrime(second,1,'RESTORE','ACTIVE','friendly',false).status,'OPEN_ADMISSION');
  assert.equal(rules.prime.spend.once_per_turn_tap_limited,false);
});
