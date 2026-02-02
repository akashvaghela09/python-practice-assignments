# Goal: Implement a boolean decision function using multiple conditions.
# Expected outcome:
# Running this file prints exactly:
# True
# False
# False
# True

def is_password_acceptable(pw: str) -> bool:
    """Return True only if all rules pass:
    - length is at least 8
    - contains at least one digit
    - does NOT contain any spaces
    - is not exactly "password" (case-sensitive)
    """
    # TODO: Implement using boolean expressions.
    has_min_len = ???
    has_digit = ???
    has_space = ???
    is_banned = ???

    acceptable = ???
    return acceptable

print(is_password_acceptable("tiger123"))     # True
print(is_password_acceptable("password"))     # False
print(is_password_acceptable("no digits"))    # False
print(is_password_acceptable("abc123 45"))    # True
