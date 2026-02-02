# Goal: Find the most frequent non-space character in a string.
# If there's a tie, choose the alphabetically smallest character.
# Expected outcome when run:
# a

s = "a b a c c"
counts = {}

for ch in s:
    if ch == " ":
        continue
    # TODO: count characters
    pass

# TODO: determine the most frequent character with tie-break rule
most_common = None

print(most_common)
