from raeon_model import Color, PrimeState
from raeon_model.prime import PrimeDirection

# Yellow Prime damaged to Red:
p = PrimeState(rank=Color.YELLOW, health=Color.RED, shield=Color.ZERO,
               direction=PrimeDirection.HYBRID)

print("Initial:", p.health_color.name, p.shield_color.name)

# Genesis example: Blue (+5) enters Red-health Yellow Prime.
result = p.receive_friendly_color(Color.BLUE)
print("After +Blue:", result)
print("State:", p.health_color.name, "health /", p.shield_color.name, "shield")

# Spend Orange (2) transduction.
p.reactivate()
shot = p.spend_transduction(Color.ORANGE, "degrade")
print("Spend Orange:", shot)
print("Remaining shield:", p.shield_color.name)
