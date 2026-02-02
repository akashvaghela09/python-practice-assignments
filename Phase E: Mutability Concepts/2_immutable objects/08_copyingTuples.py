# Goal: Show that 'copying' a tuple via slicing returns the same object.
# Expected outcome:
# - Prints: "same object: True"
# - Prints: "same value: True"

t = ("a", "b", "c")

# TODO: create t2 as a slice copy of t
t2 = None

print("same object:", t2 is t)
print("same value:", t2 == t)
