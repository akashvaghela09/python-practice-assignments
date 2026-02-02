import importlib.util
import os
import sys


def _load_module_capture_output(module_name, file_path):
    import io
    from contextlib import redirect_stdout

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)

    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)
    return buf.getvalue()


def test_prints_only_even_numbers_from_1_to_10(capsys):
    file_name = "01_skipOddNumbers.py"
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    module_name = "skipOddNumbers_01_testload"
    out = _load_module_capture_output(module_name, file_path)

    actual = [line.rstrip("\n") for line in out.splitlines()]
    expected = ["2", "4", "6", "8", "10"]

    assert expected == actual, f"expected={expected} actual={actual}"


def test_no_extra_whitespace_or_blank_lines():
    file_name = "01_skipOddNumbers.py"
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    module_name = "skipOddNumbers_01_testload_2"
    out = _load_module_capture_output(module_name, file_path)

    actual_lines = out.splitlines()
    expected_lines = ["2", "4", "6", "8", "10"]

    assert expected_lines == actual_lines, f"expected={expected_lines} actual={actual_lines}"


def test_outputs_increasing_order():
    file_name = "01_skipOddNumbers.py"
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    module_name = "skipOddNumbers_01_testload_3"
    out = _load_module_capture_output(module_name, file_path)

    actual = out.splitlines()
    actual_ints = [int(x) for x in actual] if actual else []

    expected_ints = [2, 4, 6, 8, 10]
    assert expected_ints == actual_ints, f"expected={expected_ints} actual={actual_ints}"