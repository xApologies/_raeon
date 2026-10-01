"""Data-only admission for versioned native application packages.

Definitions declare bounded representations and projection metadata. They do not
instantiate anything: only executing Genesis instructions can create the graph.
"""
import json
import re
from pathlib import PurePosixPath

from .toolchain import digest, file_hash


def reject():
    raise ValueError('ADMISSION_REJECTED')


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            reject()
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf8'), object_pairs_hook=unique_object,
                      parse_constant=lambda _: reject())


def confined(directory, relative):
    p = PurePosixPath(relative)
    if not relative or p.is_absolute() or '..' in p.parts or '\\' in relative or ':' in relative:
        reject()
    target = (directory / relative).resolve()
    if not target.is_relative_to(directory.resolve()) or not target.is_file():
        reject()
    return target


def load_package(package, expected_hash):
    if file_hash(package) != expected_hash:
        reject()
    manifest = read_json(package)
    if not isinstance(manifest, dict) or not isinstance(manifest.get('operations'), dict):
        reject()
    sources = {manifest['realize'], *(op['source'] for op in manifest['operations'].values())}
    if not sources <= set(manifest['files']) or 'OBSERVE' not in manifest['operations']:
        reject()
    if manifest['operations']['OBSERVE']['mutates'] or manifest['operations']['OBSERVE']['effects']:
        reject()
    for relative, expected in manifest['files'].items():
        if file_hash(confined(package.parent, relative)) != expected:
            reject()
    if 'state_extension' in manifest:
        extension = manifest['state_extension']
        if extension.get('abi') != 'state-extension-v1' or extension['entry'] not in extension['modules']:
            reject()
    if any(not name.endswith('.gen') for name in sources):
        reject()
    if manifest.get('schema_version', 1) == 1:
        return manifest, {}, sources
    if manifest['schema_version'] not in [2, 3]:
        reject()
    if manifest['definitions'] not in manifest['files']:
        reject()
    definitions = read_json(confined(package.parent, manifest['definitions']))
    if not isinstance(definitions, dict) or not 1 <= len(definitions) <= 256:
        reject()
    semantic_ids, native_ids = set(), set()
    for name, definition in definitions.items():
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,63}', name) or name.startswith('bound_'):
            reject()
        if name in {'sea', 'shell', 'nexus', 'state', 'request', 'A', 'B'}:
            reject()
        semantic = definition['semantic']
        if set(semantic) != {'id', 'kind', 'owner', 'public', 'private'}:
            reject()
        if not re.fullmatch(r'[A-Za-z0-9_.:-]{1,128}', semantic['id']):
            reject()
        if semantic['id'] in semantic_ids or definition['mmo_id'] in native_ids:
            reject()
        semantic_ids.add(semantic['id'])
        native_ids.add(definition['mmo_id'])
        if semantic['owner'] is not None and semantic['owner'] not in definitions:
            reject()
        if not isinstance(semantic['public'], dict) or not isinstance(semantic['private'], dict):
            reject()
        if set(semantic['public']) & set(semantic['private']):
            reject()
        if digest(definition['data']) != definition['data_sha256']:
            reject()
    relations = manifest['realization_relations']
    if len(relations) > 2048 or len({tuple(r) for r in relations}) != len(relations):
        reject()
    for source, target, relation in relations:
        if source not in {*definitions, 'state'} or target not in definitions:
            reject()
        if relation not in {'contains', 'owns', 'attaches', 'visible_to', 'private_to'}:
            reject()
    for view in manifest['views'].values():
        if set(view) != {'objects', 'private_owner'} or set(view['objects']) - set(definitions):
            reject()
        if len(set(view['objects'])) != len(view['objects']):
            reject()
        if view['private_owner'] is not None and view['private_owner'] not in definitions:
            reject()
    if manifest['schema_version'] == 3:
        contract = manifest['collections']
        if contract['abi'] != 'state-collections-v1':
            reject()
        required = {contract['config'], contract['catalog'], *contract['units'].values()}
        if not required <= set(manifest['files']):
            reject()
        sources.update(contract['units'].values())
    return manifest, definitions, sources


def verify_realized(backend, prior_bindings, prior_relations, definitions, relations):
    """Check the actually executed native graph against its admission contract."""
    if set(backend.bindings) - set(prior_bindings) - {'request'} != set(definitions):
        reject()
    identities = {}
    for name in definitions:
        obj = backend.resources[backend.bindings[name]]
        if obj['kind'] != 'GEOMETRIC' or obj['payload']['domain'] != 'state':
            reject()
        if obj['payload']['semantic'] != definitions[name]['semantic']:
            reject()
        identities[name] = obj['payload']['identity']
        backend.read_cells(obj)
    if len(set(identities.values())) != len(identities):
        reject()
    identities['state'] = backend.resources[backend.bindings['state']]['payload']['identity']
    expected = {(identities[a], identities[z], relation) for a, z, relation in relations}
    actual = {(backend.resources[r]['payload']['source'], backend.resources[r]['payload']['target'],
               backend.resources[r]['payload']['relation']) for r in backend.relations if r not in prior_relations}
    if actual != expected:
        reject()


def effective_view_owner(manifest, authority):
    """Actor capability authorizes a view; the selected view bounds disclosure."""
    view = manifest['views'].get(authority.get('view_id'))
    if not isinstance(view, dict):
        raise ValueError('AUTHORITY_DENIED')
    owner = view['private_owner']
    if owner is not None and (authority.get('player_role') != owner or not authority.get('private_view')):
        raise ValueError('AUTHORITY_DENIED')
    return owner


def relation_visible(relation, visible, owner_identity):
    return (relation['source'] in visible and relation['target'] in visible
            and (relation['relation'] != 'private_to' or relation['target'] == owner_identity))


def project(backend, manifest, authority):
    owner = effective_view_owner(manifest, authority)
    view = manifest['views'][authority['view_id']]
    objects = {}
    for name in view['objects']:
        payload = backend.resources[backend.bindings[name]]['payload']
        semantic = payload['semantic']
        fields = dict(semantic['public'])
        if owner is not None and owner == semantic['owner']:
            fields.update(semantic['private'])
        objects[name] = {'identity': payload['identity'], 'semantic_id': semantic['id'],
                         'kind': semantic['kind'], 'owner': semantic['owner'], 'fields': fields}
    visible = {o['identity'] for o in objects.values()}
    owner_id = objects[owner]['identity'] if owner in objects else None
    relations = []
    for ref in backend.relations:
        relation = backend.resources[ref]['payload']
        if relation_visible(relation, visible, owner_id):
            relations.append(dict(relation))
    # Caller detaches the entire value. Never expose native resource dictionaries.
    return {'objects': objects, 'relations': relations}
