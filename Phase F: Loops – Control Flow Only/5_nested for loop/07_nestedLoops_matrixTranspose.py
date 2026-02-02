# Goal: Compute the transpose of a matrix using nested loops.
# Expected outcome for matrix below:
# [[1, 4],
#  [2, 5],
#  [3, 6]]

matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

rows = len(matrix)
cols = len(matrix[0])

transpose = []

# TODO: Use nested loops.
# Outer loop should iterate over column index (0..cols-1).
# Inner loop should iterate over row index (0..rows-1).
# Build each transposed row and append to transpose.


print(transpose)