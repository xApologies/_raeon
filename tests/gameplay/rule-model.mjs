// Specification example model only. No Genesis source, scheduler, QMO solver or game runtime.
// Admission inputs are explicit test premises, never a claim to have proved mathematics.
import fs from 'node:fs';
const read = file => JSON.parse(fs.readFileSync(new URL('../../' + file, import.meta.url), 'utf8')).values;
export const rules = {
  match: read('data/game/match.json'),
  board: read('data/board/genesis-horizon.json'),
  configuration: read('data/topology/configuration-spaces.json'),
  prime: read('data/cycles/cycle_01/primes/working-model.json'),
  relationships: read('data/topology/relationships.json'),
};
const colors = ['Red','Orange','Yellow','Green','Blue','Violet','White'];
export function primeState(p) {
  if (!Number.isInteger(p.rank) || p.rank < 1 || p.rank > 7 ||
      !Number.isInteger(p.H) || !Number.isInteger(p.C) ||
      p.H < 0 || p.H > p.rank || p.C < 0 || p.C > p.rank || (p.H === 0 && p.C !== 0))
    throw Error('Invalid ordinary Prime state');
  if (p.H === 0) return 'INACTIVE';
  if (p.H < p.rank) return 'DAMAGED_NON_OPERATIONAL';
  return p.C === 0 ? 'HEALTHY_UNCHARGED' : 'OPERATIONAL_CHARGED';
}
export function startPrime(entry, id, slot) {
  if (rules.prime.starting_state.H !== 'H_max') throw Error('Unknown start semantics');
  return {id, slot, family:entry.family, rank:entry.rank_value, H:entry.rank_value, C:rules.prime.starting_state.C};
}
function magnitude(amount) {
  if (!Number.isInteger(amount) || amount < 0) throw Error('Invalid magnitude');
}
export function restorePrime(p, amount) {
  magnitude(amount);
  if (primeState(p) === 'INACTIVE') return {status:'EXPLICIT_REACTIVATION_REQUIRED', value:p};
  const heal = Math.min(amount, p.rank - p.H);
  const charge = Math.min(amount - heal, p.rank - p.C);
  if (amount > heal + charge) return {status:'OPEN_OVERFLOW', value:p};
  return {status:'VALID_EXAMPLE', value:{...p,H:p.H+heal,C:p.C+charge}};
}
export function degradePrime(p, amount) {
  magnitude(amount); primeState(p);
  const shieldLoss = Math.min(amount, p.C);
  return {...p, C:p.C-shieldLoss, H:p.H-Math.min(amount-shieldLoss,p.H)};
}
export function reactivatePrime(p) {
  if (primeState(p) !== 'INACTIVE') throw Error('Reactivation requires INACTIVE');
  return {...p, ...rules.prime.reactivation.to};
}
export function spendPrime(p, amount, direction, window, side, targetAndTimingAdmitted) {
  magnitude(amount);
  const allowed = primeState(p) === rules.prime.spend.requires_state && amount > 0 && amount <= p.C &&
    rules.prime.spend[p.family]?.includes(direction) &&
    rules.match.match_rules.authority_windows[window]?.[direction] === side;
  if (!allowed) return {status:'REJECTED', value:p};
  if (!targetAndTimingAdmitted) return {status:'OPEN_ADMISSION', value:p};
  return {status:'VALID_EXAMPLE', value:{...p,C:p.C-amount}};
}
export function moveCard(source, destination, id, destinationName, admitted) {
  const card = source.find(c => c.id === id);
  const capacity = destinationName === 'Hand' ? rules.board.containers.Hand.normal_capacity : Infinity;
  const ids = [...source,...destination].map(c => c.id);
  if (!admitted || !card || card.kind !== 'CARD_GEOMETRIC' ||
      [...source,...destination].some(c => c.kind !== 'CARD_GEOMETRIC') ||
      new Set(ids).size !== ids.length || destination.length >= capacity)
    return {status:'REJECTED', source, destination};
  return {status:'VALID_EXAMPLE', source:source.filter(c => c.id !== id), destination:[...destination,card]};
}
export function canAttachSpace(active, additional, admitted) {
  return admitted && Number.isInteger(active) && Number.isInteger(additional) && active >= 0 && additional >= 0 &&
    additional <= active && active < rules.configuration.maximum_active_per_player &&
    additional < rules.configuration.maximum_additional_per_player;
}
export function resolveExample(fgCount, membershipResult, poseResult, qmoId) {
  if (fgCount === 0) return {state:'EMPTY',qmo:null};
  return membershipResult === 'VALID' && poseResult === 'VALID' && qmoId
    ? {state:'RESOLVED',qmo:qmoId} : {state:'CONFIGURING',qmo:null};
}
export function useField(field) {
  if (field.state !== 'RESOLVED' || field.availability !== 'READY' || field.current <= 0)
    return {status:'REJECTED',value:field};
  return {status:'VALID_EXAMPLE',output:field.current,value:{...field,availability:'USED'}};
}
export function endActive(field) {
  if (rules.match.match_rules.active_end_refreshes_fields) throw Error('Unaccepted refresh rule');
  return field;
}
export function changeFieldColor(field, delta) {
  if (!Number.isInteger(delta)) throw Error('Invalid color delta');
  const current = Math.max(0, Math.min(field.native, field.current + delta));
  if (current === 0) return {status:'DESTRUCTION_REQUIRED',qmo:field.qmo,
    supportIds:field.supportIds,destination:rules.configuration.field_runtime.destroyed_supporting_fg_destination,
    ordering:rules.configuration.field_runtime.destruction_transaction_order,activeFieldExposed:false};
  return {status:'VALID_EXAMPLE',value:{...field,current}};
}
export function liveEmergents(activeSupportIds, admittedEdges) {
  const active = new Set(activeSupportIds);
  return admittedEdges.filter(e => e.supports.length === 2 && e.supports.every(s => active.has(s)));
}
export const colorRank = color => colors.indexOf(color) + 1;

export function mergeExample(left, right, admitted) {
  const combined = [...left, ...right];
  if (!admitted || new Set(combined.map(x => x.id)).size !== combined.length)
    return {status:'REJECTED',left,right};
  return {status:'VALID_EXAMPLE',contents:combined,independentSpaces:rules.relationships.merge.independent_spaces_after};
}
