import {pass03bSources} from './pass-03b-contract.mjs';
import {pass03Sources} from './pass-03-contract.mjs';
import {pass02Sources} from './pass-02-contract.mjs';
import {pass01Sources} from './pass-01-contract.mjs';
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';

export const runtimeDecision = 'provenance/decisions/genesis-runtime-build.json';
// Updated only with a reviewed exact-source amendment, never inferred from file extensions.
const acceptedDecisionHash = '18bb9f0ccb3ba792c7234dbe8b8ceea5f29f31a8bd7e3733075adf2962b600ca';
const hash = bytes => createHash('sha256').update(bytes).digest('hex');

export function validateRuntimeSources(root, inventory) {
  const sources = inventory.filter(p => p.endsWith('.gen')).sort();
  if (sources.length === 0) return [];
  const errors = [];
  try {
    const bytes = fs.readFileSync(path.join(root, runtimeDecision));
    if (hash(bytes) !== acceptedDecisionHash) throw new Error('runtime decision hash mismatch');
    const decision = JSON.parse(bytes);
    const original = {...decision.compiled_sources, ...pass01Sources(root, inventory)};
    const additions = pass02Sources(root, inventory);
    for (const file of Object.keys(additions)) if (file in original) throw new Error('Pass-2 cannot override earlier compiled source authority');
    const compiled = pass03bSources(root, inventory, pass03Sources(root, inventory, {...original, ...additions}));
    if (JSON.stringify(sources) !== JSON.stringify(Object.keys(compiled).sort()))
      errors.push('Executable Genesis inventory differs from the exact authorized source set');
    for (const [source, evidence] of Object.entries(compiled)) {
      if (!source.startsWith('game/core/genesis_horizon/src/') && !source.startsWith('tests/integration/genesis_horizon/application/') && !source.startsWith('game/core/raeon/application/') && !source.startsWith('tests/integration/genesis_horizon/pass_01_application/'))
        throw new Error('Executable source outside authorized implementation/test homes');
      if (hash(fs.readFileSync(path.join(root, source))) !== evidence.source_sha256)
        errors.push('Executable Genesis source changed without compilation amendment: ' + source);
      if (!/^[a-f0-9]{64}$/.test(evidence.bytecode_sha256)) errors.push('Missing compiled bytecode identity: ' + source);
    }
  } catch (error) { errors.push('Genesis source contract: ' + error.message); }
  return errors;
}

// Exact navigation amendment: exposes tested generic runtime, preserves game gates.
const navigationAmendments = {
  'game/core/README.md': {before: 'b160d475b108a6edac295e76dada06ac36037e5c771ff20168574b63119e3562', after: 'f24c2020fe41df0e889f093dcbd8e19424fd3931d273897641ce048376885a44'}
};
export function matchesRuntimeNavigation(file, actual, historical) {
  const entry = navigationAmendments[file];
  return Boolean(entry && entry.before === historical && entry.after === actual);
}
