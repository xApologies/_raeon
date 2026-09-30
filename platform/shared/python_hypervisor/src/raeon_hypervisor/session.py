from collections import deque
from dataclasses import dataclass, field


@dataclass
class Session:
    authority: dict
    buffer: bytearray = field(default_factory=bytearray)
    outgoing: deque = field(default_factory=deque)
    queued_bytes: int = 0
    pending: int = 0
    sequence: int = 0
    acknowledged: int = 0
