import importlib
import io
import sys


def run_module_capture_stdout(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        importlib.import_module(module_name)
    finally:
        sys.stdout = old
    return buf.getvalue()


def test_prints_string_length():
    out = run_module_capture_stdout("04_stringLength")
    lines = [line.strip() for line in out.splitlines() if line.strip() != ""]
    assert len(lines) == 1, f"expected=1 actual={len(lines)}"
    expected = str(len("hello world"))
    assert lines[0] == expected, f"expected={expected} actual={lines[0]}"


def test_length_variable_matches_printed_value():
    if "04_stringLength" in sys.modules:
        del sys.modules["04_stringLength"]
    import 04_stringLength as m  # noqa: E999

    actual_printed = run_module_capture_stdout("04_stringLength").strip().splitlines()[-1].strip()
    expected = str(m.length)
    assert actual_printed == expected, f"expected={expected} actual={actual_printed}"