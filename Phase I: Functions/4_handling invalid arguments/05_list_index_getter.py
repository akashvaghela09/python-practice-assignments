# Task: Implement get_item_at(seq, index).
# Requirements:
# - seq must be a list or tuple else TypeError("seq must be a list or tuple")
# - index must be int (bool not allowed) else TypeError("index must be an int")
# - If index out of range, raise IndexError("index out of range")
# - Otherwise return seq[index]
# Expected outcome:
# - get_item_at(["a","b"], 1) returns "b"
# - get_item_at([1], 2) raises IndexError("index out of range")
# - get_item_at("abc", 0) raises TypeError("seq must be a list or tuple")


def get_item_at(seq, index):
    # TODO
    pass


if __name__ == "__main__":
    print(get_item_at(["a", "b"], 1))