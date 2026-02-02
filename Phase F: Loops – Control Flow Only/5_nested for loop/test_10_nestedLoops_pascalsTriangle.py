import importlib.util
import os
import sys
import types
import pytest


def _load_module():
    filename = "10_nestedLoops_pascalsTriangle.py"
    here = os.path.dirname(__file__)
    path = os.path.join(here, filename)
    if not os.path.exists(path):
        path = os.path.join(os.getcwd(), filename)

    spec = importlib.util.spec_from_file_location("pascals_triangle_mod", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _expected_triangle(n):
    tri = []
    for r in range(n):
        row = [1] * (r + 1)
        for c in range(1, r):
            row[c] = tri[r - 1][c - 1] + tri[r - 1][c]
        tri.append(row)
    return tri


@pytest.fixture()
def mod(capsys):
    m = _load_module()
    capsys.readouterr()
    return m


def test_has_triangle_variable(mod):
    assert hasattr(mod, "triangle")


def test_triangle_is_list(mod):
    assert isinstance(mod.triangle, list)


def test_n_exists_and_is_int(mod):
    assert hasattr(mod, "n")
    assert isinstance(mod.n, int)


def test_triangle_matches_expected_for_n(mod):
    expected = _expected_triangle(mod.n)
    actual = mod.triangle
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_triangle_rows_lengths(mod):
    tri = mod.triangle
    expected_lengths = list(range(1, mod.n + 1))
    actual_lengths = [len(r) for r in tri]
    assert actual_lengths == expected_lengths, f"expected={expected_lengths!r} actual={actual_lengths!r}"


def test_triangle_row_edges_are_ones(mod):
    tri = mod.triangle
    expected_edges = [(1, 1) if len(r) > 1 else (1,) for r in tri]
    actual_edges = []
    for r in tri:
        if len(r) == 1:
            actual_edges.append((r[0],))
        else:
            actual_edges.append((r[0], r[-1]))
    assert actual_edges == expected_edges, f"expected={expected_edges!r} actual={actual_edges!r}"


def test_triangle_middle_values_follow_rule(mod):
    tri = mod.triangle
    ok = True
    first_bad = None
    for r in range(2, len(tri)):
        prev = tri[r - 1]
        row = tri[r]
        for c in range(1, r):
            expected = prev[c - 1] + prev[c]
            actual = row[c]
            if actual != expected:
                ok = False
                first_bad = (r, c, expected, actual)
                break
        if not ok:
            break
    assert ok, f"expected={first_bad[2]!r} actual={first_bad[3]!r}"


def test_prints_triangle_representation(mod, capsys):
    out = capsys.readouterr().out.strip()
    expected = repr(mod.triangle)
    actual = out
    assert actual == expected, f"expected={expected!r} actual={actual!r}"