# Goal: Avoid the mutable default argument pitfall.
# Expected outcome: prints exactly:
# ['a']
# ['b']


def add_item(item, bucket=None):
    # TODO: implement so that each call without an explicit bucket
    # starts with a fresh list (no shared state between calls).
    # Must return the list.
    pass


def main():
    print(add_item("a"))
    print(add_item("b"))


if __name__ == "__main__":
    main()
