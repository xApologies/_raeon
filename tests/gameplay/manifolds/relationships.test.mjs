import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {rules,liveEmergents,mergeExample} from '../rule-model.mjs';
test('simultaneous pairwise emergents lose only edges whose required support is lost',()=>{
  const pairs=JSON.parse(fs.readFileSync(new URL('../../../data/qmo/cycle1/manifold_pair_relations.json',import.meta.url),'utf8'));
  const instances={'M-B-01':'A','M-B-02':'B','M-B-03':'C'};
  const edges=pairs.filter(p=>p.emergent_status==='VALID'&&instances[p.a_manifold]&&instances[p.b_manifold]).map(p=>({supports:[instances[p.a_manifold],instances[p.b_manifold]],qmo:p.emergent_qmo}));
  assert.equal(edges.length,3); // Read existing admitted pairs; no new QMO derivation.
  assert.deepEqual(liveEmergents(['A','B','C'],edges),edges);
  assert.deepEqual(liveEmergents(['B','C'],edges),[edges[2]]);
  assert.deepEqual(liveEmergents(['C'],edges),[]);
  assert.equal(rules.relationships.emergence.configuration_slots_consumed,0);
  assert.equal(rules.relationships.emergence.directly_attackable,false);
});
test('merge identity union preserves instances, including two legal copies of one FG definition',()=>{
  const left=[{id:'a',definition:'FG-001'},{id:'b',definition:'FG-002'}];
  const right=[{id:'c',definition:'FG-001'}];const result=mergeExample(left,right,true);const combined=result.contents;
  assert.deepEqual(combined.map(x=>x.id),['a','b','c']);assert.equal(combined[0],left[0]);assert.equal(combined[2],right[0]);
  assert.equal(result.independentSpaces,1);
  assert.equal(mergeExample(left,[left[0]],true).status,'REJECTED');
  const rejected=mergeExample(left,right,false);assert.equal(rejected.status,'REJECTED');assert.equal(rejected.left,left);
  assert.equal(rules.relationships.merge.independent_spaces_before,2);assert.equal(rules.relationships.merge.independent_spaces_after,1);
  assert.equal(rules.relationships.merge.fg_instance_identities_preserved,true);
  assert.equal(rules.relationships.merge.merged_capacity_ceiling,'OPEN');
  assert.equal(rules.relationships.fusion.permanent_base_identity_accounting,'OPEN');
});
