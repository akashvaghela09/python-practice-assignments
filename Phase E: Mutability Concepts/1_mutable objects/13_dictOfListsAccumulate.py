# Goal: Accumulate values into lists within a dictionary.
# Expected outcome: prints exactly: {'fruit': ['apple', 'banana'], 'veg': ['carrot']}


def add_to_group(groups, category, item):
    # TODO: mutate groups so that groups[category] is a list that includes item.
    # If category doesn't exist, create it with an empty list first.
    pass


def main():
    groups = {}
    add_to_group(groups, "fruit", "apple")
    add_to_group(groups, "fruit", "banana")
    add_to_group(groups, "veg", "carrot")
    print(groups)


if __name__ == "__main__":
    main()
