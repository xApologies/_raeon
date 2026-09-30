import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';

export const pass02Decision = 'provenance/decisions/raeon-pass-02.json';
const acceptedDecisionHash = '11f7fa04775cc591ccde7ad968d0575ca05be25c3cb3fd31bb2718f9eb41d5ee';
const hash = bytes => createHash('sha256').update(bytes).digest('hex');

export function pass02Sources(root, inventory) {
  if (!inventory.includes(pass02Decision)) return {};
  const bytes = fs.readFileSync(path.join(root, pass02Decision));
  if (hash(bytes) !== acceptedDecisionHash) throw new Error('Pass-2 decision hash mismatch');
  const decision = JSON.parse(bytes);
  for (const [file, expected] of Object.entries(decision.package_files)) {
    if (!file.startsWith('game/core/raeon/application/')) throw new Error('Pass-2 package path outside application');
    if (hash(fs.readFileSync(path.join(root, file))) !== expected) throw new Error('Pass-2 package integrity: ' + file);
  }
  for (const [file, expected] of Object.entries(decision.source_inputs)) {
    if (hash(fs.readFileSync(path.join(root, file))) !== expected) throw new Error('Pass-2 source input integrity: ' + file);
  }
  return decision.compiled_sources;
}
