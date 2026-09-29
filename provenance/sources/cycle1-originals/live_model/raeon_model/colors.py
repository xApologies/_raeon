from enum import IntEnum

class Color(IntEnum):
    ZERO = 0
    RED = 1
    ORANGE = 2
    YELLOW = 3
    GREEN = 4
    BLUE = 5
    VIOLET = 6
    WHITE = 7

    @classmethod
    def from_value(cls, value: int) -> "Color":
        value = max(0, min(7, int(value)))
        return cls(value)

    def step_name(self) -> str:
        return self.name.title()
