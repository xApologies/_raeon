from dataclasses import dataclass, field
from .colors import Color
from .rules import manifold_color_for_generator_count

@dataclass
class LocalManifold:
    manifold_id: str
    generator_ids: list[str]
    current_color: Color
    max_color: Color
    sandbox_ids: list[str] = field(default_factory=list)
    active: bool = True
    used: bool = False

    @classmethod
    def from_valid_closure(cls, manifold_id: str, generator_ids: list[str], sandbox_ids=None):
        """Construct ONLY after a topology solver has established a valid closure."""
        max_color = manifold_color_for_generator_count(len(generator_ids))
        return cls(
            manifold_id=manifold_id,
            generator_ids=list(generator_ids),
            max_color=max_color,
            current_color=max_color,
            sandbox_ids=list(sandbox_ids or []),
        )

    def restore(self, amount: int):
        self.current_color = Color.from_value(
            min(int(self.max_color), int(self.current_color) + max(0, int(amount)))
        )
        return self.current_color

    def degrade(self, amount: int):
        self.current_color = Color.from_value(
            max(0, int(self.current_color) - max(0, int(amount)))
        )
        if self.current_color == Color.ZERO:
            self.active = False
        return self.current_color

@dataclass
class EmergentField:
    field_id: str
    support_manifold_ids: list[str]
    color: Color
    directly_targetable: bool = False
    active: bool = True

    def reevaluate_support(self, active_support_ids: set[str]):
        self.active = all(mid in active_support_ids for mid in self.support_manifold_ids)
        return self.active
