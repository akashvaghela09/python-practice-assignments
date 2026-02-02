import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout


def load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prints_expected_tuple(capsys):
    fname = "09_findInNested.py"
    path = os.path.join(os.path.dirname(__file__), fname)
    if not os.path.exists(path):
        path = fname

    buf = io.StringIO()
    with redirect_stdout(buf):
        load_module_from_path("m09_findInNested_print", path)

    out = buf.getvalue()
    expected = "(2, 0)\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_pos_variable_is_correct_tuple():
    fname = "09_findInNested.py"
    path = os.path.join(os.path.dirname(__file__), fname)
    if not os.path.exists(path):
        path = fname

    buf = io.StringIO()
    with redirect_stdout(buf):
        m = load_module_from_path("m09_findInNested_var", path)

    expected = (2, 0)
    actual = getattr(m, "pos", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_pos_is_tuple_of_two_ints():
    fname = "09_findInNested.py"
    path = os.path.join(os.path.dirname(__file__), fname)
    if not os.path.exists(path):
        path = fname

    buf = io.StringIO()
    with redirect_stdout(buf):
        m = load_module_from_path("m09_findInNested_type", path)

    pos = getattr(m, "pos", None)
    assert isinstance(pos, tuple), f"expected={tuple!r} actual={type(pos)!r}"
    assert len(pos) == 2, f"expected={2!r} actual={len(pos)!r}"
    assert all(isinstance(x, int) for x in pos), f"expected={'(int,int)'!r} actual={tuple(type(x) for x in pos)!r}"


def test_pos_points_to_target_in_grid():
    fname = "09_findInNested.py"
    path = os.path.join(os.path.dirname(__file__), fname)
    if not os.path.exists(path):
        path = fname

    buf = io.StringIO()
    with redirect_stdout(buf):
        m = load_module_from_path("m09_findInNested_grid", path)

    grid = getattr(m, "grid", None)
    target = getattr(m, "target", None)
    pos = getattr(m, "pos", None)

    r, c = pos
    actual = grid[r][c]
    expected = target
    assert actual == expected, f"expected={expected!r} actual={actual!r}"