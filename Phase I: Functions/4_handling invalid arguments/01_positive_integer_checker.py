# Task: Implement a function that validates whether n is a positive integer.
# Requirements:
# - If n is not an int, raise TypeError with message: "n must be an int"
# - If n <= 0, raise ValueError with message: "n must be positive"
# - Otherwise return True
# Expected outcome:
# - validate_positive_int(3) returns True
# - validate_positive_int(0) raises ValueError("n must be positive")
# - validate_positive_int("3") raises TypeError("n must be an int")


def validate_positive_int(n):
    # TODO: implement argument validation and return True for valid inputs
    pass


# Quick checks (do not change):
if __name__ == "__main__":
    print(validate_positive_int(3))