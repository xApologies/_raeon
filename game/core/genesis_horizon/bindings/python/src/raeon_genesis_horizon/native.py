"""Bindings v1 for existing Genesis primitives and native immutable engines.

Domain MMOs are finite reference execution fixtures. Registry dimensions are
retained as architectural types; no mathematical embedding is asserted.
"""
from __future__ import annotations

import copy
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm.backend import ReferenceBackend
from vendor.genesis_chirality_machine.image import FabricImage, FabricImageBuilder
from vendor.genesis_chirality_machine.fixture import deterministic_cells
from vendor.genesis_geometric_engine.allocator import RegionAllocator
from vendor.genesis_geometric_engine.engine import InstantiationEngine
from vendor.genesis_geometric_engine.model import RepresentationBundle
from vendor.genesis_geometric_engine.profiles import Generic3p1p1Profile
from genesis_transform_engine.engine import TransformationEngine
from genesis_transform_engine.model import TransformRequest, InvariantContract
from genesis_transform_engine.view import TransformView
from genesis_portal_engine import CorridorGraph, CapacityLedger, PortalEngine
from genesis_portal_engine.model import CorridorEdge, PortalAddress, PreservationContract
from genesis_rainbow_road import RainbowRoadEngine, RoadCapacityManager, RoadLedger, audit_road_receipt
from genesis_rainbow_road.model import RainbowRoadRequest

from .toolchain import digest, file_hash


class BindingError(RuntimeError):
    pass


def create_fabric(path, cells=32768, seed=430043):
    path = Path(path)
    if path.exists():
        raise BindingError('Fabric creation requires a new path')
    path.parent.mkdir(parents=True, exist_ok=True)
    FabricImageBuilder.build(path, deterministic_cells(cells, seed))
    return file_hash(path)


class NativeBackend(ReferenceBackend):
    def __init__(self, profile, fabric_path, working, identity):
        super().__init__(backend_id='raeon-native-bindings', version='1.0.0')
        self.profile = copy.deepcopy(profile)
        self.working = Path(working).resolve()
        self.working.mkdir(parents=True, exist_ok=True)
        self.identity = identity
        if file_hash(fabric_path) != profile['fabric']['sha256']:
            raise BindingError('FABRIC_INTEGRITY')
        required = {'sea', 'shell', 'nexus', 'state', 'A', 'B', 'request'}
        if set(profile['definitions']) != required:
            raise BindingError('MISSING_DEFINITION')
        self.fabric = FabricImage(fabric_path, verify=True)
        self.allocator = RegionAllocator(self.fabric.cell_count, alignment=8)
        self.instantiator = InstantiationEngine(self.fabric, self.allocator, self.working / 'instances')
        self.transformer = TransformationEngine(self.fabric, self.working / 'transforms')
        self.application_values = {}
        self.collections = None
        self.executing_source = None
        self.application_definitions = {}
        self.realization_relations = []
        self.bindings = {}
        self.relations = []
        self.authority = None
        self.phase = 'boot'
        self.active_request = None
        self.native_receipts = []
        self.pending = {}
        self.road_history = []
        edges = []
        for left, right in profile['containment']:
            for a, z in [(left, right), (right, left)]:
                edges.append(CorridorEdge(a + '-' + z, a, z, ('GENERIC',), ('ANY',), ('ANY',), 1.0, 1.0, 1, 1, 'White', True))
        graph = CorridorGraph(edges)
        self.local_graph = graph
        capacity = CapacityLedger({edge.edge_id: 1 for edge in edges}, self.working / 'capacity.jsonl')
        self.local_capacity = capacity
        manager = RoadCapacityManager(capacity, RoadLedger(self.working / 'road-bus.jsonl'))
        portal = PortalEngine(self.fabric, self.allocator, graph, manager, self.working / 'portals')
        self.road_engine = RainbowRoadEngine(portal, manager, self.working / 'roads')
        # Checkpoints retain the append-only native trace. Continue its chain;
        # candidate rollback restores capacity state, never forensic log bytes.
        for ledger, path in [(capacity, capacity.ledger_path), (manager.ledger, manager.ledger.path),
                             (portal.ledger, portal.ledger.path), (self.road_engine.ledger, self.road_engine.ledger.path)]:
            if path.exists():
                with path.open(encoding='utf8') as stream:
                    for line in stream:
                        entry = json.loads(line)
                        ledger.prev = entry['entry_hash']
                        event = entry.get('event', {})
                        # Historical checkpoints did not serialize reservation
                        # ordinals. Their native ledgers preserve those entries.
                        if ledger is capacity and event['kind'] in ('ROUTE_CAPACITY_RESERVED', 'ROUTE_CAPACITY_RELEASED'):
                            capacity.reservations[event['reservation_id']] = {k:v for k,v in event.items() if k != 'kind'}
                        if ledger is manager.ledger and event['kind'] in ('ROAD_PORTAL_SUBRESERVED', 'ROAD_PORTAL_SUBRELEASED'):
                            manager.subreservations[event['reservation_id']] = {k:v for k,v in event.items() if k != 'kind'}

    def transport_record(self):
        manager = self.road_engine.capacity
        return {'schema': 1, 'edges': [asdict(e) for e in self.local_graph.edges.values()],
                'capacity': copy.deepcopy(self.local_capacity.capacity),
                'reservations': copy.deepcopy(self.local_capacity.reservations),
                'active': manager.active, 'holds': copy.deepcopy(manager.holds),
                'subreservations': copy.deepcopy(manager.subreservations)}

    def restore_transport(self, record):
        if record is None:
            return  # Explicit historical checkpoint upgrade; ledgers recovered above.
        if record['schema'] != 1:
            raise BindingError('TRANSPORT_CHECKPOINT_INTEGRITY')
        graph = self.local_graph
        graph.edges.clear(); graph.out.clear()
        for row in record['edges']:
            row = copy.deepcopy(row)
            for key in ('sectors', 'chirality_classes', 'residue_classes'):
                row[key] = tuple(row[key])
            graph.add_edge(CorridorEdge(**row))
        self.local_capacity.capacity = copy.deepcopy(record['capacity'])
        self.local_capacity.reservations = copy.deepcopy(record['reservations'])
        manager = self.road_engine.capacity
        manager.active = record['active']
        manager.holds = copy.deepcopy(record['holds'])
        manager.subreservations = copy.deepcopy(record['subreservations'])

    def _put(self, *args, **kwargs):
        if len(self.resources) >= self.profile['limits']['native_resources']:
            raise BindingError('BACKPRESSURE')
        return super()._put(*args, **kwargs)

    def mount_fabric(self, uri):
        if uri != 'fabric://horizon/locked-v1':
            raise BindingError('UNKNOWN_FABRIC')
        return self._put('FABRIC', {'uri': uri, 'sha256': self.profile['fabric']['sha256'],
                                  'fabric_tag': self.fabric.fabric_tag, 'immutable_base': True})

    def alloc(self, fabric, cells):
        if type(cells) is not int or not 0 < cells <= self.fabric.cell_count:
            raise BindingError('BUDGET_EXCEEDED')
        return super().alloc(fabric, cells)

    def instantiate(self, fabric, region, mmo):
        name = mmo.get('handle', '').removeprefix('@')
        service = self.collections
        unit = service.unit if service else None
        if name in {'app_new', 'app_item', 'app_source', 'app_target'}:
            if not unit or self.phase != 'application' or not self.executing_source:
                raise BindingError('AUTHORITY_DENIED')
            required = {'app_new': 'instantiate', 'app_item': 'transport', 'app_source': 'relation', 'app_target': 'relation'}[name]
            if unit['mode'] != required or self.executing_source != service.directory + '/' + service.manifest['collections']['units'][{'relation': 'relate'}.get(required, required)]:
                raise BindingError('AUTHORITY_DENIED')
            if name == 'app_new':
                name = unit['name']
                self.application_definitions[name] = copy.deepcopy(unit['definition'])
            else:
                key = {'app_item': 'name', 'app_source': 'source', 'app_target': 'target'}[name]
                return self.resources[self.bindings[unit[key]]]

        if name.startswith('bound_'):
            name = name[6:]
            if name not in self.bindings:
                raise BindingError('UNRESOLVED_PERSISTENT_RESOURCE')
            return self.resources[self.bindings[name]]
        if name not in self.profile['definitions'] and name not in self.application_definitions:
            raise BindingError('UNKNOWN_MMO')
        if name in self.application_definitions and self.phase != 'realize' and not (unit and unit.get('mode') == 'instantiate' and name == unit['name']):
            raise BindingError('AUTHORITY_DENIED')
        if name in self.profile['domains'] and self.phase != 'boot':
            raise BindingError('AUTHORITY_DENIED')
        if name in ('A', 'B') and (self.phase != 'realize' or self.application_definitions):
            raise BindingError('AUTHORITY_DENIED')
        if name == 'request' and self.phase != 'route':
            raise BindingError('AUTHORITY_DENIED')
        if name in self.bindings and name != 'request':
            raise BindingError('DUPLICATE_INSTANCE')
        definition = (self.application_definitions if name in self.application_definitions else self.profile['definitions'])[name]
        if digest(definition['data']) != definition['data_sha256']:
            raise BindingError('DEFINITION_INTEGRITY')
        data = definition['data']
        shape = tuple(data['grid_shape'])
        arrays = {key: np.array(value, dtype=np.float32).reshape(shape + ((2, 2) if key == 'chirality_field_3p1p1' else ()))
                  for key, value in data['arrays'].items()}
        sources = {'definition': definition['data_sha256'], 'instance_namespace': digest(self.identity)}
        if 'provenance_commitment' in definition:
            sources['application_provenance'] = definition['provenance_commitment']
        if name == 'request':
            if self.active_request is None:
                raise BindingError('UNBOUND_REQUEST')
            sources['request_commitment'] = digest(self.active_request)
        bundle = RepresentationBundle(definition['mmo_id'], definition['representation_id'],
                                      'GENERIC_3P1P1', shape, arrays,
                                      sources)
        plan, reservation = self.instantiator.plan(bundle, Generic3p1p1Profile())
        if plan.required_cells > region['payload']['cells']:
            self.allocator.abort(reservation)
            raise BindingError('BUDGET_EXCEEDED')
        instance, receipts = self.instantiator.materialize(bundle, Generic3p1p1Profile(), plan, reservation, verify_stride=1)
        native = instance.to_dict()
        native['segment_chain'] = [native['segment_path']]
        stable = self.identity + ':' + native['instance_id']
        resource = self._put('GEOMETRIC', {'binding': name, 'identity': stable, 'native': native, 'closed': True,
                                          'definition_sha256': digest(definition), 'domain': name if name in self.profile['domains'] else 'state'})
        if 'semantic' in definition:
            resource['payload']['semantic'] = copy.deepcopy(definition['semantic'])
        self.bindings[name] = resource['resource_id']
        self.native_receipts.append({'operation': 'instantiate', 'name': name, 'receipts': receipts})
        if name == 'request':
            resource['payload']['location'] = self.active_request['source']
            resource['payload']['request_commitment'] = sources['request_commitment']
        return resource

    def read_cells(self, resource):
        native = resource['payload']['native']
        view = TransformView(self.fabric, native['segment_chain'])
        try:
            return [view.read_index(i) for i in range(native['region']['start'], native['region']['start'] + native['region']['count'])]
        finally:
            view.close()

    def relate(self, geo, target, attrs):
        unit = self.collections.unit if self.collections else None
        if target == 'app_target' and unit and unit['mode'] == 'relation':
            target = unit['target']
        if target not in self.bindings:
            raise BindingError('UNRESOLVED_RELATION_TARGET')
        other = self.resources[self.bindings[target]]
        source_name = geo['payload']['binding']
        relation = attrs.get('relation')
        allowed = self.phase == 'boot' and [source_name, target] in self.profile['containment'] and relation == 'contains'
        allowed |= self.phase == 'realize' and not self.application_definitions and source_name == 'state' and target in ('A', 'B') and relation == 'contains'
        allowed |= self.phase == 'realize' and [source_name, target, relation] in self.realization_relations
        allowed |= self.phase == 'application' and [source_name, target, relation] in (self.authority or {}).get('relationships', [])
        allowed |= bool(unit and unit['mode'] == 'relation' and self.phase == 'application' and source_name == unit['source'] and target == unit['target'] and relation == 'contains')
        if not allowed:
            raise BindingError('AUTHORITY_DENIED')
        result = self._put('RELATION', {'source': geo['payload']['identity'], 'target': other['payload']['identity'], 'relation': relation},
                           [geo['resource_id'], other['resource_id']])
        if result['resource_id'] not in self.relations:
            self.relations.append(result['resource_id'])
        return result

    def admit(self, geo, attrs):
        operation = attrs.get('operation')
        if operation == 'COLLECTION_TRANSACTION' and self.collections:
            return self.collections.admit(geo, attrs)
        if operation == 'COLLECTION_ROUTE':
            unit = self.collections.unit if self.collections else None
            if not unit or unit['mode'] != 'transport' or geo['payload']['binding'] != unit['name']:
                raise BindingError('AUTHORITY_DENIED')
            return self._put('ADMISSION', {'source': geo['resource_id'], 'operation': operation, 'admitted': True}, [geo['resource_id']])
        if not self.authority or operation not in self.authority.get('operations', []):
            raise BindingError('AUTHORITY_DENIED')
        if operation == 'INHERIT_STATE':
            if geo['payload'].get('binding') != 'state' or self.phase != 'state_commit':
                raise BindingError('AUTHORITY_DENIED')
        elif geo['payload'].get('binding') in self.profile['domains']:
            raise BindingError('AUTHORITY_DENIED')
        return self._put('ADMISSION', {'source': geo['resource_id'], 'operation': operation, 'actor': self.authority['actor'], 'admitted': True}, [geo['resource_id']])

    def transform(self, geo, admission, attrs):
        operator = attrs.get('operator')
        if admission['payload']['source'] != geo['resource_id'] or operator != admission['payload']['operation']:
            raise BindingError('ADMISSION_REJECTED')
        if operator == 'COLLECTION_TRANSACTION' and self.collections:
            return self.collections.transform(geo, admission, attrs)
        if operator not in ('MIRROR_CHIRALITY', 'INHERIT_STATE'):
            raise BindingError('UNKNOWN_OPERATION')
        native = geo['payload']['native']
        req = TransformRequest(native, native['segment_chain'], 'GENERIC_LIVE' if operator == 'MIRROR_CHIRALITY' else 'PIPELINE_R',
                               [{'op': 'MIRROR_CHIRALITY' if operator == 'MIRROR_CHIRALITY' else 'INHERIT'}], InvariantContract())
        result = self.transformer.execute(req)
        payload = copy.deepcopy(geo['payload'])
        payload['native'] = result.child_instance
        payload['pre_state_root'] = result.pre_state_root
        payload['post_state_root'] = result.post_state_root
        successor = self._put('GEOMETRIC', payload, [geo['resource_id'], admission['resource_id']])
        self.pending[payload['binding']] = successor['resource_id']
        self.native_receipts.append({'operation': operator, 'receipt': result.receipt, 'changed_cells': result.changed_cells})
        return successor

    def fork(self, geo, attrs):
        raise BindingError('UNDECLARED_EFFECT')

    def write_overlay(self, fabric, addr, value):
        raise BindingError('UNDECLARED_EFFECT')

    def assert_closure(self, resource):
        if resource['kind'] == 'GEOMETRIC':
            self.read_cells(resource)
        return super().assert_closure(resource)

    def close(self):
        self.fabric.close()

    def portal_open(self, geo, admission, sector, attrs):
        unit = self.collections.unit if self.collections else None
        if unit and unit['mode'] == 'transport':
            if admission['payload']['operation'] != 'COLLECTION_ROUTE' or admission['payload']['source'] != geo['resource_id'] or sector != 'GENERIC' or attrs.get('corridor') != 'application-local':
                raise BindingError('INVALID_ROUTE')
            source, target = unit['source'], unit['target']
            self.collections.authorize_route(unit['name'], source, target)
            edge_id = source + '-' + target
            if edge_id not in self.local_graph.edges:
                self.local_graph.add_edge(CorridorEdge(edge_id, source, target, ('GENERIC',), ('ANY',), ('ANY',), 1.0, 1.0, 1, 1, 'White', True))
                self.local_capacity.capacity[edge_id] = 1
            return super().portal_open(geo, admission, sector, dict(attrs, corridor=source + '->' + target))
        if geo['payload']['binding'] != 'request' or admission['payload']['operation'] != 'ROUTE':
            raise BindingError('INVALID_ROUTE')
        if admission['payload']['source'] != geo['resource_id'] or sector != 'GENERIC':
            raise BindingError('ADMISSION_REJECTED')
        corridor = attrs.get('corridor', '').split('->')
        if len(corridor) != 2 or corridor[0] != geo['payload'].get('location'):
            raise BindingError('INVALID_ROUTE')
        if corridor not in self.profile['containment'] and list(reversed(corridor)) not in self.profile['containment']:
            raise BindingError('INVALID_ROUTE')
        return super().portal_open(geo, admission, sector, attrs)

    def portal_transport(self, portal, geo, attrs):
        source, target = portal['payload']['attrs']['corridor'].split('->')
        unit = self.collections.unit if self.collections else None
        destination = target if unit and unit['mode'] == 'transport' and attrs.get('destination') == 'application-target' else attrs.get('destination')
        if destination != target or portal['payload']['source'] != geo['resource_id']:
            raise BindingError('INVALID_ROUTE')
        native = geo['payload']['native']
        request = RainbowRoadRequest(native, native['segment_chain'], PortalAddress(source), [PortalAddress(target)],
                                     preservation=PreservationContract(['__FULL_CELL__']), road_name='')
        result = self.road_engine.execute(request)
        if not audit_road_receipt(result.receipt)['pass']:
            raise BindingError('CLOSURE_FAILED')
        payload = copy.deepcopy(geo['payload'])
        payload.update(native=result.final_instance, location=target, native_road=result.receipt)
        return self._put('GEOMETRIC', payload, [geo['resource_id'], portal['resource_id']], sector='GENERIC')

    def portal_close(self, portal, dest):
        if dest['payload'].get('native_road', {}).get('status') != 'CLOSED':
            raise BindingError('CLOSURE_FAILED')
        result = super().portal_close(portal, dest)
        result['payload']['native_road'] = dest['payload']['native_road']
        self.road_history.append(copy.deepcopy(dest['payload']['native_road']))
        return result

    def road_close(self, road, geo):
        receipts = [self.resources[r]['payload']['native_road'] for r in road['payload']['legs']]
        if not receipts or not all(audit_road_receipt(r)['pass'] for r in receipts):
            raise BindingError('CLOSURE_FAILED')
        for left, right in zip(receipts, receipts[1:]):
            if left['final_instance_id'] != right['source_instance_id']:
                raise BindingError('CLOSURE_FAILED')
        result = super().road_close(road, geo)
        unit = self.collections.unit if self.collections else None
        if unit and unit['mode'] == 'transport':
            unit.update(closed=True, successor=geo['resource_id'])
        return result
