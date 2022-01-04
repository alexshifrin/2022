import math
reveal_type(math.pi)

def circumference(radius: float) -> float:
    return 2 * math.pi * radius

circ = circumference(10)

reveal_locals()