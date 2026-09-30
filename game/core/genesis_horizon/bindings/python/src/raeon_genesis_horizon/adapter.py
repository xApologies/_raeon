"""Serialized Horizon owner over verified Genesis and native immutable resources.

The commit point is an fsynced, atomically replaced resource-graph root containing
both successor bindings and the operation outcome. Candidate overlays never
replace live bindings before that point. This is a trusted reference deployment,
not a sandbox for arbitrary hostile Genesis packages.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import shutil
import threading
import uuid

from .toolchain import initialize, compile_paths, execute, canonical, digest, file_hash


class HorizonError(RuntimeError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


class Horizon:
    def __init__(self, storage, root=None, fault_hook=None):
        self.root, self.upstream, self.lock = initialize(root)
        from .native import NativeBackend
        self.backend_type = NativeBackend
        self.storage = Path(storage).resolve()
        self.storage.mkdir(parents=True, exist_ok=True)
        self.lifecycle = 'CREATED'
        self._backend = None
        self._state = None
        self._mutex = threading.RLock()
        self._builds = {}
        self.fault_hook = fault_hook or (lambda point: None)
        self.epoch = uuid.uuid4().hex

    def _fault(self, point):
        self.fault_hook(point)

    def _run(self, relative, budget):
        if relative not in self._builds:
            self._builds[relative] = compile_paths([self.root / relative], self.root, Path(relative).stem)
        try:
            remaining = min(budget, getattr(self, '_remaining', budget))
            if remaining <= 0:
                raise HorizonError('BUDGET_EXCEEDED')
            result = execute(self._builds[relative], self._backend, remaining)
            if hasattr(self, '_remaining'):
                self._remaining -= result.receipt['payload']['steps']
        except Exception as error:
            if 'step limit' in str(error):
                raise HorizonError('BUDGET_EXCEEDED') from error
            raise
        return result.receipt

    def _core(self, name, budget):
        return self._run('game/core/genesis_horizon/src/' + name + '.gen', budget)

    def _ready(self):
        if hasattr(self, '_remaining'):
            del self._remaining
        if self._backend and sum(p.stat().st_size for p in self.storage.rglob('*') if p.is_file()) + 1048576 > self.profile['limits']['native_storage_bytes']:
            raise HorizonError('BACKPRESSURE')
        if self.lifecycle != 'READY':
            raise HorizonError('ADMISSION_REJECTED' if self.lifecycle == 'QUIESCING' else 'RUNTIME_FAULT')

    def _record(self):
        b = self._backend
        return {'bindings': b.bindings, 'relations': b.relations, 'resources': b.resources,
                'ledger': b.ledger, 'allocator': b.allocator.snapshot(), 'road_history': b.road_history,
                'native_receipts': b.native_receipts}

    def _restore_record(self, record):
        b = self._backend
        for field in ['bindings', 'relations', 'resources', 'ledger', 'road_history', 'native_receipts']:
            setattr(b, field, copy.deepcopy(record[field]))
        b.allocator.entries = copy.deepcopy(record['allocator']['entries'])
        b.pending = {}

    def _save(self, state):
        payload = {'schema': 1, 'profile_hash': digest(self.profile), 'upstream': self.lock['upstream_commit'],
                   'state': state, 'native': self._record(), 'store': str(self.storage),
                   'builds': {k: v.receipt['gvm_sha256'] for k, v in self._builds.items()}}
        envelope = {'payload': payload, 'sha256': digest(payload)}
        temp = self.storage / 'root.pending'
        with temp.open('wb') as stream:
            stream.write(canonical(envelope))
            stream.flush()
            os.fsync(stream.fileno())
        self._fault('before_publish')
        os.replace(temp, self.storage / 'root.json')
        self._state = copy.deepcopy(state)

    def boot(self, profile=None, trusted_context=None, budget=100000):
        with self._mutex:
            if self.lifecycle != 'CREATED' or (self.storage / 'root.json').exists():
                raise HorizonError('ADMISSION_REJECTED')
            self.lifecycle = 'BOOTING'
            self.profile = copy.deepcopy(profile or json.loads((self.root / 'data/platform/genesis-horizon-profile.json').read_text(encoding='utf8')))
            expected = json.loads((self.root / 'data/platform/genesis-horizon-profile.json').read_text(encoding='utf8'))
            if digest(expected) != digest(self.profile):
                self.lifecycle = 'FAULTED'
                raise HorizonError('ADMISSION_REJECTED')
            context = trusted_context or {}
            self.identity = context.get('instance_identity', uuid.uuid4().hex)
            from .native import create_fabric
            fabric = Path(context.get('fabric_path', self.storage / 'fabric.gcf')).resolve()
            try:
                if not fabric.exists() and fabric == self.storage / 'fabric.gcf':
                    create_fabric(fabric, self.profile['fabric']['cells'], self.profile['fabric']['seed'])
                self._backend = self.backend_type(self.profile, fabric, self.storage / 'native', self.identity)
                receipt = self._core('boot', budget)
                if len(self._backend.bindings) != 4 or len(self._backend.relations) != 3:
                    raise HorizonError('CLOSURE_FAILED')
                state = {'identity': self.identity, 'revision': 0, 'application': None, 'outcomes': {}, 'inputs': [], 'root': ''}
                state['root'] = self._semantic_root(state)
                self._save(state)
                self.lifecycle = 'READY'
                return {'identity': self.identity, 'domains': self.domains(), 'receipt': receipt, 'epoch': self.epoch}
            except Exception:
                if self._backend:
                    self._backend.close()
                self.lifecycle = 'FAULTED'
                raise

    def domains(self):
        return {name: {'identity': self._backend.resources[self._backend.bindings[name]]['payload']['identity'],
                       'version': self._backend.resources[self._backend.bindings[name]]['payload']['native']['instance_id'],
                       'dimensions': dims}
                for name, dims in self.profile['domains'].items()}

    def _semantic_root(self, state):
        b = self._backend
        objects = {}
        for name, ref in sorted(b.bindings.items()):
            if name == 'request':
                continue
            obj = b.resources[ref]
            objects[name] = {'identity': obj['payload']['identity'],
                             'version': obj['payload']['native']['instance_id'],
                             'cells': [cell.pack().hex() for cell in b.read_cells(obj)]}
        return digest({'identity': self.identity, 'revision': state['revision'], 'objects': objects,
                       'relations': [b.resources[ref]['payload'] for ref in b.relations]})

    def _authority(self, authority, operations=()):
        if not isinstance(authority, dict) or not authority.get('actor'):
            raise HorizonError('AUTHORITY_DENIED')
        self._backend.authority = {'actor': authority['actor'], 'operations': list(operations),
                                   'relationships': authority.get('relationships', [])}

    def realize_application(self, package_ref, authority, budget=100000):
        with self._mutex:
            self._ready()
            if not authority.get('realize'):
                raise HorizonError('AUTHORITY_DENIED')
            package = (self.root / package_ref['path']).resolve()
            if not package.is_relative_to(self.root / 'tests/integration/genesis_horizon/application'):
                raise HorizonError('AUTHORITY_DENIED')
            if file_hash(package) != package_ref['sha256']:
                raise HorizonError('ADMISSION_REJECTED')
            manifest = json.loads(package.read_text(encoding='utf8'))
            for relative, expected in manifest['files'].items():
                path = (package.parent / relative).resolve()
                if not path.is_relative_to(package.parent) or file_hash(path) != expected:
                    raise HorizonError('ADMISSION_REJECTED')
            if self._state['application']:
                if self._state['application']['package_sha256'] == package_ref['sha256']:
                    return copy.deepcopy(self._state['application'])
                raise HorizonError('ADMISSION_REJECTED')
            saved = copy.deepcopy(self._record())
            try:
                self._backend.phase = 'realize'
                self._authority(authority, ['INHERIT_STATE'])
                self._run((package.parent / manifest['realize']).relative_to(self.root).as_posix(), budget)
                self._core('state', budget)
                self._backend.bindings.update(self._backend.pending)
                state = copy.deepcopy(self._state)
                state['application'] = {'id': manifest['id'], 'package_sha256': package_ref['sha256'], 'manifest': manifest,
                                        'directory': package.parent.relative_to(self.root).as_posix()}
                state['root'] = self._semantic_root(state)
                self._save(state)
                return copy.deepcopy(state['application'])
            except Exception:
                self._restore_record(saved)
                raise

    def _route(self, direction, semantic, authority, budget):
        if len(self._backend.road_history) + 3 > self.profile['limits']['native_road_receipts']:
            raise HorizonError('BACKPRESSURE')
        self._authority(authority, ['ROUTE'])
        self._backend.active_request = {'source': 'sea' if direction == 'in' else 'state', 'semantic': semantic}
        return self._core('road_' + direction, budget)

    def _view(self, authority):
        app = self._state['application']
        if not app or authority.get('application_id') != app['id'] or authority.get('view_id') not in ('public', 'writer'):
            raise HorizonError('AUTHORITY_DENIED')
        if authority['view_id'] == 'writer' and not authority.get('private_view'):
            raise HorizonError('AUTHORITY_DENIED')
        names = app['manifest']['views'][authority['view_id']]
        b = self._backend
        objects = {}
        for name in names:
            resource = b.resources[b.bindings[name]]
            objects[name] = {'identity': resource['payload']['identity'],
                             'cells': [{'handedness': c.handedness, 'occupancy': c.occupancy_pattern} for c in b.read_cells(resource)]}
        visible_ids = {obj['identity'] for obj in objects.values()}
        relations = [copy.deepcopy(b.resources[r]['payload']) for r in b.relations
                     if b.resources[r]['payload']['source'] in visible_ids and b.resources[r]['payload']['target'] in visible_ids]
        return {'objects': objects, 'relations': relations}

    def observe(self, view_context, projection_cursor=None):
        with self._mutex:
            self._ready()
            view = self._view(view_context)
            self._route('in', {'observe': view_context['view_id']}, view_context, 100000)
            app = self._state['application']
            self._run(app['directory'] + '/' + app['manifest']['operations']['OBSERVE']['source'], 100000)
            self._route('out', {'view_digest': digest(view)}, view_context, 100000)
            return {'view_id': view_context['view_id'], 'epoch': self.epoch, 'state_revision': self._state['revision'],
                    'view': view, 'digest': digest(view)}

    def lookup_outcome(self, operation_key):
        with self._mutex:
            return copy.deepcopy(self._state['outcomes'].get(digest(list(operation_key))))

    def execute(self, intent, authority, budget=100000):
        with self._mutex:
            self._ready()
            self._view(authority)
            app = self._state['application']
            key = digest([app['id'], authority['actor'], intent['request_id']])
            request_digest = digest(intent)
            previous = self._state['outcomes'].get(key)
            if previous:
                if previous['request_digest'] != request_digest:
                    raise HorizonError('REQUEST_ID_CONFLICT')
                if previous.get('expired'):
                    raise HorizonError('RETRY_EXPIRED')
                return copy.deepcopy(previous)
            if len(self._state['outcomes']) >= self.profile['limits']['outcome_records']:
                raise HorizonError('BACKPRESSURE')
            operation = intent['operation']
            definition = app['manifest']['operations'].get(operation)
            if not definition:
                raise HorizonError('UNKNOWN_OPERATION')
            if operation not in authority.get('operations', []) or intent['arguments'] != {}:
                raise HorizonError('AUTHORITY_DENIED')
            if intent['expected_revision'] != self._state['revision']:
                raise HorizonError('STALE_PRECONDITION')
            self._remaining = budget
            saved = copy.deepcopy(self._record())
            old_root = self._state['root']
            try:
                incoming = self._route('in', intent, authority, budget)
                self._backend.phase = 'application'
                self._authority(authority, definition['effects'] + ['INHERIT_STATE'])
                self._backend.authority['relationships'] = definition.get('relationships', [])
                receipt = self._run(app['directory'] + '/' + definition['source'], budget)
                self._fault('after_candidate')
                if definition['mutates']:
                    self._core('state', budget)
                    self._backend.bindings.update(self._backend.pending)
                self._fault('before_closure')
                outgoing = self._route('out', {'request_digest': request_digest}, authority, budget)
                state = copy.deepcopy(self._state)
                state['revision'] += int(definition['mutates'])
                state['root'] = self._semantic_root(state)
                outcome = {'status': 'COMMITTED' if definition['mutates'] else 'OBSERVED',
                           'request_digest': request_digest, 'request_id': intent['request_id'],
                           'revision': state['revision'], 'previous_root': old_root, 'root': state['root'],
                           'commit_id': digest([key, state['root']]), 'native_execution': receipt['resource_id'],
                           'inward': incoming['resource_id'], 'outward': outgoing['resource_id']}
                state['outcomes'][key] = outcome
                state['inputs'].append({'intent': copy.deepcopy(intent), 'authority': copy.deepcopy(authority), 'root': state['root']})
                self._save(state)
            except Exception:
                self._restore_record(saved)
                raise
            finally:
                if hasattr(self, '_remaining'):
                    del self._remaining
            # Delivery is outside the commit transaction. Callers recover by key.
            self._fault('after_commit')
            return copy.deepcopy(outcome)

    def expire_outcome(self, operation_key, authority):
        """Trusted retention control retains a bounded tombstone; IDs are never reused."""
        with self._mutex:
            self._ready()
            if not authority.get('checkpoint'):
                raise HorizonError('AUTHORITY_DENIED')
            key = digest(list(operation_key))
            if key not in self._state['outcomes']:
                raise HorizonError('RETRY_EXPIRED')
            state = copy.deepcopy(self._state)
            record = state['outcomes'][key]
            state['outcomes'][key] = {'request_digest': record['request_digest'], 'expired': True}
            self._save(state)

    def quiesce(self, budget=100000):
        with self._mutex:
            if self.lifecycle in ('QUIESCING', 'STOPPED'):
                return {'lifecycle': self.lifecycle}
            self._ready()
            receipt = self._core('lifecycle', budget)
            self.lifecycle = 'QUIESCING'
            return {'lifecycle': self.lifecycle, 'receipt': receipt}

    def checkpoint(self, authority):
        with self._mutex:
            if not authority.get('checkpoint'):
                raise HorizonError('AUTHORITY_DENIED')
            if self.lifecycle not in ('READY', 'QUIESCING'):
                raise HorizonError('RUNTIME_FAULT')
            self._core('lifecycle', 100000)
            self._save(copy.deepcopy(self._state))
            checkpoints = self.storage / 'checkpoints'
            if checkpoints.exists() and len(list(checkpoints.iterdir())) >= 16:
                raise HorizonError('BACKPRESSURE')
            native_bytes = sum(p.stat().st_size for p in (self.storage / 'native').rglob('*') if p.is_file())
            used_bytes = sum(p.stat().st_size for p in self.storage.rglob('*') if p.is_file())
            if used_bytes + native_bytes + 2097152 > self.profile['limits']['native_storage_bytes']:
                raise HorizonError('BACKPRESSURE')
            name = uuid.uuid4().hex
            target = self.storage / 'checkpoints' / name
            target.mkdir(parents=True)
            files = [self.storage / 'root.json', self._backend.fabric.path, *sorted((self.storage / 'native').rglob('*'))]
            manifest = {}
            for path in files:
                if path.is_file():
                    if not path.resolve().is_relative_to(self.storage):
                        raise HorizonError('AUTHORITY_DENIED')
                    relative = path.relative_to(self.storage)
                    dest = target / relative
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(path, dest)
                    manifest[relative.as_posix()] = file_hash(dest)
            (target / 'manifest.json').write_bytes(canonical(manifest))
            return {'name': name, 'sha256': digest(manifest), 'root': self._state['root']}

    def restore(self, checkpoint_ref, authority, budget=100000):
        with self._mutex:
            if not authority.get('restore'):
                raise HorizonError('AUTHORITY_DENIED')
            name = checkpoint_ref.get('name', '')
            if len(name) != 32 or any(c not in '0123456789abcdef' for c in name):
                raise HorizonError('AUTHORITY_DENIED')
            source = self.storage / 'checkpoints' / name
            manifest = json.loads((source / 'manifest.json').read_text(encoding='utf8'))
            if digest(manifest) != checkpoint_ref['sha256']:
                raise HorizonError('RUNTIME_FAULT')
            for relative, expected in manifest.items():
                path = (source / relative).resolve()
                if not path.is_relative_to(source) or file_hash(path) != expected:
                    raise HorizonError('RUNTIME_FAULT')
            envelope = json.loads((source / 'root.json').read_text(encoding='utf8'))
            payload = envelope['payload']
            if digest(payload) != envelope['sha256'] or payload['upstream'] != self.lock['upstream_commit']:
                raise HorizonError('RUNTIME_FAULT')
            profile = json.loads((self.root / 'data/platform/genesis-horizon-profile.json').read_text(encoding='utf8'))
            if digest(profile) != payload['profile_hash']:
                raise HorizonError('RUNTIME_FAULT')
            # Candidate has its own native directory; failed verification cannot touch live resources.
            candidate_root = self.storage / 'restored' / uuid.uuid4().hex
            candidate_root.mkdir(parents=True)
            for relative in manifest:
                destination = candidate_root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source / relative, destination)
            old_prefix = payload['store']
            def relocate(value):
                if isinstance(value, str) and value.startswith(old_prefix + os.sep):
                    return str(candidate_root) + value[len(old_prefix):]
                if isinstance(value, list):
                    return [relocate(v) for v in value]
                if isinstance(value, dict):
                    return {relocate(k): relocate(v) for k, v in value.items()}
                return value
            payload = relocate(payload)
            old = (self._backend, self._state, getattr(self, 'profile', None), getattr(self, 'identity', None), self.storage)
            candidate = None
            try:
                self.profile = profile
                self.identity = payload['state']['identity']
                candidate = self.backend_type(profile, candidate_root / 'fabric.gcf', candidate_root / 'native', self.identity)
                self._backend = candidate
                self._restore_record(payload['native'])
                for relative, expected in payload['builds'].items():
                    build = compile_paths([self.root / relative], self.root, Path(relative).stem)
                    if build.receipt['gvm_sha256'] != expected:
                        raise HorizonError('RUNTIME_FAULT')
                    self._builds[relative] = build
                if self._semantic_root(payload['state']) != payload['state']['root']:
                    raise HorizonError('RUNTIME_FAULT')
                self._core('lifecycle', budget)
                self.storage = candidate_root
                self._save(payload['state'])
            except Exception:
                if candidate:
                    candidate.close()
                self._backend, self._state, self.profile, self.identity, self.storage = old
                raise
            if old[0] and self.lifecycle != 'STOPPED':
                old[0].close()
            self.epoch = uuid.uuid4().hex
            self.lifecycle = 'READY'
            return {'root': self._state['root'], 'epoch': self.epoch, 'domains': self.domains()}

    def close(self):
        with self._mutex:
            if self.lifecycle == 'STOPPED':
                return {'lifecycle': 'STOPPED'}
            if self.lifecycle == 'READY':
                self.quiesce()
            if self._backend and self.lifecycle != 'FAULTED':
                self._backend.close()
            self.lifecycle = 'STOPPED'
            return {'lifecycle': 'STOPPED'}
