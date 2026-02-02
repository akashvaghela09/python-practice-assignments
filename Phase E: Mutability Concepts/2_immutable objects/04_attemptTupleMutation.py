# Goal: Intentionally trigger and catch a TypeError when trying to mutate a tuple.
# Expected outcome:
# - Prints: "error: TypeError"
# - Prints: "tuple still: (1, 2, 3)"

t = (1, 2, 3)

try:
    # TODO: attempt to change the middle element to 99
    pass
except Exception as e:
    print("error:", type(e).__name__)

print("tuple still:", t)
