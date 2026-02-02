# Goal: Avoid unintended shared mutation using a shallow copy.
# Expected outcome: prints exactly:
# original: [1, 2, 3]
# copy: [1, 2, 3, 99]

def main():
    original = [1, 2, 3]

    # TODO: create a shallow copy of original and store in copied
    copied = None

    # TODO: mutate copied to add 99 without changing original

    print("original:", original)
    print("copy:", copied)


if __name__ == "__main__":
    main()
