# Task: Implement require_non_empty_string(s).
# Requirements:
# - If s is not a str, raise TypeError("s must be a str")
# - If s is empty or only whitespace, raise ValueError("s must be a non-empty string")
# - Otherwise return s stripped of leading/trailing whitespace
# Expected outcome:
# - require_non_empty_string("  hi ") returns "hi"
# - require_non_empty_string("   ") raises ValueError("s must be a non-empty string")
# - require_non_empty_string(None) raises TypeError("s must be a str")


def require_non_empty_string(s):
    # TODO
    pass


if __name__ == "__main__":
    print(require_non_empty_string("  hi "))