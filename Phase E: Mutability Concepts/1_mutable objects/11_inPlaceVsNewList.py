# Goal: Distinguish in-place mutation from creating a new list.
# Expected outcome: prints exactly:
# same_object: True
# nums: [3, 1, 2]


def main():
    nums = [3, 1, 2]
    before_id = id(nums)

    # TODO: sort nums in-place (do not assign nums to a new list)

    after_id = id(nums)

    print("same_object:", before_id == after_id)
    print("nums:", nums)


if __name__ == "__main__":
    main()
