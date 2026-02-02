# Task: Implement build_query(**params).
# Requirements:
# - Only these keys are allowed: "q", "page", "limit"
# - If any other key is present, raise TypeError("unexpected parameter: <key>")
# - page and limit must be positive ints (bool not allowed); otherwise raise ValueError:
#   - "page must be a positive int"
#   - "limit must be a positive int"
# - q must be a non-empty string after stripping; else ValueError("q must be a non-empty string")
# - Return a dict containing only provided keys with validated values
# Expected outcome:
# - build_query(q="cats", page=1) returns {"q":"cats","page":1}
# - build_query(sort="asc") raises TypeError("unexpected parameter: sort")
# - build_query(q="   ") raises ValueError("q must be a non-empty string")


def build_query(**params):
    # TODO
    pass


if __name__ == "__main__":
    print(build_query(q="cats", page=1))