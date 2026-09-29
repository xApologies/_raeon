from dataclasses import dataclass
from enum import Enum
from .colors import Color

class PrimeDirection(str, Enum):
    RESTORE = "RESTORE"
    DEGRADE = "DEGRADE"
    HYBRID = "HYBRID"

@dataclass
class PrimeState:
    """Executable core of the currently established Prime state model.

    rank:
        Printed/native Prime rank. Current design permits Yellow..White.
        rank value supplies intrinsic max health and current modeled shield capacity.

    health:
        Current intrinsic health.

    shield:
        Active color shield / spendable transduction reservoir.

    Overflow is *returned*, not silently discarded, because final overflow semantics
    remain OPEN.
    """
    rank: Color
    health: int | None = None
    shield: int = 0
    direction: PrimeDirection = PrimeDirection.HYBRID
    destroyed: bool = False
    used: bool = False

    def __post_init__(self):
        if self.rank < Color.YELLOW or self.rank > Color.WHITE:
            raise ValueError("Prime rank must currently be Yellow through White")
        if self.health is None:
            self.health = int(self.rank)
        self.health = max(0, min(int(self.health), self.max_health))
        self.shield = max(0, min(int(self.shield), self.max_shield))
        self.destroyed = self.health == 0

    @property
    def max_health(self) -> int:
        return int(self.rank)

    @property
    def max_shield(self) -> int:
        # Current live model: rank is both health and shield/transduction ceiling.
        return int(self.rank)

    @property
    def health_color(self) -> Color:
        return Color.from_value(self.health)

    @property
    def shield_color(self) -> Color:
        return Color.from_value(self.shield)

    @property
    def active(self) -> bool:
        return (not self.destroyed) and self.shield > 0

    def receive_friendly_color(self, amount: int) -> dict:
        """Heal intrinsic health first; remainder fills shield.
        Returns an explicit overflow field because overflow policy is unresolved.
        """
        if self.destroyed:
            raise ValueError("destroyed Prime cannot ordinarily receive color")
        amount = max(0, int(amount))
        missing = self.max_health - self.health
        healed = min(missing, amount)
        self.health += healed
        amount -= healed

        shield_room = self.max_shield - self.shield
        shield_added = min(shield_room, amount)
        self.shield += shield_added
        amount -= shield_added

        return {
            "healed": healed,
            "shield_added": shield_added,
            "overflow": amount,
            "health": self.health,
            "shield": self.shield,
        }

    def receive_degradation(self, amount: int) -> dict:
        """Hostile degradation hits shield first, then intrinsic health."""
        if self.destroyed:
            return {"shield_lost": 0, "health_lost": 0, "overkill": int(amount)}
        amount = max(0, int(amount))

        shield_lost = min(self.shield, amount)
        self.shield -= shield_lost
        amount -= shield_lost

        health_lost = min(self.health, amount)
        self.health -= health_lost
        amount -= health_lost

        if self.health == 0:
            self.destroyed = True
            self.shield = 0

        return {
            "shield_lost": shield_lost,
            "health_lost": health_lost,
            "overkill": amount,
            "health": self.health,
            "shield": self.shield,
            "destroyed": self.destroyed,
        }

    def spend_transduction(self, amount: int, mode: str) -> dict:
        """Spend shield as transduction magnitude.

        mode is 'restore' or 'degrade'. Directionality is enforced.
        Target application is deliberately outside this object.
        """
        if self.destroyed:
            raise ValueError("destroyed Prime cannot transduce")
        if self.used:
            raise ValueError("Prime is currently used; reactivation timing is unresolved")
        amount = int(amount)
        if amount <= 0:
            raise ValueError("transduction amount must be positive")
        if amount > self.shield:
            raise ValueError("cannot spend more color than current shield")

        mode = mode.lower()
        if mode not in {"restore", "degrade"}:
            raise ValueError("mode must be restore or degrade")
        if self.direction == PrimeDirection.RESTORE and mode != "restore":
            raise ValueError("restore-only Prime cannot degrade")
        if self.direction == PrimeDirection.DEGRADE and mode != "degrade":
            raise ValueError("degrade-only Prime cannot restore")

        self.shield -= amount
        self.used = True
        return {
            "mode": mode,
            "magnitude": amount,
            "remaining_shield": self.shield,
            "remaining_shield_color": self.shield_color.name,
        }

    def reactivate(self):
        """Minimal state hook only. Exact legal source/timing is still OPEN."""
        if self.destroyed:
            raise ValueError("destroyed Prime cannot ordinarily reactivate")
        self.used = False
