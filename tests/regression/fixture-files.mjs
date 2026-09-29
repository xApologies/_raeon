import fs from 'node:fs';
import path from 'node:path';
export function copyFixtureFile(root,dir,file) {
 const source=path.join(root,file),target=path.join(dir,file);
 if(file.endsWith('/raeon_FULL_exhaustive_migration_2026-09-29.zip')) {
  fs.writeFileSync(target,'version https://git-lfs.github.com/spec/v1\noid sha256:48d6ca53999cc06a27e309f3f51d4ba6cb5ed3ed65592781c6a21b5dfbb1d958\nsize 242064399\n');
 } else if(file.endsWith('/GENESIS_PROPAGATION_FULL_CONTINUITY_v8.zip')) {
  // A valid LFS checkout may intentionally contain a pointer. Avoid copying 234 MB per fixture.
  fs.writeFileSync(target,'version https://git-lfs.github.com/spec/v1\noid sha256:4ecef0cc37f61292403311078426674ff874e4f4d1814a8ed468d59d0e62eae6\nsize 233685828\n');
 } else fs.copyFileSync(source,target);
}
