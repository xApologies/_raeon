from .errors import BoundaryError


def reserve(session, limit, maximum_response_bytes):
    if session.queued_bytes + maximum_response_bytes > limit:
        raise BoundaryError('BACKPRESSURE')


def drain(session, max_frames, max_bytes):
    if type(max_frames) is not int or type(max_bytes) is not int or min(max_frames, max_bytes) < 0:
        raise BoundaryError()
    frames = []
    used = 0
    while session.outgoing and len(frames) < max_frames:
        frame = session.outgoing[0]
        if used + len(frame) > max_bytes:
            break
        frames.append(session.outgoing.popleft())
        used += len(frame)
        session.queued_bytes -= len(frame)
    return tuple(frames)
