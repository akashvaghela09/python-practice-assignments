# Task: Implement validate_open_args(path, mode).
# Requirements:
# - path must be a non-empty str else TypeError("path must be a non-empty string")
# - mode must be one of: "r", "w", "a" else ValueError("invalid mode")
# - If mode is "r", path must end with ".txt" else ValueError("read mode requires .txt file")
# - Return a tuple (path, mode)
# Expected outcome:
# - validate_open_args("notes.txt", "r") returns ("notes.txt","r")
# - validate_open_args("notes.md", "r") raises ValueError("read mode requires .txt file")
# - validate_open_args("", "w") raises TypeError("path must be a non-empty string")


def validate_open_args(path, mode):
    # TODO
    pass


if __name__ == "__main__":
    print(validate_open_args("notes.txt", "r"))