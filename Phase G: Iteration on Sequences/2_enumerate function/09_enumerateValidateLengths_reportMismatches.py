# Goal: Compare each word to expected length and report mismatches with index.
# Expected outcome:
# Index 1 expected 4 got 5
# Index 3 expected 3 got 2

words = ["tree", "house", "code", "py"]
expected_lengths = [4, 4, 4, 3]

# TODO:
# Use enumerate to iterate over words with indices.
# Compare len(word) to expected_lengths[index].
# Print only mismatches in the format:
# "Index <i> expected <expected> got <actual>"
for ___, ___ in ___:
    expected = expected_lengths[___]
    actual = len(___)
    if ___:
        print(___)
