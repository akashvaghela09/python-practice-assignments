# Goal: Remove stopwords using 'not in'.
# Expected outcome:
# - Prints exactly:
#   keep: ['quick', 'brown', 'fox']

words = ["the", "quick", "brown", "fox"]
stopwords = {"the", "a", "an"}

keep = []
for w in words:
    # TODO: Append only words not in stopwords
    if None:
        keep.append(w)

print(f"keep: {keep}")
