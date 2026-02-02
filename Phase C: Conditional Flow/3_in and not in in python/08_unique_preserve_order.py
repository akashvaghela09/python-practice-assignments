# Goal: Build a list of unique items while preserving order using 'not in'.
# Expected outcome:
# - Prints exactly:
#   unique: [3, 1, 2, 4]

items = [3, 1, 2, 3, 2, 4, 1]

unique = []
for x in items:
    # TODO: Add x only if it is not already in unique
    if None:
        unique.append(x)

print(f"unique: {unique}")
