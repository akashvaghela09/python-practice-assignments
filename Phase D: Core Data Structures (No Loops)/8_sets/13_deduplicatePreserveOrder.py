# Goal: Remove duplicates from a list while preserving original order.
# Expected outcome: It prints exactly:
# [3, 1, 2, 5, 4]

items = [3, 1, 3, 2, 1, 5, 2, 4, 5]

seen = set()
result = []
for x in items:
    ____  # TODO: if x not in seen, add to seen and append to result

print(result)
