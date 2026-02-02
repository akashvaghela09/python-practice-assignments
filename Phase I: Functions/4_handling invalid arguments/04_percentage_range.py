# Task: Implement clamp_percentage(p) with invalid argument checks.
# Requirements:
# - p must be int or float (bool not allowed) else TypeError("p must be a number")
# - p must be between 0 and 100 inclusive else ValueError("p must be between 0 and 100")
# - Return p as float
# Expected outcome:
# - clamp_percentage(0) returns 0.0
# - clamp_percentage(100) returns 100.0
# - clamp_percentage(-1) raises ValueError("p must be between 0 and 100")


def clamp_percentage(p):
    # TODO
    pass


if __name__ == "__main__":
    print(clamp_percentage(75))