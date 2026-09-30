"""Strict v2 envelope schemas. Domain-specific operation validity is Horizon-owned."""
import re
from .errors import BoundaryError, CODES

INBOUND = frozenset(['HELLO', 'INTENT', 'SYNC_REQUEST', 'ACK', 'HEARTBEAT'])
OUTBOUND = frozenset(['WELCOME', 'SNAPSHOT', 'DELTA', 'RECEIPT', 'EVENT', 'ERROR', 'HEARTBEAT_ACK'])
MAX_INT = 9007199254740991
ID = re.compile(r'[A-Za-z0-9._:-]{1,128}\Z', re.ASCII)


def identifier(value):
    if type(value) is not str or not ID.fullmatch(value):
        raise BoundaryError()


def integer(value):
    if type(value) is not int or not 0 <= value <= MAX_INT:
        raise BoundaryError()


def exact(obj, required, optional=()):
    if type(obj) is not dict or set(obj) - set(required) - set(optional) or not set(required) <= set(obj):
        raise BoundaryError()


def tree(value, depth=0):
    if depth > 24:
        raise BoundaryError()
    if type(value) is dict:
        for key, item in value.items():
            if type(key) is not str or len(key) > 128:
                raise BoundaryError()
            tree(item, depth + 1)
    elif type(value) is list:
        for item in value:
            tree(item, depth + 1)
    elif type(value) is int:
        if not -MAX_INT <= value <= MAX_INT:
            raise BoundaryError()
    elif type(value) is str:
        try:
            value.encode('utf8', 'strict')
        except UnicodeError as error:
            raise BoundaryError() from error
    elif value is not None and type(value) is not bool:
        # This v2 profile uses exact integers; floats require a future declared schema.
        raise BoundaryError()


def validate(envelope, direction):
    if direction not in ('in', 'out'):
        raise BoundaryError()
    tree(envelope)
    exact(envelope, ['schema_version', 'kind', 'message_id', 'application_id', 'epoch', 'payload'],
          ['correlation_id', 'commit_id', 'delivery_sequence'] if direction == 'out' else [])
    if type(envelope['schema_version']) is not int or envelope['schema_version'] != 2:
        raise BoundaryError('UNSUPPORTED_VERSION')
    for key in ['message_id', 'application_id', 'epoch', 'correlation_id', 'commit_id']:
        if key in envelope:
            identifier(envelope[key])
    if 'delivery_sequence' in envelope:
        integer(envelope['delivery_sequence'])
    kind = envelope['kind']
    if type(kind) is not str or kind not in (INBOUND if direction == 'in' else OUTBOUND):
        raise BoundaryError()
    body = envelope['payload']
    if type(body) is not dict:
        raise BoundaryError()
    if direction == 'out' and 'correlation_id' not in envelope:
        raise BoundaryError()
    fields = {
        'HELLO': (['protocol'], []), 'INTENT': (['request_id', 'operation', 'arguments', 'expected_revision'], []),
        'SYNC_REQUEST': (['view_id', 'revision'], []), 'ACK': (['delivery_sequence'], []), 'HEARTBEAT': ([], []),
        'WELCOME': (['protocol', 'view_id'], []), 'HEARTBEAT_ACK': ([], []),
        'SNAPSHOT': (['view_id', 'epoch', 'revision', 'digest', 'view'], ['state_revision']),
        'DELTA': (['view_id', 'epoch', 'base_revision', 'revision', 'commit_id', 'changes', 'digest'], ['state_revision']),
        'RECEIPT': (['status', 'request_id'], ['request_digest', 'revision', 'previous_root', 'root', 'commit_id', 'native_execution', 'inward', 'outward', 'code']),
        'ERROR': (['code'], []), 'EVENT': (['name', 'data'], []),
    }
    exact(body, *fields[kind])
    for key in ['view_id', 'request_id', 'operation', 'epoch', 'digest', 'commit_id', 'name']:
        if key in body:
            identifier(body[key])
    for key in ['revision', 'base_revision', 'expected_revision', 'delivery_sequence', 'state_revision']:
        if key in body:
            integer(body[key])
    if kind in ('HELLO', 'WELCOME') and (type(body['protocol']) is not int or body['protocol'] != 2):
        raise BoundaryError('UNSUPPORTED_VERSION')
    if kind == 'INTENT' and type(body['arguments']) is not dict:
        raise BoundaryError()
    if kind == 'RECEIPT' and body['status'] not in ('REJECTED', 'COMMITTED', 'OBSERVED', 'FAULTED_OR_UNKNOWN'):
        raise BoundaryError()
    if 'code' in body and (type(body['code']) is not str or body['code'] not in CODES):
        raise BoundaryError()
    if kind == 'SNAPSHOT' and type(body['view']) is not dict:
        raise BoundaryError()
    if 'epoch' in body and body['epoch'] != envelope['epoch']:
        raise BoundaryError()
    if 'commit_id' in envelope and 'commit_id' in body and envelope['commit_id'] != body['commit_id']:
        raise BoundaryError()
    if kind == 'DELTA':
        exact(body['changes'], ['replace_view'])
        if type(body['changes']['replace_view']) is not dict:
            raise BoundaryError()
        if type(body['changes']) is not dict or body['revision'] != body['base_revision'] + 1:
            raise BoundaryError()
    return envelope
