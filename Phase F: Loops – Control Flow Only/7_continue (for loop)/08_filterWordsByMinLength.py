# From the list of words, collect only those with length >= min_len.
# Use continue to skip shorter words. Print the filtered words joined by a single space.
# Expected outcome (exact):
# elephant giraffe

words = ["cat", "elephant", "dog", "giraffe", "ant"]
min_len = 5

kept = []
for w in words:
    # TODO: if len(w) < min_len, continue
    
    kept.append(w)

print(" ".join(kept))
