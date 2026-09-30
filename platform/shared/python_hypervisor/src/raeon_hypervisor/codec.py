import json
import struct
import zlib
from .validation import validate
from .errors import BoundaryError

HEADER = struct.Struct('>8sBBHII')
MAGIC = b'RAEONH2!'
MAX_PAYLOAD = 1048576


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf8')


def encode(envelope, direction='out', max_payload=MAX_PAYLOAD):
    validate(envelope, direction)
    payload = canonical(envelope)
    if len(payload) > max_payload:
        raise BoundaryError()
    return HEADER.pack(MAGIC, 2, 0, 0, len(payload), zlib.crc32(payload)) + payload


def header(frame, max_payload=MAX_PAYLOAD):
    if len(frame) < HEADER.size:
        raise BoundaryError()
    magic, major, minor, flags, size, checksum = HEADER.unpack_from(frame)
    if magic != MAGIC:
        raise BoundaryError()
    if major != 2 or minor != 0 or flags != 0:
        raise BoundaryError('UNSUPPORTED_VERSION')
    if size > max_payload:
        raise BoundaryError()
    return size, checksum


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise BoundaryError()
        result[key] = value
    return result


def reject_constant(value):
    raise BoundaryError()


def decode(frame, direction='in', max_payload=MAX_PAYLOAD):
    if type(frame) is not bytes or len(frame) > max_payload + HEADER.size:
        raise BoundaryError()
    size, checksum = header(frame, max_payload)
    payload = frame[HEADER.size:]
    if len(payload) != size or zlib.crc32(payload) != checksum:
        raise BoundaryError()
    try:
        value = json.loads(payload.decode('utf8', 'strict'), object_pairs_hook=unique, parse_constant=reject_constant)
        return validate(value, direction)
    except (UnicodeError, ValueError, RecursionError, TypeError, KeyError) as error:
        if isinstance(error, BoundaryError):
            raise
        raise BoundaryError() from error
