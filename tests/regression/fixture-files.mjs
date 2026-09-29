import fs from 'node:fs';
import path from 'node:path';
export function copyFixtureFile(root,dir,file) {
 const source=path.join(root,file),target=path.join(dir,file);
 if(file.endsWith('/GENESIS_PROPAGATION_FULL_CONTINUITY_v8.zip')) {
  // A valid LFS checkout may intentionally contain a pointer. Avoid copying 234 MB per fixture.
  fs.writeFileSync(target,'version https://git-lfs.github.com/spec/v1\noid sha256:4ecef0cc37f61292403311078426674ff874e4f4d1814a8ed468d59d0e62eae6\nsize 233685828\n');
 } else fs.copyFileSync(source,target);
}
