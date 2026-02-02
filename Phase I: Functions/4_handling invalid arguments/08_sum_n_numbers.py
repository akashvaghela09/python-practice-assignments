# Task: Implement sum_n(numbers, n).
# Requirements:
# - numbers must be a list of ints/floats (bool not allowed) else TypeError("numbers must be a list of numbers")
# - n must be int (bool not allowed) else TypeError("n must be an int")
# - n must be between 0 and len(numbers) inclusive else ValueError("n out of allowed range")
# - Return sum of the first n elements
# Expected outcome:
# - sum_n([1,2,3,4], 2) returns 3
# - sum_n([1,2,3], 5) raises ValueError("n out of allowed range")
# - sum_n([1,"2",3], 2) raises TypeError("numbers must be a list of numbers")


def sum_n(numbers, n):
    # TODO
    pass


if __name__ == "__main__":
    print(sum_n([1, 2, 3, 4], 2))