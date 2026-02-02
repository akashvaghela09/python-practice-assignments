# Goal: Build an immutable, hashable composite key from nested data.
# Expected outcome:
# - Prints: "key hashable: True"
# - Prints: "lookup: found"

user = {
    "name": "Ada",
    "roles": ["admin", "editor"],
    "region": "EU"
}

# TODO: create an immutable key using (name, tuple(roles), region)
key = None

# TODO: create a dict cache mapping key -> "found"
cache = None

# TODO: set key_hashable to True if hash(key) works without raising
key_hashable = None

print("key hashable:", key_hashable)
print("lookup:", cache.get(key))
