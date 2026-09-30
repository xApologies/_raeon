import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';

export const passDecision = 'provenance/decisions/raeon-pass-01.json';
const acceptedDecisionHash = '2b6867217a47c5a82de8b42fbc06f245d28d26dfa14fda943ed55c695294c317';
const hash = bytes => createHash('sha256').update(bytes).digest('hex');

export function pass01Sources(root, inventory) {
  if (!inventory.some(p => p.startsWith('game/core/raeon/application/'))) return {};
  const bytes = fs.readFileSync(path.join(root, passDecision));
  if (hash(bytes) !== acceptedDecisionHash) throw new Error('Pass-1 decision hash mismatch');
  const decision = JSON.parse(bytes);
  for (const [file, expected] of Object.entries(decision.package_files)) {
    if (!file.startsWith('game/core/raeon/application/')) throw new Error('Pass-1 package path outside authorized home');
    if (hash(fs.readFileSync(path.join(root, file))) !== expected) throw new Error('Pass-1 package integrity: ' + file);
  }
  return decision.compiled_sources;
}
