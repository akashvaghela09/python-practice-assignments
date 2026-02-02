import importlib.util
import io
import os
import sys


def _load_module_from_filename(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("student_module_01", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_main_capture_stdout(module):
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        module.main()
    finally:
        sys.stdout = old
    return buf.getvalue()


def test_main_prints_expected_list_exactly():
    module = _load_module_from_filename("01_listMutationBasics.py")
    out = _run_main_capture_stdout(module)
    expected = "[10, 99, 30, 40]\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_main_output_is_single_line_only():
    module = _load_module_from_filename("01_listMutationBasics.py")
    out = _run_main_capture_stdout(module)
    expected = 1
    actual = len(out.splitlines(True))
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_main_output_has_no_extra_whitespace():
    module = _load_module_from_filename("01_listMutationBasics.py")
    out = _run_main_capture_stdout(module)
    expected = out
    actual = out.rstrip("\n")
    assert actual + "\n" == expected, f"expected={expected!r} actual={(actual + chr(10))!r}"