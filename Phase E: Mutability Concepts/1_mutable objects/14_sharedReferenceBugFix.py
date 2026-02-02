# Goal: Fix a shared-reference bug when creating a matrix (list of lists).
# Expected outcome: prints exactly:
# [[0, 0, 0], [0, 1, 0], [0, 0, 0]]


def make_grid(rows, cols):
    # BUGGY starter (do not keep as-is):
    # return [[0] * cols] * rows

    # TODO: implement make_grid so each row is an independent list.
    pass


def main():
    grid = make_grid(3, 3)

    # Set center cell to 1
    grid[1][1] = 1

    print(grid)


if __name__ == "__main__":
    main()
