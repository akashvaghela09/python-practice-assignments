# Goal: Create an immutable object using a frozen dataclass and observe mutation failure.
# Expected outcome:
# - Prints: "Point(x=2, y=5)"
# - Prints: "mutate error: FrozenInstanceError" (or a subclass name depending on Python)

from dataclasses import dataclass

# TODO: define a frozen dataclass Point with fields x:int and y:int

# TODO: instantiate p = Point(2, 5)
p = None
print(p)

try:
    # TODO: attempt to modify p.x
    pass
except Exception as e:
    print("mutate error:", type(e).__name__)
