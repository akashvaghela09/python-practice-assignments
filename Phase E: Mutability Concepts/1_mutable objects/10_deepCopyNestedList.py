# Goal: Use deep copy to prevent nested mutation from affecting the original.
# Expected outcome: prints exactly:
# original: [[1, 2], [3, 4]]
# deep: [[1, 99], [3, 4]]

import copy


def main():
    original = [[1, 2], [3, 4]]

    # TODO: create a deep copy of original
    deep = None

    # TODO: mutate deep so that the first inner list's second element becomes 99

    print("original:", original)
    print("deep:", deep)


if __name__ == "__main__":
    main()
