# Goal: Approximate sqrt(value) using Newton's method until the approximation changes by less than tolerance.
# Newton update: x = (x + value/x) / 2
# Start with x = value (for value > 0). Use a while loop.
# For value = 25.0 and tolerance = 1e-6, expected outcome (exact line, rounded to 6 decimals):
# Approx sqrt: 5.000000

value = 25.0
tolerance = 1e-6

# TODO: initialize x and prev so the loop works correctly
x = __________
prev = __________

# TODO: loop until the absolute change is less than tolerance
while __________:
    prev = x
    x = (x + value / x) / 2

print("Approx sqrt:", f"{x:.6f}")
