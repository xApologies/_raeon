"""Faithful indexing of existing ordinary identities; no mathematical generation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def build_catalog(root):
    root = Path(root)
    sources, records = {}, {}

    def read(relative):
        path = root / relative
        sources[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        return json.loads(path.read_text(encoding='utf8'))

    system = read('data/cycles/cycle_01/card-system.json')['values']['cycle_01']
    copy_limits = {'Field Generator': system['normal_copy_limits']['field_generator'],
                   'Utility': system['normal_copy_limits']['utility'],
                   'Prime': read('data/cycles/cycle_01/primes/status.json')['copy_limit']}

    def add(path, pointer, value, category, key=None, status=None):
        handle = key or 'source:' + path + '#' + pointer
        if handle in records:
            raise ValueError('duplicate catalog handle')
        records[handle] = {'handle': handle, 'category': category,
                           'source': path, 'pointer': pointer,
                           'source_sha256': sources[path], 'record': value,
                           'record_sha256': hashlib.sha256(canonical(value)).hexdigest(),
                           'printed_id': value.get('card_id', 'OPEN') if isinstance(value, dict) else 'OPEN',
                           'copy_limit': copy_limits[category],
                           'source_status': status or 'SOURCE_BACKED'}

    path = 'data/cycles/cycle_01/field_generators/objects.json'
    for i, value in enumerate(read(path)):
        add(path, '/' + str(i), value, 'Field Generator', value['card_id'], value['status'])
    path = 'data/cycles/cycle_01/primes/status.json'
    data = read(path)
    for i, value in enumerate(data['objects']):
        add(path, '/objects/' + str(i), value, 'Prime', status=data['status'])
    for family in ['transduction', 'activation', 'sandbox_activation', 'draw_deck', 'recovery', 'stability', 'restore_prime']:
        path = 'data/cycles/cycle_01/utilities/' + family + '.json'
        data = read(path)
        if family == 'restore_prime':
            add(path, '', data, 'Utility', status=data['status'])
        elif family == 'transduction':
            for direction in ['restore', 'degrade', 'universal']:
                for i, value in enumerate(data['values'][direction]):
                    add(path, '/values/' + direction + '/' + str(i), value, 'Utility')
        elif 'ranks' in data['values']:
            for i, value in enumerate(data['values']['ranks']):
                add(path, '/values/ranks/' + str(i), value, 'Utility')
        else:
            for i, value in enumerate(data['values']['slots']):
                add(path, '/values/slots/' + str(i), value, 'Utility', status=value.get('working_rank', {}).get('authority', 'OPEN'))
    counts = {k: sum(r['category'] == k for r in records.values()) for k in ['Field Generator', 'Prime', 'Utility']}
    assert counts == {'Field Generator': 120, 'Prime': 14, 'Utility': 51}, counts
    return {'schema': 1, 'kind': 'SOURCE_INDEX_NOT_NEW_CARD_AUTHORITY', 'sources': sources,
            'counts': counts, 'records': records}


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    target = root / 'game/core/raeon/application/catalog.json'
    target.write_text(json.dumps(build_catalog(root), indent=2, ensure_ascii=False) + '\n', encoding='utf8', newline='\n')
