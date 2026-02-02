# Goal: Track and verify object identity across mutations and copies.
# Expected outcome: prints exactly:
# same_after_mutation: True
# same_after_shallow_copy: False
# alias_reflects_change: True
# final: {'a': [1, 2, 3, 4], 'b': [1, 2, 3, 4], 'c': [1, 2, 3]}


def main():
    data = {"a": [1, 2, 3]}

    # TODO: create b as an alias to the same list as data['a'] (not a copy)
    b = None

    # TODO: create c as a shallow copy of data['a']
    c = None

    before_id = id(data["a"])

    # TODO: mutate data['a'] by appending 4

    after_id = id(data["a"])

    # TODO: compute booleans:
    # same_after_mutation: True if the list object identity didn't change
    # same_after_shallow_copy: False if c is a different object than data['a']
    # alias_reflects_change: True if b sees the appended 4
    same_after_mutation = None
    same_after_shallow_copy = None
    alias_reflects_change = None

    print("same_after_mutation:", same_after_mutation)
    print("same_after_shallow_copy:", same_after_shallow_copy)
    print("alias_reflects_change:", alias_reflects_change)
    print("final:", {"a": data["a"], "b": b, "c": c})


if __name__ == "__main__":
    main()
