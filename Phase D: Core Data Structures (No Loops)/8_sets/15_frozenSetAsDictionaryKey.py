# Goal: Use frozenset to group anagrams as dictionary keys (order-independent letters).
# Expected outcome: It prints exactly 3 on a single line.
# Explanation: There should be 3 anagram groups: {'eat','tea','ate'}, {'tan','nat'}, {'bat'}.

words = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']

groups = {}  # maps frozenset/tuple-like key -> list of words
for w in words:
    key = ____  # TODO: create a hashable key representing letters in w (sorted) using frozenset or tuple
    ____       # TODO: add w into groups under that key

print(len(groups))
