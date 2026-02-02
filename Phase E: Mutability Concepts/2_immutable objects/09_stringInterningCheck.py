# Goal: Compare equality vs identity for strings built differently.
# Note: Do not rely on interning for identity; demonstrate that == is correct.
# Expected outcome:
# - Prints: "equal: True"
# - Prints: "identical: False" (build one string dynamically so identity differs)

# TODO: create a as literal "python"
a = None

# TODO: create b dynamically so it equals "python" but is typically a different object
# Hint: use ''.join([...]) or format
b = None

print("equal:", a == b)
print("identical:", a is b)
