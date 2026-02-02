import importlib.util
import io
import os
import sys


def _run_script(path):
    old_stdout = sys.stdout
    buf = io.StringIO()
    try:
        sys.stdout = buf
        spec = importlib.util.spec_from_file_location("mod05", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old_stdout
    return buf.getvalue(), module


def test_output_exact():
    path = os.path.join(os.path.dirname(__file__), "05_moduloRemainder.py")
    out, _ = _run_script(path)
    expected = "Leftover cookies: 5\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_leftover_value():
    path = os.path.join(os.path.dirname(__file__), "05_moduloRemainder.py")
    _, mod = _run_script(path)
    expected = mod.cookies % mod.box_size
    actual = mod.leftover
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_leftover_is_int():
    path = os.path.join(os.path.dirname(__file__), "05_moduloRemainder.py")
    _, mod = _run_script(path)
    expected = int
    actual = type(mod.leftover)
    assert actual is expected, f"expected={expected!r} actual={actual!r}"


def test_leftover_in_valid_range():
    path = os.path.join(os.path.dirname(__file__), "05_moduloRemainder.py")
    _, mod = _run_script(path)
    expected = list(range(mod.box_size))
    actual = mod.leftover
    assert actual in expected, f"expected={expected!r} actual={actual!r}"