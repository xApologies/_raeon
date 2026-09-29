import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';
import {resolveRepositoryPath} from './load-design-state.mjs';

export const contractPath='provenance/audits/full-migration-2026-09-29-semantic-changes.json';
export const contractHash='2ad4771042ddf84c97f9a35a52eed40123aeb349c1478b35eb6c64f99bb6fd6f';
export function loadFullMigrationContract(root) {
 const bytes=fs.readFileSync(resolveRepositoryPath(root,contractPath));
 if(createHash('sha256').update(bytes).digest('hex')!==contractHash)throw Error('Reviewed full-migration contract changed without an explicit amendment');
 return JSON.parse(bytes.toString('utf8'));
}
export function projectBeforeFullMigration(root,state) {
 const projected=structuredClone(state);
 for(const change of loadFullMigrationContract(root).semantic_changes){
  let parent=projected;
  for(const part of change.path.slice(0,-1))parent=parent[part];
  const key=change.path.at(-1);
  if(!isDeepStrictEqual(parent[key],change.after))throw Error('Unapproved full-migration semantic value: '+change.path.join('.'));
  if(change.before_absent)delete parent[key];else parent[key]=structuredClone(change.before);
 }
 return projected;
}
