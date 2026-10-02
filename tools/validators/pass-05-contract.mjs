import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';

export const pass05Decision = 'provenance/decisions/raeon-pass-05.json';
const acceptedDecisionHash = '5ea484b3f393c3528df618c836c0cf9ac7b5ec85ab6d9ff6e37b4de2ee49d1f4';
const hash = value => createHash('sha256').update(value).digest('hex');

function declaration(root) {
  const location = path.join(root, pass05Decision);
  if (!fs.existsSync(location)) return null;
  const bytes = fs.readFileSync(location);
  if (hash(bytes) !== acceptedDecisionHash) throw new Error('Pass-5 amendment integrity');
  const decision = JSON.parse(bytes);
  if (decision.starting_sha !== '63771ab37dfec9a0c9de907c60f6f8b2f7a3f670' ||
      decision.whole_game_phase !== 'PREPRODUCTION' || decision.open_items.length !== 16)
    throw new Error('Pass-5 lineage, maturity or OPEN authority drift');
  return decision;
}

export function pass05(root) {
  const decision = declaration(root);
  if (!decision) return null;
  for (const [file, expected] of Object.entries({...decision.sources, ...decision.preserved_tests,
      ...decision.qmo_sources, ...decision.sealed_receipts})) {
    if (hash(fs.readFileSync(path.join(root,file))) !== expected) throw new Error('Pass-5 source integrity: '+file);
  }
  for (const [file, entry] of Object.entries(decision.changes)) {
    if (hash(fs.readFileSync(path.join(root,file))) !== entry.after_sha256) throw new Error('Pass-5 changed source integrity: '+file);
  }
  return decision;
}

export function matchesPass05(root,file,actual,historical) {
  // The caller already hashed this file. Match exactly the authenticated
  // amendment for it; the full new source set is checked by pass05Sources.
  const entry = declaration(root)?.changes[file];
  return Boolean(entry && entry.before_sha256 === historical && entry.after_sha256 === actual);
}

export function projectPass05File(root,file,value) {
  const expected = declaration(root)?.historical_metadata[file];
  if (!expected) return value;
  if (!isDeepStrictEqual(value.effective_authority,expected)) throw new Error('Pass-5 authority pointer drift: '+file);
  const prior = structuredClone(value);
  delete prior.effective_authority;
  return prior;
}

export function pass05Sources(root,inventory,prior) {
  if (!inventory.includes(pass05Decision)) return prior;
  const decision = pass05(root);
  if (!decision) throw new Error('Missing Pass-5 amendment');
  const result = {...prior};
  for (const [file,entry] of Object.entries(decision.compiled_sources)) {
    if (file in prior) throw new Error('Pass-5 cannot replace an inherited Genesis source');
    result[file] = entry;
  }
  return result;
}
