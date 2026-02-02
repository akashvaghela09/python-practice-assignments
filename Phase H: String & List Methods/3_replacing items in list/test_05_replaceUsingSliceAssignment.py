import importlib.util
import os
import sys

import pytest


def _load_module():
    filename = "05_replaceUsingSliceAssignment.py"
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("assignment_05_replaceUsingSliceAssignment", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_printed_output_matches_expected(capsys):
    expected = "['a', 'X', 'Y', 'e']"
    _load_module()
    out = capsys.readouterr().out.strip()
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_letters_list_modified_as_expected(capsys):
    expected_list = ['a', 'X', 'Y', 'e']
    capsys.readouterr()
    m = _load_module()
    assert hasattr(m, "letters"), "expected has_attr=True actual has_attr=False"
    assert m.letters == expected_list, f"expected={expected_list!r} actual={m.letters!r}"


def test_length_is_correct(capsys):
    expected_len = 4
    capsys.readouterr()
    m = _load_module()
    actual_len = len(getattr(m, "letters", []))
    assert actual_len == expected_len, f"expected={expected_len!r} actual={actual_len!r}"


def test_middle_three_replaced_not_removed_all(capsys):
    expected_first = 'a'
    expected_last = 'e'
    capsys.readouterr()
    m = _load_module()
    letters = m.letters
    assert letters[0] == expected_first, f"expected={expected_first!r} actual={letters[0]!r}"
    assert letters[-1] == expected_last, f"expected={expected_last!r} actual={letters[-1]!r}"