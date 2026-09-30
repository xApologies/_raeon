import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {copyFixtureFile} from './fixture-files.mjs';
import {loadFullMigration,validateFullMigrationData,validateFullMigrationRepository} from '../../tools/validators/validate-full-migration.mjs';
import {loadDesignState} from '../../tools/validators/load-design-state.mjs';
import {projectBeforeFullMigration} from '../../tools/validators/full-migration-contract.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const baseline=loadFullMigration(root);
test('full migration preserves original sources and reconciles accepted design',()=>assert.deepEqual(validateFullMigrationRepository(root).errors,[]));
test('approved amendments do not erase unrelated historical values',()=>{
 const s=loadDesignState(root);s.utility_structure.families.transduction.restore[0].charge_delta=999;
 const projected=projectBeforeFullMigration(root,s);
 assert.equal(projected.utility_structure.families.transduction.restore[0].charge_delta,999);
 assert.throws(()=>projectBeforeFullMigration(root,{...loadDesignState(root),runtime_direction:{language:'invented'}}),/Unapproved (?:full-migration|game-definition) semantic value/);
});
for(const [name,mutate,label]of [
 ['old 200-card count',s=>s.manifest.counts.ordinary_total=200,'185 ordinary identities'],
 ['missing Prime identity',s=>s.prime_catalog.objects.pop(),'Complete Prime catalog'],
 ['duplicate Prime identity',s=>s.prime_catalog.objects[0]=s.prime_catalog.objects[1],'Unique structural Prime identities'],
 ['Universal White Prime',s=>s.prime_catalog.objects.at(-1).rank='White','Prime family/rank/direction'],
 ['Prime copies above one',s=>s.prime_catalog.copy_limit=2,'Prime copy limit'],
 ['charge changes rank',s=>s.prime_model.values.identity_and_rank_change_with_charge=true,'Charge never changes'],
 ['charge before health',s=>s.prime_model.values.friendly_restore.order=['C','H'],'Restore heals H before C'],
 ['charge on damaged intrinsic health',s=>s.prime_model.values.friendly_restore.charge_requires_full_intrinsic_health=false,'Full H before charge'],
 ['mandatory whole-charge spending',s=>s.prime_model.values.spend.partial_allowed=false,'Partial charge spending'],
 ['Restore Prime negative spending',s=>s.prime_model.values.spend.Restore=['DEGRADE'],'Restore direction'],
 ['Universal ceiling above Green',s=>s.prime_model.values.spend.universal_maximum_rank='White','Universal Green ceiling'],
 ['health before shield damage',s=>s.prime_model.values.hostile_degradation.order=['H','C'],'Degradation hits C before H'],
 ['inactive Prime to Graveyard',s=>s.prime_model.values.inactive.moves_to_graveyard=true,'INACTIVE in fixed position'],
 ['reactivation fully heals',s=>s.restore_prime.effect.to.H=7,'Restore Prime reactivation to 1/0 only'],
 ['reactivation grants charge',s=>s.restore_prime.effect.to.C=1,'Restore Prime reactivation to 1/0 only'],
 ['incorrect Restore example',s=>s.prime_model.values.examples[0].after.C=3,'Prime numerical example'],
 ['incorrect partial spend example',s=>s.prime_model.values.examples[1].after.C=0,'Prime numerical example'],
 ['incorrect degradation example',s=>s.prime_model.values.examples[2].after.H=1,'Prime numerical example'],
 ['resolved space frozen',s=>s.configuration_spaces.values.resolved_reopening='OPEN','Resolved reconfiguration accepted'],
 ['independent FG extraction',s=>s.configuration_spaces.values.individual_extraction_or_transfer=true,'No individual committed extraction'],
 ['capacity as required count',s=>s.configuration_spaces.values.capacity_is_maximum_not_required_count=false,'Capacity is maximum'],
 ['field color equals capacity',s=>s.configuration_spaces.values.capacity_color_independent_of_field_color=false,'Capacity and field colors independent'],
 ['orbit camera',s=>s.generator_interaction.values.orbit_camera=true,'No orbit camera'],
 ['positional Z control',s=>s.generator_interaction.values.player_controlled_position_z=true,'No positional Z'],
 ['only 2D orientation',s=>s.generator_interaction.values.orientation_dimensions=2,'3D orientation'],
 ['partial feedback invents closure',s=>s.generator_interaction.values.partial_feedback.creates_legality=true,'Partial feedback cannot invent legality'],
 ['single FG field',s=>s.generator_interaction.values.partial_feedback.one_fg_forms_field=true,'One FG forms no field'],
 ['merge loses contents',s=>s.relationships.values.merge.committed_contents_preserved=false,'Merge preserves contents'],
 ['merge retains both independent spaces',s=>s.relationships.values.merge.independent_spaces_after=2,'Merge board-width cost'],
 ['invented merged capacity',s=>s.relationships.values.merge.merged_capacity_ceiling=8,'No invented merged capacity ceiling'],
 ['merge count guarantees closure',s=>s.relationships.values.merge.count_guarantees_closure=true,'Merged count is not closure'],
 ['fusion construction puzzle',s=>s.relationships.values.fusion.new_minigame=true,'No fusion minigame'],
 ['separate emergent FG puzzle',s=>s.relationships.values.emergence.separate_fg_construction=true,'No separate Emergent construction'],
 ['emergent removes supports',s=>s.relationships.values.emergence.supports_remain_distinct=false,'Emergent supports remain distinct'],
 ['runtime truth moves to platform',s=>s.runtime.values.runtime_direction.game_truth=['platform shell'],'Authoritative runtime truth'],
 ['Blender as live game runtime',s=>s.runtime.values.runtime_direction.blender_role='live runtime','Blender offline'],
 ['claimed Genesis implementation',s=>s.runtime.values.runtime_direction.implemented=true,'No runtime implementation claim'],
 ['premature production advancement',s=>s.manifest.phase='PROTOTYPE','Whole-game PREPRODUCTION']
])test('full migration rejects '+name,()=>{
 const value=structuredClone(baseline);mutate(value);
 assert.ok(validateFullMigrationData(value).errors.some(x=>x.includes(label)),label);
});
for(const [name,mutate,label]of [
 ['rewritten amendment ledger',d=>fs.appendFileSync(path.join(d,'provenance/audits/full-migration-2026-09-29-semantic-changes.json'),' '),'Reviewed full-migration contract'],
 ['wrong LFS source identity',d=>fs.writeFileSync(path.join(d,'provenance/sources/full-migration-2026-09-29/raeon_FULL_exhaustive_migration_2026-09-29.zip'),'version https://git-lfs.github.com/spec/v1\noid sha256:incorrect\nsize 242064399\n'),'Full source LFS identity'],
 ['changed original Utility',d=>{const p=path.join(d,'data/cycles/cycle_01/utilities/transduction.json');fs.appendFileSync(p,' ');},'Preserved source/history/original Utility/Black/runtime']
])test('full repository rejects '+name,()=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'raeon-full-migration-test-'));
 try{
  const files=JSON.parse(fs.readFileSync(path.join(root,'data/manifests/current-files.json'),'utf8')).files;
  for(const p of files){fs.mkdirSync(path.dirname(path.join(dir,p)),{recursive:true});copyFixtureFile(root,dir,p);}
  mutate(dir);assert.ok(validateFullMigrationRepository(dir).errors.some(x=>x.includes(label)),label);
 }finally{
  assert.equal(path.dirname(path.resolve(dir)),path.resolve(os.tmpdir()));assert.ok(path.basename(dir).startsWith('raeon-full-migration-test-'));
  fs.rmSync(dir,{recursive:true,force:true});
 }
});
