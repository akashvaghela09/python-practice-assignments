# Goal: Validate that a username contains only allowed characters using 'in' / 'not in'.
# Allowed characters: lowercase letters, digits, underscore.
# Expected outcome:
# - Prints exactly:
#   VALID
#   INVALID

allowed = "abcdefghijklmnopqrstuvwxyz0123456789_"

usernames = ["dev_42", "Bad-Name"]

for name in usernames:
    # TODO: Set is_valid to True only if every character in name is in allowed
    is_valid = None

    if is_valid:
        print("VALID")
    else:
        print("INVALID")
