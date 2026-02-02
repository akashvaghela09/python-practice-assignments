# Goal: Use 'in' with any()/all() for permission checks.
# Expected outcome:
# - Prints exactly:
#   missing: ['delete']

required = ["read", "write", "delete"]
user_permissions = {"read", "write"}

missing = []
# TODO: Fill missing with permissions from required that are not in user_permissions
for perm in required:
    if None:
        missing.append(perm)

print(f"missing: {missing}")
