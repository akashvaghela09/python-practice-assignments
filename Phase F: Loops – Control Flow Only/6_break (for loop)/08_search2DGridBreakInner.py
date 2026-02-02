# Goal: In the grid below, find the first occurrence of 'X'.
# Print its position as 'row,col' (zero-based) and stop scanning further in that row using break.
# (Only break out of the inner loop; the outer loop can continue.)
# Expected outcome:
# 1,2

grid = [
    [".", ".", ".", "."],
    [".", ".", "X", "."],
    ["X", ".", ".", "."]
]

for r in range(len(grid)):
    for c in range(len(grid[r])):
        # TODO: if grid[r][c] == 'X', print f"{r},{c}" and break
        pass
