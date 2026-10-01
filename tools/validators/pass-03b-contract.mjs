import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';

export const pass03bDecision = 'provenance/decisions/raeon-pass-03b.json';
const acceptedDecisionHash = '38fb9b2e9e9b2490b21152ee5342c5c1f0bdb44bcc0bc820fb559c4c96bdbd24';
const hash = bytes => createHash('sha256').update(bytes).digest('hex');

export function pass03b(root) {
  const file = path.join(root, pass03bDecision);
  if (!fs.existsSync(file)) return null;
  const bytes = fs.readFileSync(file);
  if (hash(bytes) !== acceptedDecisionHash) throw new Error('Pass-3B amendment integrity');
  const decision = JSON.parse(bytes);
  for (const [relative, expected] of Object.entries({...decision.sources, ...decision.preserved_tests})) {
    if (hash(fs.readFileSync(path.join(root, relative))) !== expected) throw new Error('Pass-3B source integrity: ' + relative);
  }
  for (const [relative, entry] of Object.entries(decision.changes)) {
    if (hash(fs.readFileSync(path.join(root, relative))) !== entry.after_sha256) throw new Error('Pass-3B changed source integrity: ' + relative);
  }
  return decision;
}

export function matchesPass03b(root, file, actual, historical) {
  const entry = pass03b(root)?.changes[file];
  return Boolean(entry && entry.before_sha256 === historical && entry.after_sha256 === actual);
}

export function pass03bSources(root, inventory, prior) {
  if (!inventory.includes(pass03bDecision)) return prior;
  const decision = pass03b(root);
  if (!decision) throw new Error('Missing Pass-3B amendment');
  const result = {...prior};
  for (const [file, entry] of Object.entries(decision.compiled_sources)) {
    if (file in prior && decision.changes[file]?.before_sha256 !== prior[file].source_sha256)
      throw new Error('Pass-3B compilation amendment has a different predecessor');
    result[file] = entry;
  }
  return result;
}
