import importlib.util
import io
import os
import sys

import pytest


def load_module_from_filename(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("student_module_10", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prints_expected_output(capsys):
    load_module_from_filename("10_ternary_for_default_value_with_none.py")
    captured = capsys.readouterr()
    expected = "Hello, Anonymous\n"
    actual = captured.out
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_display_name_variable_is_anonymous_when_name_none():
    module = load_module_from_filename("10_ternary_for_default_value_with_none.py")
    expected = "Anonymous"
    actual = getattr(module, "display_name", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_does_not_print_extra_output(capsys):
    load_module_from_filename("10_ternary_for_default_value_with_none.py")
    captured = capsys.readouterr()
    expected_err = ""
    actual_err = captured.err
    assert actual_err == expected_err, f"expected={expected_err!r} actual={actual_err!r}"