import importlib.util
import io
import os
import sys


def load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prints_expected_sum(capsys):
    path = os.path.join(os.path.dirname(__file__), "02_splitCsvToInts.py")
    load_module_from_path("assignment_02_splitCsvToInts", path)
    captured = capsys.readouterr()
    out = captured.out.strip()
    expected = "60"
    assert out == expected, f"expected={expected} actual={out}"


def test_output_is_single_line_integer(capsys):
    path = os.path.join(os.path.dirname(__file__), "02_splitCsvToInts.py")
    load_module_from_path("assignment_02_splitCsvToInts_2", path)
    captured = capsys.readouterr()
    lines = [ln for ln in captured.out.splitlines() if ln.strip() != ""]
    expected_lines = 1
    actual_lines = len(lines)
    assert actual_lines == expected_lines, f"expected={expected_lines} actual={actual_lines}"
    actual = lines[0].strip()
    expected = str(int(actual))
    assert actual == expected, f"expected={expected} actual={actual}"


def test_no_traceback_on_import():
    path = os.path.join(os.path.dirname(__file__), "02_splitCsvToInts.py")
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        load_module_from_path("assignment_02_splitCsvToInts_3", path)
        err = sys.stderr.getvalue()
    finally:
        sys.stderr = old_stderr
    expected = ""
    actual = err
    assert actual == expected, f"expected={expected!r} actual={actual!r}"