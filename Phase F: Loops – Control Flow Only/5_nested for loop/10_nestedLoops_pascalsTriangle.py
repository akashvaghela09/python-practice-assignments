# Goal: Generate Pascal's triangle with nested loops.
# Build a list of lists, where each row is computed from the previous row.
# Expected outcome when n=6:
# [[1],
#  [1, 1],
#  [1, 2, 1],
#  [1, 3, 3, 1],
#  [1, 4, 6, 4, 1],
#  [1, 5, 10, 10, 5, 1]]

n = 6

triangle = []

# TODO: Use an outer loop to build each row index r from 0..n-1.
# Each row starts and ends with 1.
# For middle positions, use values from the previous row:
# prev[c-1] + prev[c]
# Use an inner loop to fill the middle values.


print(triangle)