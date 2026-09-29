import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {resolveRepositoryPath} from '../validators/load-design-state.mjs';

export const repositoryRoot=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
// Read-only catalog lookup. No generation, admission inference or runtime effects.
export function queryCycle1(root,kind,...ids) {
  const read=p=>fs.readFileSync(resolveRepositoryPath(root,p),'utf8');
  const json=p=>JSON.parse(read(p));
  const manifest=json('data/manifests/cycle1-source-import.json');
  const data=k=>json(manifest.datasets[k]);
  const missing=()=>({status:'OPEN',reason:'No supplied catalog record; missing data is not TERMINATES.'});
  if(kind==='counts')return manifest.counts;
  if(kind==='fg')return data('field_generators').find(x=>x.card_id===ids[0]||x.id===ids[0])??missing();
  if(kind==='base')return data('base').find(x=>x.manifold_id===ids[0]||x.id===ids[0])??missing();
  if(kind==='qmo')return [...data('field_generators'),...data('base'),...data('derived')].find(x=>x.id===ids[0])??missing();
  if(kind==='pair')return data('pairs').find(x=>[x.a_manifold,x.b_manifold].sort().join('|')===[...ids].sort().join('|'))??missing();
  if(kind==='atlas')return data('atlas');
  if(kind==='render') {
    const row=data('render_catalog').find(x=>x.manifold_id===ids[0]||x.qmo_address===ids[0]);
    if(!row)return missing();
    const {source_prefix,repository_prefix}=manifest.render_source_path_mapping;
    if(!row.render_spec.startsWith(source_prefix))throw Error('Unknown render path mapping');
    // Return original JSON text: deterministic_seed can exceed JS safe integers.
    return read(repository_prefix+row.render_spec.slice(source_prefix.length));
  }
  throw Error('Usage: node tools/qmo/query-cycle1.mjs counts|fg ID|base ID|qmo ADDRESS|pair M-A M-B|atlas|render M-ID');
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  try {
    const value=queryCycle1(repositoryRoot,...process.argv.slice(2));
    process.stdout.write(typeof value==='string'?value:JSON.stringify(value,null,2)+'\n');
  } catch(error) {console.error(error.message);process.exitCode=1;}
}
