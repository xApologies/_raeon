import {matchesPass05} from './pass-05-contract.mjs';
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';

export const pass04Decision = 'provenance/decisions/raeon-pass-04.json';
const acceptedDecisionHash = '59a63059ab3c36baf0f30ae1dae48762bdc126fc5b469366fb14a384d0b0e290';
const hash = value => createHash('sha256').update(value).digest('hex');

export function pass04(root) {
  const location = path.join(root, pass04Decision);
  if (!fs.existsSync(location)) return null;
  const bytes = fs.readFileSync(location);
  if (hash(bytes) !== acceptedDecisionHash) throw new Error('Pass-4 amendment integrity');
  const decision = JSON.parse(bytes);
  if (decision.starting_sha !== 'd644a361aa2ce788a1da991b15e3b8e3be5c7cba' ||
      decision.whole_game_phase !== 'PREPRODUCTION') throw new Error('Pass-4 lineage or maturity drift');
  for (const [file, expected] of Object.entries({...decision.sources, ...decision.preserved_tests, ...decision.qmo_sources})) {
    const actual = hash(fs.readFileSync(path.join(root, file)));
    if (actual !== expected && !matchesPass05(root,file,actual,expected)) throw new Error('Pass-4 source integrity: ' + file);
  }
  for (const [file, entry] of Object.entries(decision.changes)) {
    const actual = hash(fs.readFileSync(path.join(root, file)));
    if (actual !== entry.after_sha256 && !matchesPass05(root,file,actual,entry.after_sha256)) throw new Error('Pass-4 changed source integrity: ' + file);
  }
  return decision;
}

export function matchesPass04(root, file, actual, historical) {
  const entry = pass04(root)?.changes[file];
  return Boolean(entry && entry.before_sha256 === historical && (entry.after_sha256 === actual || matchesPass05(root,file,actual,entry.after_sha256))) || matchesPass05(root,file,actual,historical);
}

export function pass04Sources(root, inventory, prior) {
  if (!inventory.includes(pass04Decision)) return prior;
  const decision = pass04(root);
  if (!decision) throw new Error('Missing Pass-4 amendment');
  const result = {...prior};
  for (const [file, entry] of Object.entries(decision.compiled_sources)) {
    if (file in prior && decision.changes[file]?.before_sha256 !== prior[file].source_sha256)
      throw new Error('Pass-4 compilation predecessor mismatch');
    result[file] = entry;
  }
  return result;
}
