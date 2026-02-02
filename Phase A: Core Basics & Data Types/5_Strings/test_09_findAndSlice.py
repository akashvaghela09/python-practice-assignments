import importlib.util
import io
import os
import sys


def _run_module_capture_stdout(module_filename):
    path = os.path.join(os.path.dirname(__file__), module_filename)
    spec = importlib.util.spec_from_file_location("assignment_mod_09", path)
    mod = importlib.util.module_from_spec(spec)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        spec.loader.exec_module(mod)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout

    return mod, output


def test_prints_domain_only():
    _, out = _run_module_capture_stdout("09_findAndSlice.py")
    expected = "example.com"
    actual = out.strip()
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_at_index_is_correct_and_int():
    mod, _ = _run_module_capture_stdout("09_findAndSlice.py")
    expected = mod.email.index("@")
    actual = mod.at_index
    assert isinstance(actual, int), f"expected={int!r} actual={type(actual)!r}"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_domain_value_is_correct_and_matches_printed():
    mod, out = _run_module_capture_stdout("09_findAndSlice.py")
    expected = mod.email.split("@", 1)[1]
    actual = mod.domain
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    printed = out.strip()
    assert printed == expected, f"expected={expected!r} actual={printed!r}"


def test_domain_derived_from_at_index():
    mod, _ = _run_module_capture_stdout("09_findAndSlice.py")
    expected = mod.email[mod.at_index + 1 :]
    actual = mod.domain
    assert actual == expected, f"expected={expected!r} actual={actual!r}"