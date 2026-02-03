# Goal: Avoid direct float equality; use a tolerance check.
# Expected outcome (exact lines):
# False
# True

x = 0.1 + 0.2

print(x == 0.3)

tolerance = 1e-9
is_close = abs(x - 0.3) < tolerance # compare absolute difference to tolerance

print(is_close)
