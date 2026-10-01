"""Lossless, source-locked Cycle-1 queries. Catalog evidence is never live closure."""
import copy
import hashlib
import json
from collections import Counter


def sha(data):
    return hashlib.sha256(data).hexdigest()


class Corpus:
    def __init__(self, root):
        self.root = root
        self.lock = json.loads((root / 'game/qmo/cycle1.lock.json').read_text(encoding='utf8'))
        self.lock_hash = sha((root / 'game/qmo/cycle1.lock.json').read_bytes())
        self.verify()
        self.data = {key: json.loads((root / entry['path']).read_text(encoding='utf8'))
                     for key, entry in self.lock['datasets'].items() if entry['path'].endswith('.json')}
        self.fgs = self.index(self.data['field_generators'], 'card_id')
        self.base = self.index(self.data['base'], 'manifold_id')
        self.qmos = self.index([*self.data['base'], *self.data['fusion'], *self.data['emergent']], 'id')
        self.pairs = {tuple(sorted((r['a_manifold'], r['b_manifold']))): r for r in self.data['pairs']}
        self.compatibility = {tuple(sorted((r['a'], r['b']))): r for r in self.data['compatibility']}
        counts = dict(field_generators=len(self.fgs), base=len(self.base), fusion=len(self.data['fusion']),
                      emergent=len(self.data['emergent']), atlas=len(self.qmos), pairs=len(self.pairs),
                      compatibility=len(self.compatibility))
        if counts != self.lock['counts']:
            raise ValueError('QMO_CORPUS_INTEGRITY')
        for row in self.base.values():
            if any(g not in self.fgs for g in row['generators']):
                raise ValueError('QMO_REFERENCE_INTEGRITY')
        for row in self.pairs.values():
            for field in ('fusion_result_qmo', 'emergent_qmo'):
                if row[field] is not None and row[field] not in self.qmos:
                    raise ValueError('QMO_REFERENCE_INTEGRITY')

    @staticmethod
    def index(records, key):
        result = {record[key]: record for record in records}
        if len(result) != len(records):
            raise ValueError('QMO_DUPLICATE_ID')
        return result

    def verify(self):
        if sha((self.root / 'game/qmo/cycle1.lock.json').read_bytes()) != self.lock_hash:
            raise ValueError('QMO_CORPUS_INTEGRITY')
        for entry in self.lock['datasets'].values():
            target = (self.root / entry['path']).resolve()
            if not target.is_relative_to(self.root.resolve()) or sha(target.read_bytes()) != entry['sha256']:
                raise ValueError('QMO_CORPUS_INTEGRITY')

    def lookup(self, identity):
        self.verify()
        row = self.fgs.get(identity) or self.base.get(identity) or self.qmos.get(identity)
        return copy.deepcopy(row) if row else {'status': 'OPEN', 'reason': 'SOURCE_RECORD_ABSENT'}

    def pair(self, left, right):
        self.verify()
        row = self.pairs.get(tuple(sorted((left, right))))
        return copy.deepcopy(row) if row else {'status': 'OPEN', 'reason': 'SOURCE_PAIR_ABSENT'}

    def candidates(self, handles, budget=60):
        """Exhaustive ordinary whole-membership lookup, preserving multiplicity.

        Subsets/duplicate assignment and fusion require separate accepted contracts.
        The remaining records are never interpreted as a negative on budget expiry.
        """
        self.verify()
        return self.candidates_verified(handles, budget)

    def candidates_verified(self, handles, budget=60):
        """Internal query after this instance's caller verifies the source boundary."""
        if type(budget) is not int or not 0 <= budget <= 60 or len(handles) > 120:
            raise ValueError('QUERY_BUDGET')
        members = Counter(handles)
        rows = sorted(self.base.values(), key=lambda row: row['id'])
        matches = [copy.deepcopy(row) for row in rows[:budget] if Counter(row['generators']) == members]
        complete = budget == len(rows)
        return {'candidates': matches, 'complete_search': complete, 'examined': budget,
                'total_candidates': len(rows), 'membership': 'MATCH' if matches else
                ('UNRESOLVED' if not complete or any(n > 1 for n in members.values()) else 'NO_MATCH'),
                'subset_policy': 'OPEN', 'duplicate_policy': 'OPEN',
                'pose_closure': 'UNRESOLVED' if complete else 'BUDGET_EXHAUSTED',
                'permission': 'POLICY_GATED', 'effect': 'OBSERVED', 'witness': None}

    def potential_edges(self, copies, limit=128):
        """Catalog correspondences only: no transformed face/contact claim."""
        result, total = [], 0
        ordered = sorted(copies.items())
        for index, (a, left) in enumerate(ordered):
            for b, right in ordered[index + 1:]:
                row = self.compatibility.get(tuple(sorted((left, right))))
                if row is None:
                    continue
                total += 1
                if len(result) < limit:
                    reverse = row['a'] != left
                    result.append({'a': a, 'b': b, 'source_pair': [row['a'], row['b']],
                        'faces': [{'a_face': m['b_face' if reverse else 'a_face'],
                                   'b_face': m['a_face' if reverse else 'b_face']} for m in row['matches']],
                        'status': 'CATALOG_POTENTIAL', 'live_pose': 'UNRESOLVED'})
        return {'edges': result, 'total': total, 'complete': total <= limit,
                'authoritative_live_edges': [], 'reason': 'G-POSE'}
