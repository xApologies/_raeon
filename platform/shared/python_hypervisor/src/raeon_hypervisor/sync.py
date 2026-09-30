import copy
import hashlib
from collections import deque
from .codec import canonical
from .errors import BoundaryError


class ViewHistory:
    def __init__(self, limit):
        self.latest = None
        self.revision = 0
        self.deltas = deque(maxlen=limit)

    def update(self, projection, commit_id):
        projection = copy.deepcopy(projection)
        digest = hashlib.sha256(canonical(projection['view'])).hexdigest()
        if projection['digest'] != digest:
            raise BoundaryError('RUNTIME_FAULT')
        delta = None
        if self.latest is not None and self.latest['digest'] != digest:
            delta = {'view_id': projection['view_id'], 'epoch': projection['epoch'], 'base_revision': self.revision,
                     'revision': self.revision + 1, 'commit_id': commit_id, 'changes': {'replace_view': projection['view']}, 'digest': digest,
                     'state_revision': projection['state_revision']}
            self.revision += 1
            self.deltas.append(copy.deepcopy(delta))
        projection['revision'] = self.revision
        self.latest = projection
        return delta

    def resume(self, cursor):
        chain = [copy.deepcopy(d) for d in self.deltas if d['base_revision'] >= cursor]
        current = cursor
        for delta in chain:
            if delta['base_revision'] != current:
                return None
            current = delta['revision']
        return chain if current == self.revision else None
