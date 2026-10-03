import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';

export const pass06Decision = 'provenance/decisions/raeon-pass-06.json';
const acceptedDecisionHash = '6a6298211ced90801c2fc7fa05d03a15c097e73ba4b80f169319bfec0f391d4d';
const hash = value => createHash('sha256').update(value).digest('hex');
// Exact reviewed pairs also support sealed predecessor validators operating on
// minimal copied fixtures. This is no general permission for successor edits.
const approvedAmendments = {"AGENTS.md":{"after_sha256":"88ebe1791c2a6aef80fab13cbde0eccb6ba60e371765837915c1e01f2f57e53b","before_sha256":"6e268c0a86d491fa2ebf96f6a9c786c17479c64432f6d9dd8fa6ee4e2fe73400"},"game/core/genesis_horizon/bindings/python/src/raeon_genesis_horizon/adapter.py":{"after_sha256":"892c99d0b7b45b29dde8fe5406bb10cd32dc485c28538b52a23554a2ad471db7","before_sha256":"506214e62be06ae521f8970ef0582ee7c80087778dde30c2d6a4491dfcb8f7ed"},"game/core/genesis_horizon/bindings/python/src/raeon_genesis_horizon/native.py":{"after_sha256":"4d01b6b2f848928ecdd9d9573de2c82e4f2266e9fb2ff291c2179b3072431ed3","before_sha256":"1b91acb7f3106e5cfdea610ca0b8032ef7951b28d87e2a1178d1d5cbf3c575f3"},"game/core/raeon/application/manifest.json":{"after_sha256":"eb9de82343dba530a739284c0a649acbe8b2c281696ddf5509cd23e92a9629d1","before_sha256":"cfaae1587e6b2632b0e3f013a71225d7b83bf2fb8e59b782b45cb3b18204c9d7"},"game/match/state.py":{"after_sha256":"2017e0229f348b93e924002049c2e1781f6a5f611d7422c86e14c957e3ad80df","before_sha256":"0fd5883e6e998e74487ff6d6f406dfc5c18f2f92294ac260d06a1cd62197d210"},"game/sandbox/topology.py":{"after_sha256":"aba6b97d5233188fb2e8d4740a1c48a5f88e35583ccb1c7a61e2620f7982983b","before_sha256":"8f4364c735b342cf54eaeb6380b73cb5976d586b95e35fecab7e35475f07543b"},"tools/genesis_runtime.py":{"after_sha256":"f3deecb559452562803b0bff62a3e01f82f698742edb651950e42587f3b94d81","before_sha256":"c9674b44df3d83f2d7ab086b57d4b1df3d2bc0d16e3b41b0a08d3ffaae8241df"},"tools/genesis_runtime_distribution.py":{"after_sha256":"5a896901251612106d64ed0415898cd37e7d9e94abc0937f3b17c70228f126cb","before_sha256":"0c9d8b91ab25f8a80251051bf4a021032df7e7ab3665386bf46179096ac0cba1"},"tools/genesis_runtime_pass05.py":{"after_sha256":"fc817448f95ec85b1ce857858446c8e9ceddb76628d42d3edde9db5d636a24ee","before_sha256":"2999b056c7b7bee641c6fa3b949a7de6fac339915f52b4a5df3e57bd6d2051d8"},"tools/validators/genesis-runtime-contract.mjs":{"after_sha256":"42f705767b91726299454355c508ce9aa6b5bc0a022ffbfc201a853a189015a6","before_sha256":"3cdac36ff046d90458df8c52dbf1f80f3a95d36de59128188fe77fe266377b96"},"tools/validators/pass-05-contract.mjs":{"after_sha256":"2bc05d8d19cae34ed537f9fc5af51f80c8622b3683c36bb3a5b1dc9224cffd49","before_sha256":"88ab38c91e374a94eb62d07d90f5ecc4b6a83a1716fe397b93d9970505fa6584"}};

function declaration(root) {
  const location = path.join(root,pass06Decision);
  if (!fs.existsSync(location)) return null;
  const bytes=fs.readFileSync(location);
  if (hash(bytes)!==acceptedDecisionHash) throw new Error('Pass-6 amendment integrity');
  const decision=JSON.parse(bytes);
  if (decision.starting_sha!=='388a241ba5674c157131601aad677ab52350f2c6' ||
      decision.whole_game_phase!=='PREPRODUCTION' || decision.open_items.length!==12)
    throw new Error('Pass-6 lineage, maturity or OPEN authority drift');
  return decision;
}

export function matchesPass06(root,file,actual,historical) {
  const entry=(declaration(root)?.changes ?? approvedAmendments)[file];
  return Boolean(entry && entry.before_sha256===historical && entry.after_sha256===actual);
}

export function pass06(root) {
  const decision=declaration(root);
  if (!decision) return null;
  for (const [file,expected] of Object.entries({...decision.sources,...decision.preserved_tests,...decision.qmo_sources,...decision.sealed_receipts}))
    if (hash(fs.readFileSync(path.join(root,file)))!==expected) throw new Error('Pass-6 source integrity: '+file);
  for (const [file,entry] of Object.entries(decision.changes))
    if (hash(fs.readFileSync(path.join(root,file)))!==entry.after_sha256) throw new Error('Pass-6 changed source integrity: '+file);
  return decision;
}

export function pass06Sources(root,inventory,prior) {
  if (!inventory.includes(pass06Decision)) return prior;
  const decision=pass06(root);const result={...prior};
  for (const [file,entry] of Object.entries(decision.compiled_sources)) {
    if (file in prior) throw new Error('Pass-6 cannot replace an inherited Genesis source');
    result[file]=entry;
  }
  return result;
}
