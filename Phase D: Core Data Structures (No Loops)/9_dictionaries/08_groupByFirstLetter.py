# Goal: Group words by their first letter (values should be lists).
# Expected outcome when run:
# {'a': ['ant', 'art'], 'b': ['bat', 'ball'], 'c': ['cat']}

words = ["ant", "bat", "art", "ball", "cat"]
groups = {}

for word in words:
    first = word[0]
    # TODO: append word into groups[first], creating a list if needed
    pass

print(groups)
