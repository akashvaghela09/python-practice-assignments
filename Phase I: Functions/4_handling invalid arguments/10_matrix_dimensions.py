# Task: Implement validate_matrix(matrix).
# Requirements:
# - matrix must be a non-empty list of non-empty lists
#   If invalid type/emptiness, raise TypeError("matrix must be a non-empty list of non-empty lists")
# - All rows must have the same length; else ValueError("matrix rows must have the same length")
# - All elements must be numbers (int/float, bool not allowed); else TypeError("matrix elements must be numbers")
# - Return (rows, cols)
# Expected outcome:
# - validate_matrix([[1,2],[3,4]]) returns (2,2)
# - validate_matrix([[1,2],[3]]) raises ValueError("matrix rows must have the same length")


def validate_matrix(matrix):
    # TODO
    pass


if __name__ == "__main__":
    print(validate_matrix([[1, 2], [3, 4]]))