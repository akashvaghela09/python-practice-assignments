import importlib
import io
import contextlib


def test_prints_expected_output():
    mod_name = "03_updateNestedList"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(mod_name)
    out = buf.getvalue().strip()
    expected = "[[0, 1], [2, 99]]"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_grid_mutated_correctly():
    mod_name = "03_updateNestedList"
    with contextlib.redirect_stdout(io.StringIO()):
        m = importlib.reload(importlib.import_module(mod_name))
    expected = [[0, 1], [2, 99]]
    actual = getattr(m, "grid", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"