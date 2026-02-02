# Goal: Validate a password with multiple requirements.
# Requirements:
# - length >= 8
# - must contain at least one digit OR at least one special character from '!@#'
# - must NOT contain spaces
# Print exactly: VALID or INVALID
# Expected outcome:
# With password='abcde1fg' => VALID
# With password='abcd e1fg' => INVALID

password = "abcde1fg"

has_digit = any(ch.isdigit() for ch in password)
has_special = any(ch in "!@#" for ch in password)
has_space = (" " in password)

# TODO: Combine conditions using 'and', 'or', and 'not'.
if ____:
    print("VALID")
else:
    print("INVALID")
