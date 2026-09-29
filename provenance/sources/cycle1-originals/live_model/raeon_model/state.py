from dataclasses import dataclass, field
from .sandbox import Sandbox
from .prime import PrimeState

@dataclass
class PlayerState:
    player_id: str
    graveyard: list[str] = field(default_factory=list)
    base_sandboxes: list[Sandbox] = field(default_factory=lambda: [
        Sandbox("A", permanent=True),
        Sandbox("B", permanent=True),
        Sandbox("C", permanent=True),
    ])
    extra_sandboxes: list[Sandbox] = field(default_factory=list)
    primes: list[PrimeState] = field(default_factory=list)
    hand: list[str] = field(default_factory=list)

    @property
    def sandboxes(self):
        return self.base_sandboxes + self.extra_sandboxes
