# Goal: Implement a stable sort (do not use list.sort() or sorted()).
# Task: Write stable_sort_by_key(items, key_func) that returns a NEW list.
# Constraint: Must be stable (original order preserved for equal keys).
# Hint: Implement merge sort.
# Expected outcome:
# When sorting by score ascending, the returned list must be:
# [('Ben', 2), ('Dan', 2), ('Ava', 3), ('Cara', 3)]
# (Ben must stay before Dan; Ava must stay before Cara).

def stable_sort_by_key(items, key_func):
    # TODO: implement stable merge sort that uses key_func
    # Do NOT mutate the input list.
    pass

pairs = [('Ava', 3), ('Ben', 2), ('Cara', 3), ('Dan', 2)]

# TODO: call stable_sort_by_key with key_func that extracts the score
sorted_pairs = None

print(sorted_pairs)
