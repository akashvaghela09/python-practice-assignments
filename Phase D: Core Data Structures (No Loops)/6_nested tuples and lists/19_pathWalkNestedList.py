# Goal: Follow a path of indices into a nested structure
# Expected outcome: running this file prints exactly: 99

# The structure can contain lists and tuples mixed.
data = [
    ("ignore", [0, 1, 2]),
    ["x", ("y", [10, 99])]
]

path = [1, 1, 1, 1]  # data[1][1][1][1] -> 99

# TODO: walk the path iteratively (no hardcoded indexing) to get the final value
current = data

# for idx in path:
#     ...

value = None

print(value)
