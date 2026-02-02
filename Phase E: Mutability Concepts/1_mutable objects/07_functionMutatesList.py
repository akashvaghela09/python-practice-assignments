# Goal: Show that functions can mutate passed-in mutable objects.
# Expected outcome: prints exactly: [2, 4, 6]


def double_in_place(nums):
    # TODO: mutate nums so each element is doubled, in-place
    # Do not create and return a new list.
    pass


def main():
    data = [1, 2, 3]
    double_in_place(data)
    print(data)


if __name__ == "__main__":
    main()
