# Goal: Observe that ints are immutable by comparing identities before/after an operation.
# Expected outcome:
# - Prints two different ids for x and y
# - Prints: "x is y? False"

x = 10
# TODO: store id of x in before
before = None

y = x + 1  # creates a new int object
# TODO: store id of y in after
after = None

print(before)
print(after)
print("x is y?", x is y)
