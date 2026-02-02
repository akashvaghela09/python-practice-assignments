# Task: Compute the maximum sum of any consecutive window of length k.
# Constraints:
# - Do not use external libraries.
# - Use sequence slicing and/or incremental updates.
# Expected outcome:
# For the given data and k, max_sum should be 12 (from window [3, 4, 5]).

data = [1, -2, 3, 4, 5, -1]
k = 3

# Initialize max_sum appropriately.
max_sum = __

# Iterate over all windows and update max_sum.
for i in range(__, __):
    window_sum = __
    if window_sum > max_sum:
        max_sum = window_sum

print(max_sum)
