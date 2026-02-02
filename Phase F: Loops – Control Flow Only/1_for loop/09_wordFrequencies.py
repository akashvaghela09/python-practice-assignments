# Count word frequencies using a for loop.
# Split on whitespace, treat words as case-insensitive.
# Expected outcome: print {'to': 3, 'be': 2, 'or': 1}

text = "To be or to be to"
words = text.lower().split()
counts = {}

# TODO: Use a for loop to count occurrences into the dictionary
for w in ____:
    if ____:
        counts[w] = ____
    else:
        counts[w] = ____

print(counts)
