import importlib.util
import io
import os
import sys


def _run_module_capture_stdout(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("mod_under_test", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old
    return module, buf.getvalue()


def test_prints_expected_output():
    _, out = _run_module_capture_stdout("06_defaultWithOr.py")
    expected = "Hello, stranger\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_final_name_variable_value():
    mod, _ = _run_module_capture_stdout("06_defaultWithOr.py")
    expected = "stranger"
    actual = getattr(mod, "final_name", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_final_name_is_string():
    mod, _ = _run_module_capture_stdout("06_defaultWithOr.py")
    actual = getattr(mod, "final_name", None)
    assert isinstance(actual, str), f"expected={str.__name__!r} actual={type(actual).__name__!r}"