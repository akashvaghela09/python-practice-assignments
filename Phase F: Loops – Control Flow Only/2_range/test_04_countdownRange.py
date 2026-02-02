import importlib.util
import io
import os
import sys


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_countdown_range_print_and_value(capsys):
    path = os.path.join(os.path.dirname(__file__), "04_countdownRange.py")
    load_module(path, "countdown_mod")

    out = capsys.readouterr().out.strip()
    expected = str([5, 4, 3, 2, 1])
    assert out == expected, f"expected={expected} actual={out}"


def test_countdown_variable_exists_and_correct():
    path = os.path.join(os.path.dirname(__file__), "04_countdownRange.py")
    mod = load_module(path, "countdown_mod2")

    expected = [5, 4, 3, 2, 1]
    actual = getattr(mod, "countdown", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_no_extra_output_lines(capsys):
    path = os.path.join(os.path.dirname(__file__), "04_countdownRange.py")
    load_module(path, "countdown_mod3")

    out = capsys.readouterr().out
    lines = [line for line in out.splitlines() if line.strip() != ""]
    expected_count = 1
    actual_count = len(lines)
    assert actual_count == expected_count, f"expected={expected_count} actual={actual_count}"