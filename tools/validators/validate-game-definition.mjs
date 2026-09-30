import {validateRuntimeSources} from './genesis-runtime-contract.mjs';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';
import {loadDesignState, resolveRepositoryPath} from './load-design-state.mjs';
import {decisionPath, loadGameDefinitionContract, projectBeforeGameDefinition, projectGameDefinitionFile} from './game-definition-contract.mjs';

export function validateGameDefinition(root) {
  let checks = 0;
  const errors = [];
  const check = (ok, label) => { checks++; if (!ok) errors.push(label); };
  const same = (a, b, label) => check(isDeepStrictEqual(a, b), label);
  const bytes = p => fs.readFileSync(resolveRepositoryPath(root, p));
  const json = p => JSON.parse(bytes(p).toString('utf8'));
  try {
    const contract = loadGameDefinitionContract(root);
    for (const file of Object.keys(contract.json_changes)) {
      projectGameDefinitionFile(root, file, json(file));
      check(true, 'Exact accepted amendments: ' + file);
    }
    projectBeforeGameDefinition(root, loadDesignState(root));
    for (const [file, hash] of Object.entries(contract.preserved_catalog_sha256))
      same(createHash('sha256').update(bytes(file)).digest('hex'), hash, 'Unchanged catalog bytes: ' + file);
    const index = json('data/manifests/accepted-state.json');
    same(index.game_definition_reconciliation, decisionPath, 'Accepted-state decision pointer');
    same(json('data/manifests/authority-map.json').game_definition_reconciliation, decisionPath, 'Authority decision pointer');
    same(index.production.phase, 'PREPRODUCTION', 'Whole-game PREPRODUCTION');
    const match = json('data/game/match.json').values;
    const board = json('data/board/genesis-horizon.json').values;
    const config = json('data/topology/configuration-spaces.json').values;
    const prime = json('data/cycles/cycle_01/primes/working-model.json').values;
    same(match.match_rules.hand_normal_capacity, board.containers.Hand.normal_capacity, 'Hand capacity mirror');
    same(json('data/cycles/cycle_01/utilities/draw_deck.json').values.hand_size_maximum, 7, 'Draw/Hand capacity seven');
    same(board.configuration_region.maximum_active, config.maximum_active_per_player, 'Configuration cap mirror');
    same(board.configuration_region.maximum_additional, config.maximum_additional_per_player, 'Expansion cap mirror');
    same(prime.starting_state, {H:'H_max', C:0, state:'HEALTHY_UNCHARGED'}, 'Normal Prime start');
    for (const [key, value] of Object.entries(match.turn_match_open)) same(value, 'OPEN', 'Retained match OPEN: ' + key);
    same(match.match_rules.refresh_boundary, 'OPEN', 'Refresh boundary OPEN');
    same(prime.friendly_restore.overflow, 'OPEN', 'Prime overflow OPEN');
    same(config.field_runtime.destruction_transaction_order, 'OPEN', 'Destruction ordering OPEN');
    const inventory = json('data/manifests/current-files.json').files;
    check(!inventory.some(p => /RAEON_(?:GIT_UPDATE_PACKAGE|LIVE_DEVELOPMENT_MODEL|LIVE_RULES_MODEL)/.test(p)), 'Transfer archives/trees excluded');
    const runtimeErrors = validateRuntimeSources(root, inventory);
    check(runtimeErrors.length === 0, 'Only exact compiled Genesis sources authorized by runtime build order: ' + runtimeErrors.join('; '));
  } catch (error) { errors.push('Game-definition validation failed: ' + error.message); }
  return {checks, errors};
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const result = validateGameDefinition(path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..'));
  for (const error of result.errors) console.error('FAIL: ' + error);
  console.log(`${result.errors.length ? 'FAIL' : 'PASS'} — ${result.checks} game-definition checks; ${result.errors.length} error(s).`);
  console.log('Scope: accepted design/data amendments and preserved source bytes; no Genesis runtime, mathematical proof or balance claim.');
  if (result.errors.length) process.exitCode = 1;
}
