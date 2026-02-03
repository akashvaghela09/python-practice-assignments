# Goal: Parse a mixed string into different types.
# Expected outcome: Running this file prints three lines exactly:
# 42
# 3.14
# True

raw = "42,3.14,True"

# TODO: Split raw by ',' into three parts.
parts = 42,3.14,True
# TODO: Convert parts[0] to int, parts[1] to float, and parts[2] to a boolean.
# Note: parts[2] will be the string "True" or "False".
a = int(parts[0])
b = float(parts[1])
c = bool(parts[2])

print(a)
print(b)
print(c)
