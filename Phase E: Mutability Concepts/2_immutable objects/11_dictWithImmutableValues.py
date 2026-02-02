# Goal: Update a mapping by replacing (not mutating) an immutable value.
# Expected outcome:
# - Prints: "before: (1, 2)"
# - Prints: "after: (1, 2, 3)"

prefs = {"dims": (1, 2)}

print("before:", prefs["dims"])

# TODO: append 3 to the tuple by creating a new tuple and reassigning prefs["dims"]

print("after:", prefs["dims"])
