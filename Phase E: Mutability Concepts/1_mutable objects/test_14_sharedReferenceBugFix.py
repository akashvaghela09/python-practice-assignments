import importlib
import ast
import pytest

mod = importlib.import_module("14_sharedReferenceBugFix")


def test_make_grid_creates_independent_rows():
    grid = mod.make_grid(3, 3)
    assert isinstance(grid, list)
    assert len(grid) == 3
    assert all(isinstance(row, list) for row in grid)
    assert all(len(row) == 3 for row in grid)

    grid[1][1] = 1
    assert grid[1][1] == 1
    assert grid[0][1] == 0
    assert grid[2][1] == 0

    assert id(grid[0]) != id(grid[1])
    assert id(grid[1]) != id(grid[2])
    assert id(grid[0]) != id(grid[2])


def test_make_grid_no_shared_reference_all_rows_and_modifications():
    grid = mod.make_grid(4, 2)
    ids = [id(r) for r in grid]
    assert len(set(ids)) == len(ids)

    grid[0][0] = 9
    assert grid[0][0] == 9
    assert grid[1][0] == 0
    assert grid[2][0] == 0
    assert grid[3][0] == 0


def test_make_grid_handles_zero_dimensions():
    g1 = mod.make_grid(0, 3)
    assert g1 == []

    g2 = mod.make_grid(3, 0)
    assert isinstance(g2, list)
    assert len(g2) == 3
    assert all(isinstance(r, list) and len(r) == 0 for r in g2)
    assert len({id(r) for r in g2}) == 3


def test_main_prints_expected_grid(capsys, monkeypatch):
    monkeypatch.setattr(mod, "__name__", "__main__", raising=False)
    mod.main()
    out = capsys.readouterr().out.strip()

    actual = ast.literal_eval(out)
    expected = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]

    assert actual == expected, f"expected={expected} actual={actual}"