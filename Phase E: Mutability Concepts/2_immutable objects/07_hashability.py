# Goal: Determine what can be used as dictionary keys (hashable/immutable).
# Expected outcome:
# - Prints: "tuple_key_ok: True"
# - Prints: "list_key_error: TypeError"

# TODO: create a dict using a tuple key (1, 2)
d = None

# TODO: set tuple_key_ok to True if lookup by (1, 2) yields "ok"
tuple_key_ok = None

try:
    # TODO: attempt to use a list [1, 2] as a dict key
    pass
except Exception as e:
    print("list_key_error:", type(e).__name__)

print("tuple_key_ok:", tuple_key_ok)
