# Goal: Understand aliasing: two variables referencing the same mutable list.
# Expected outcome: prints exactly:
# a: ["x", "y", "z"]
# b: ["x", "y", "z"]

def main():
    a = ["x", "y"]

    # TODO: make b refer to the SAME list object as a (aliasing)
    b = None

    # TODO: mutate the list through b so that the shared list becomes ["x","y","z"]

    print("a:", a)
    print("b:", b)


if __name__ == "__main__":
    main()
