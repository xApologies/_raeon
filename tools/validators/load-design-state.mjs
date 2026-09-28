import fs from 'node:fs';
import path from 'node:path';

export function resolveRepositoryPath(root,relative) {
  if(typeof relative!=='string'||path.isAbsolute(relative)||relative.includes('\\')||relative.split('/').some(x=>['..','.git','_inbox',''].includes(x)))throw Error(`Unsafe repository pointer: ${relative}`);
  return path.join(root,relative);
}
export function loadDesignState(root) {
  const read=p=>JSON.parse(fs.readFileSync(resolveRepositoryPath(root,p),'utf8'));
  const index=read('data/manifests/accepted-state.json');
  if(index.schema_version!==4||index.current_design_checkpoint!=='0004')throw Error('Expected normalized schema 4 checkpoint 0004');
  const state={schema_version:index.schema_version,current_design_checkpoint:index.current_design_checkpoint};
  for(const key of ['authority','source','sources','production','source_import_required','open_items'])state[key]=structuredClone(index[key]);
  const seen=new Set(Object.keys(state));
  for(const [id,pointer]of Object.entries(index.datasets)) {
    const data=read(pointer.path);
    if(!Array.isArray(pointer.keys)||!data.values||JSON.stringify(Object.keys(data.values).sort())!==JSON.stringify([...pointer.keys].sort()))throw Error(`Dataset key mismatch: ${id}`);
    for(const key of pointer.keys){if(seen.has(key)||['__proto__','constructor','prototype'].includes(key))throw Error(`Duplicate/unsafe semantic key: ${key}`);seen.add(key);state[key]=data.values[key];}
  }
  if(!state.utility_structure||state.utility_structure.families)throw Error('Utility overview must not duplicate family datasets');
  state.utility_structure.families={};
  for(const [name,p]of Object.entries(index.utility_families)){
    if(['__proto__','constructor','prototype'].includes(name))throw Error('Unsafe Utility family');
    const family=read(p);if(family.family!==name)throw Error(`Utility family identity mismatch: ${name}`);
    state.utility_structure.families[name]=family.values;
  }
  return state;
}

// Exact governance amendments authorized by the canonical-main cleanup directive.
// Historical manifests retain their original hashes; all other protection is unchanged.
const approvedGovernanceHashes = {
  "PROJECT_CONSTITUTION.md": "36826788906f1490ce37cad2e09780c64035eef948187bd60278fcfb4bb7ca2c",
  "DEVELOPMENT_CONSTITUTION.md": "e8452ff1fc09a16b09dcda01141fa04387064adb37ca1b2ca55194bd801dc21b"
};
export function matchesProtectedHash(file, actual, historical) {
  return actual === (approvedGovernanceHashes[file] ?? historical);
}
