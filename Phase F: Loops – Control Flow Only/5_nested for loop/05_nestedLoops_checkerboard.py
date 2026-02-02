# Goal: Create a checkerboard pattern using nested loops.
# Use 'X' and '.' alternating by (row+col) parity.
# Expected outcome when size=5:
# X.X.X
# .X.X.
# X.X.X
# .X.X.
# X.X.X

size = 5

lines = []

# TODO: Use nested loops over r and c from 0..size-1.
# If (r + c) is even -> 'X' else '.'
# Build each row string and append to lines.


print("\n".join(lines))