# Goal: Sort only the middle slice of a list, leaving ends untouched.
# Task: Sort indices 2 through 6 inclusive in ascending order.
# Expected outcome: nums must become [100, 50, 1, 2, 3, 4, 9, 8, 7].

nums = [100, 50, 4, 3, 2, 1, 9, 8, 7]

start = 2
end_inclusive = 6

# TODO:
# 1) extract the sublist nums[start:end_inclusive+1]
# 2) sort it ascending
# 3) put it back into nums in the same positions

print(nums)
