import {matchesRuntimeNavigation} from './genesis-runtime-contract.mjs';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';
import {resolveRepositoryPath} from './load-design-state.mjs';

export const decisionPath = 'provenance/decisions/game-definition-2026-09-30.json';
export const decisionHash = '0fb95919f320247b79505217b5c9c017209fc9e4d28f50d648dbceed224e94dd';
export function loadGameDefinitionContract(root) {
  const bytes = fs.readFileSync(resolveRepositoryPath(root, decisionPath));
  if (createHash('sha256').update(bytes).digest('hex') !== decisionHash)
    throw Error('Reviewed game-definition amendment changed without explicit acceptance');
  return JSON.parse(bytes.toString('utf8'));
}

// Verify every amended current value before projecting it to historical authority.
// Unrelated values are deliberately untouched so earlier validators still reject drift.
export function reverseAmendments(value, changes) {
  const projected = structuredClone(value);
  for (const change of changes) {
    let parent = projected;
    for (const part of change.path.slice(0, -1)) parent = parent?.[part];
    const key = change.path.at(-1);
    if (!parent || (change.after_absent ? Object.hasOwn(parent, key)
      : !Object.hasOwn(parent, key) || !isDeepStrictEqual(parent[key], change.after)))
      throw Error('Unapproved game-definition semantic value: ' + change.path.join('.'));
    if (change.before_absent) delete parent[key];
    else parent[key] = structuredClone(change.before);
  }
  return projected;
}
export function projectBeforeGameDefinition(root, state) {
  return reverseAmendments(state, loadGameDefinitionContract(root).semantic_changes);
}
export function projectGameDefinitionFile(root, file, value) {
  return reverseAmendments(value, loadGameDefinitionContract(root).json_changes[file] ?? []);
}
export function projectGameDefinitionText(root, file, text) {
  for (const change of loadGameDefinitionContract(root).text_changes[file] ?? []) {
    if (!text.includes(change.after) || text.includes(change.before))
      throw Error('Unapproved game-definition prose amendment: ' + file);
    text = text.replace(change.after, change.before);
  }
  return text;
}
export function matchesGameDefinitionAmendment(root, file, actualHash, priorHash) {
  const entry = loadGameDefinitionContract(root).approved_file_amendments[file];
  return (entry?.before_sha256 === priorHash && entry?.after_sha256 === actualHash) || matchesRuntimeNavigation(file, actualHash, priorHash);
}
