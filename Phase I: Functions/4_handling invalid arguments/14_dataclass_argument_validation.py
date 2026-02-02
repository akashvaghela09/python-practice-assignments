# Task: Create a dataclass UserInput and validate fields in __post_init__.
# Fields:
# - username: str, must be 3-20 chars, alnum or underscore only
# - age: int, must be between 13 and 120 inclusive (bool not allowed)
# - email: str, must contain exactly one "@" and at least one "." after the "@"
# Invalid handling:
# - Raise TypeError("username must be a str"), TypeError("age must be an int"), TypeError("email must be a str")
# - Raise ValueError("invalid username"), ValueError("invalid age"), ValueError("invalid email")
# Expected outcome:
# - UserInput("alice_1", 30, "a@b.com") constructs successfully
# - UserInput("a!", 30, "a@b.com") raises ValueError("invalid username")
# - UserInput("alice", True, "a@b.com") raises TypeError("age must be an int")

from dataclasses import dataclass


@dataclass
class UserInput:
    username: str
    age: int
    email: str

    def __post_init__(self):
        # TODO: validate types and values; raise with exact messages above
        pass


if __name__ == "__main__":
    u = UserInput("alice_1", 30, "a@b.com")
    print(u)