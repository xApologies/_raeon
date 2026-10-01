import {matchesPass03b} from './pass-03b-contract.mjs';
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';

export const pass03Decision = 'provenance/decisions/raeon-pass-03.json';
const acceptedDecisionHash = '5b335817588b8c372fdc70fb3a88053e28eea0c3334d609cb96ec823eb64ebe2';
const hash = value => createHash('sha256').update(value).digest('hex');

export function pass03(root) {
  const file = path.join(root, pass03Decision);
  if (!fs.existsSync(file)) return null;
  const bytes = fs.readFileSync(file);
  if (hash(bytes) !== acceptedDecisionHash) throw new Error('Pass-3 amendment integrity');
  const decision = JSON.parse(bytes);
  for (const [relative, expected] of Object.entries(decision.sources)) {
    const actual = hash(fs.readFileSync(path.join(root, relative)));
    if (actual !== expected && !matchesPass03b(root, relative, actual, expected)) throw new Error('Pass-3 source integrity: ' + relative);
  }
  for (const [relative, entry] of Object.entries(decision.changes)) {
    const actual = hash(fs.readFileSync(path.join(root, relative)));
    if (actual !== entry.after_sha256 && !matchesPass03b(root, relative, actual, entry.after_sha256)) throw new Error('Pass-3 changed source integrity: ' + relative);
  }
  return decision;
}

export function matchesPass03(root, file, actual, historical) {
  const entry = pass03(root)?.changes[file];
  return Boolean(entry && entry.before_sha256 === historical && (entry.after_sha256 === actual || matchesPass03b(root, file, actual, entry.after_sha256)));
}

export function pass03Sources(root, inventory, prior) {
  if (!inventory.includes(pass03Decision)) return prior;
  const decision = pass03(root);
  if (!decision) throw new Error('Missing Pass-3 amendment');
  const result = {...prior};
  for (const [file, entry] of Object.entries(decision.compiled_sources)) {
    if (file in prior && decision.changes[file]?.before_sha256 !== prior[file].source_sha256)
      throw new Error('Pass-3 compilation amendment has a different predecessor');
    result[file] = entry;
  }
  return result;
}
