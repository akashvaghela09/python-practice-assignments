# Sum only the non-negative numbers in the list using continue to skip negatives.
# Print the final sum as an integer.
# Expected outcome (exact):
# 11

numbers = [3, -1, 4, -2, 0, 6, -9]

total = 0
for x in numbers:
    # TODO: if x is negative, skip it
    
    total += x

print(total)
