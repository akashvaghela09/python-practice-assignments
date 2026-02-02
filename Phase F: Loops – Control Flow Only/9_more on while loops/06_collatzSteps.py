# Compute how many steps it takes to reach 1 using the Collatz process.
# Rule: if n is even, n = n//2 else n = 3*n + 1
# Input: integer n (n > 0)
# Output: a single integer: number of steps to reach 1
# Expected outcome example: input 6 -> output 8

n = int(input().strip())
steps = 0

# TODO: while n != 1:
# - apply Collatz rule
# - increment steps

print(steps)
