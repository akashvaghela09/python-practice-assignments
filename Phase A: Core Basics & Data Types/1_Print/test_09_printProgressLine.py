import importlib.util
import io
import os
import sys


def _load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_output_is_single_line_with_loading_100():
    file_path = os.path.join(os.path.dirname(__file__), "09_printProgressLine.py")
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        _load_module("student_09_printProgressLine", file_path)
    finally:
        sys.stdout = old

    out = buf.getvalue()

    expected = "Loading... 100%\n"
    actual = out.replace("\r", "")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_no_extra_lines_or_whitespace():
    file_path = os.path.join(os.path.dirname(__file__), "09_printProgressLine.py")
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        _load_module("student_09_printProgressLine_2", file_path)
    finally:
        sys.stdout = old

    out = buf.getvalue()
    actual = out.replace("\r", "")

    expected_line_count = 1
    actual_line_count = actual.count("\n")
    assert actual_line_count == expected_line_count, f"expected={expected_line_count!r} actual={actual_line_count!r}"

    expected = "Loading... 100%\n"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_starts_with_loading_and_ends_with_newline():
    file_path = os.path.join(os.path.dirname(__file__), "09_printProgressLine.py")
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        _load_module("student_09_printProgressLine_3", file_path)
    finally:
        sys.stdout = old

    out = buf.getvalue()
    actual = out.replace("\r", "")

    expected_starts = True
    actual_starts = actual.startswith("Loading...")
    assert actual_starts == expected_starts, f"expected={expected_starts!r} actual={actual_starts!r}"

    expected_ends = True
    actual_ends = actual.endswith("\n")
    assert actual_ends == expected_ends, f"expected={expected_ends!r} actual={actual_ends!r}"