import math
reveal_type(math.pi)

# can inspect with `circumference.__annotations__`
def circumference(radius: float) -> float:
    # type: (float) -> float
    return 2 * math.pi * radius

# can inspect on module level with `__annotations__`
circ = circumference(10)

reveal_locals()