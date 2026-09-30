"""Single semantic execution owner, bounded input and byte-only delivery."""
from collections import deque
import copy
import threading
import uuid

from .codec import HEADER, decode, encode, header
from .errors import BoundaryError, CODES
from .session import Session
from .sync import ViewHistory
from . import delivery
from .validation import identifier, integer


class Hypervisor:
    def __init__(self, horizon_adapter, config):
        self.adapter = horizon_adapter
        self.config = copy.deepcopy(config)
        for key in ('max_payload_bytes', 'inbound_per_session', 'outbound_bytes_per_session', 'delta_history', 'diagnostics'):
            if type(self.config[key]) is not int or self.config[key] <= 0:
                raise BoundaryError()
        self.sessions = {}
        self.pending = deque()
        self.views = {}
        self.diagnostics = deque(maxlen=self.config['diagnostics'])
        self._mutex = threading.RLock()
        self.closed = False

    @property
    def epoch(self):
        return self.adapter.epoch

    def bind_session(self, trusted_session_context):
        with self._mutex:
            if self.closed:
                raise BoundaryError('UNBOUND_SESSION')
            for name in ('actor', 'application_id', 'view_id'):
                identifier(trusted_session_context.get(name))
            if len(self.sessions) >= self.config.get('sessions', 64):
                raise BoundaryError('BACKPRESSURE')
            handle = uuid.uuid4().hex
            self.sessions[handle] = Session(copy.deepcopy(trusted_session_context))
            return handle

    def _session(self, handle):
        if self.closed or handle not in self.sessions:
            raise BoundaryError('UNBOUND_SESSION')
        return self.sessions[handle]

    def receive(self, session_handle, frame_bytes):
        with self._mutex:
            try:
                session = self._session(session_handle)
                limit = self.config['max_payload_bytes']
                if type(frame_bytes) is not bytes or len(session.buffer) + len(frame_bytes) > limit + HEADER.size:
                    raise BoundaryError()
                session.buffer.extend(frame_bytes)
                if len(session.buffer) < HEADER.size:
                    return {'status': 'BUFFERED'}
                size, _ = header(session.buffer, limit)
                if len(session.buffer) < size + HEADER.size:
                    return {'status': 'BUFFERED'}
                frame = bytes(session.buffer)
                session.buffer.clear()
                message = decode(frame, 'in', limit)
                if message['application_id'] != session.authority['application_id']:
                    raise BoundaryError('UNKNOWN_APPLICATION')
                if message['epoch'] != self.epoch:
                    raise BoundaryError('STALE_PRECONDITION')
                if session.pending >= self.config['inbound_per_session']:
                    raise BoundaryError('BACKPRESSURE')
                session.pending += 1
                self.pending.append((session_handle, message))
                return {'status': 'QUEUED'}
            except BoundaryError as error:
                if session_handle in self.sessions:
                    self.sessions[session_handle].buffer.clear()
                return {'status': 'REJECTED', 'code': error.code}

    def _emit(self, session, message, kind, body, commit_id=None):
        sequence = session.sequence + 1
        envelope = {'schema_version': 2, 'kind': kind, 'message_id': uuid.uuid4().hex,
                    'application_id': session.authority['application_id'], 'epoch': self.epoch,
                    'payload': copy.deepcopy(body), 'correlation_id': message['message_id'], 'delivery_sequence': sequence}
        if commit_id:
            envelope['commit_id'] = commit_id
        frame = encode(envelope, 'out', self.config['max_payload_bytes'])
        delivery.reserve(session, self.config['outbound_bytes_per_session'], len(frame))
        session.outgoing.append(frame)
        session.queued_bytes += len(frame)
        session.sequence = sequence

    def _view(self, session, commit_id='observation'):
        authority = session.authority
        key = (authority['application_id'], authority['actor'], authority['view_id'], self.epoch)
        if key not in self.views and len(self.views) >= self.config.get('view_histories', 256):
            raise BoundaryError('BACKPRESSURE')
        history = self.views.setdefault(key, ViewHistory(self.config['delta_history']))
        projection = self.adapter.observe(copy.deepcopy(authority), None)
        delta = history.update(projection, commit_id)
        return history, delta

    def step(self, execution_budget=100000):
        with self._mutex:
            if type(execution_budget) is not int or not 0 < execution_budget <= 100000:
                raise BoundaryError('BUDGET_EXCEEDED')
            if self.closed or not self.pending:
                return {'status': 'IDLE'}
            handle, message = self.pending.popleft()
            if handle not in self.sessions:
                return {'status': 'SESSION_CLOSED'}
            session = self.sessions[handle]
            session.pending -= 1
            kind, body = message['kind'], message['payload']
            outcome = None
            try:
                # Reserve two maximum-sized outputs before entering the adapter.
                delivery.reserve(session, self.config['outbound_bytes_per_session'], 2 * (self.config['max_payload_bytes'] + HEADER.size))
                if message['epoch'] != self.epoch:
                    raise BoundaryError('STALE_PRECONDITION')
                if kind == 'HELLO':
                    history, _ = self._view(session)
                    self._emit(session, message, 'WELCOME', {'protocol': 2, 'view_id': session.authority['view_id']})
                    self._emit(session, message, 'SNAPSHOT', history.latest)
                elif kind == 'INTENT':
                    try:
                        outcome = self.adapter.execute(copy.deepcopy(body), copy.deepcopy(session.authority), execution_budget)
                    except Exception as execution_error:
                        if getattr(execution_error, 'code', None) in CODES:
                            raise
                        outcome = self.adapter.lookup_outcome((session.authority['application_id'], session.authority['actor'], body['request_id']))
                        if outcome is None:
                            raise
                        # A conflicting retry must not be converted into the earlier success.
                        from .codec import canonical
                        import hashlib
                        if outcome['request_digest'] != hashlib.sha256(canonical(body)).hexdigest():
                            outcome = None
                            raise BoundaryError('REQUEST_ID_CONFLICT')
                    self._emit(session, message, 'RECEIPT', outcome, outcome.get('commit_id'))
                    history, delta = self._view(session, outcome.get('commit_id', 'observation'))
                    if delta:
                        self._emit(session, message, 'DELTA', delta, outcome.get('commit_id'))
                    elif history.latest is not None:
                        self._emit(session, message, 'SNAPSHOT', history.latest)
                elif kind == 'SYNC_REQUEST':
                    if body['view_id'] != session.authority['view_id']:
                        raise BoundaryError('AUTHORITY_DENIED')
                    history, _ = self._view(session)
                    chain = history.resume(body['revision'])
                    # Arbitrary replay size is bounded by available bytes; otherwise a snapshot repairs it.
                    if chain and len(chain) <= 1:
                        for delta in chain:
                            self._emit(session, message, 'DELTA', delta, delta['commit_id'])
                    else:
                        self._emit(session, message, 'SNAPSHOT', history.latest)
                elif kind == 'ACK':
                    if body['delivery_sequence'] > session.sequence:
                        raise BoundaryError()
                    session.acknowledged = max(session.acknowledged, body['delivery_sequence'])
                elif kind == 'HEARTBEAT':
                    self._emit(session, message, 'HEARTBEAT_ACK', {})
                return {'status': 'PROCESSED', 'kind': kind}
            except Exception as error:
                code = getattr(error, 'code', str(error))
                if code not in CODES:
                    code = 'RUNTIME_FAULT'
                self.diagnostics.append({'type': type(error).__name__, 'code': code})
                if outcome and outcome.get('status') == 'COMMITTED':
                    return {'status': 'COMMITTED_DELIVERY_PENDING', 'commit_id': outcome['commit_id']}
                try:
                    if kind == 'INTENT':
                        self._emit(session, message, 'RECEIPT', {'status': 'FAULTED_OR_UNKNOWN' if code == 'RUNTIME_FAULT' else 'REJECTED',
                                                             'request_id': body['request_id'], 'code': code})
                    else:
                        self._emit(session, message, 'ERROR', {'code': code})
                except BoundaryError:
                    pass
                return {'status': 'REJECTED' if code != 'RUNTIME_FAULT' else 'FAULTED_OR_UNKNOWN', 'code': code}

    def drain(self, session_handle, max_frames=16, max_bytes=8388608):
        with self._mutex:
            return delivery.drain(self._session(session_handle), max_frames, max_bytes)

    def close_session(self, session_handle):
        with self._mutex:
            self.sessions.pop(session_handle, None)
            self.pending = deque((h, m) for h, m in self.pending if h != session_handle)
            return {'status': 'CLOSED'}

    def save_checkpoint(self, trusted_authority):
        with self._mutex:
            if self.pending:
                raise BoundaryError('ADMISSION_REJECTED')
            return self.adapter.checkpoint(copy.deepcopy(trusted_authority))

    def restore_checkpoint(self, checkpoint_ref, trusted_authority):
        with self._mutex:
            result = self.adapter.restore(checkpoint_ref, copy.deepcopy(trusted_authority), 100000)
            self.pending.clear()
            self.views.clear()
            for session in self.sessions.values():
                session.buffer.clear()
                session.outgoing.clear()
                session.pending = session.queued_bytes = session.sequence = session.acknowledged = 0
            return result

    def close(self, mode='drain', execution_budget=100000):
        with self._mutex:
            if self.closed:
                return {'status': 'CLOSED'}
            if mode not in ('drain', 'cancel'):
                raise BoundaryError()
            if mode == 'drain':
                while self.pending:
                    self.step(execution_budget)
            else:
                self.pending.clear()
            self.adapter.quiesce(execution_budget)
            self.adapter.close()
            self.closed = True
            return {'status': 'CLOSED'}
