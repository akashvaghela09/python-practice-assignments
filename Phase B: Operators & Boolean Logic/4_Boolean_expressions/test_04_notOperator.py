import importlib.util
import os
import sys


def _load_module_capture_stdout(path, module_name="mod_04_notOperator"):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)

    out = []
    original_stdout_write = sys.stdout.write

    def _write(s):
        out.append(s)
        return len(s)

    sys.stdout.write = _write
    try:
        spec.loader.exec_module(module)
    finally:
        sys.stdout.write = original_stdout_write

    return module, "".join(out)


def test_output_exact_lines():
    path = os.path.join(os.path.dirname(__file__), "04_notOperator.py")
    _, captured = _load_module_capture_stdout(path)

    expected = "True\nFalse\nTrue\n"
    actual = captured
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_outputs_are_booleans_only():
    path = os.path.join(os.path.dirname(__file__), "04_notOperator.py")
    _, captured = _load_module_capture_stdout(path)

    lines = captured.splitlines()
    expected = 3
    actual = len(lines)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"

    for i, line in enumerate(lines):
        expected_set = {"True", "False"}
        actual_val = line
        assert actual_val in expected_set, f"expected={expected_set!r} actual={actual_val!r}"


def test_importable_module():
    path = os.path.join(os.path.dirname(__file__), "04_notOperator.py")
    spec = importlib.util.spec_from_file_location("mod_04_notOperator_import", path)
    module = importlib.util.module_from_spec(spec)

    out = []
    original_stdout_write = sys.stdout.write

    def _write(s):
        out.append(s)
        return len(s)

    sys.stdout.write = _write
    try:
        spec.loader.exec_module(module)
    finally:
        sys.stdout.write = original_stdout_write

    assert hasattr(module, "is_raining") is True
    assert hasattr(module, "has_umbrella") is True