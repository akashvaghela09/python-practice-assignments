# Goal: Replace a specific consecutive pattern (sublist) in place.
# Pattern: [0, 0, 0] should be replaced with [1, 1]. Replace all non-overlapping occurrences from left to right.
# Expected outcome: printing the list shows [5, 1, 1, 2, 1, 1, 9]

data = [5, 0, 0, 0, 2, 0, 0, 0, 9]
pattern = [0, 0, 0]
replacement = [1, 1]

# TODO:
# Walk through the list and whenever you find 'pattern' starting at the current index,
# replace that slice with 'replacement', then continue scanning from after the inserted replacement.
# (Do not use .replace() since this is a list, not a string.)

print(data)
