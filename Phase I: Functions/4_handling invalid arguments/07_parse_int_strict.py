# Task: Implement parse_int_strict(s).
# Requirements:
# - s must be str else TypeError("s must be a str")
# - s may have leading/trailing whitespace; strip it
# - After stripping, s must match optional leading sign followed by digits only
#   If not, raise ValueError("invalid integer literal")
# - Return the parsed int
# Expected outcome:
# - parse_int_strict("  -42 ") returns -42
# - parse_int_strict("3.14") raises ValueError("invalid integer literal")
# - parse_int_strict(10) raises TypeError("s must be a str")


def parse_int_strict(s):
    # TODO
    pass


if __name__ == "__main__":
    print(parse_int_strict("  -42 "))