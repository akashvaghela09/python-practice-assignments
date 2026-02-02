import importlib.util
import io
import os
import sys


def load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_printed_output_matches_expected(capsys):
    path = os.path.join(os.path.dirname(__file__), "04_appendToInnerList.py")
    load_module_from_path("assignment_04_appendToInnerList", path)
    captured = capsys.readouterr()
    expected = "[['a', 'b', 'c'], ['x']]\n"
    assert captured.out == expected, f"expected={expected!r} actual={captured.out!r}"
    assert captured.err == "", f"expected={''!r} actual={captured.err!r}"


def test_letters_structure_after_execution():
    path = os.path.join(os.path.dirname(__file__), "04_appendToInnerList.py")
    module = load_module_from_path("assignment_04_appendToInnerList_state", path)
    expected = [["a", "b", "c"], ["x"]]
    assert module.letters == expected, f"expected={expected!r} actual={module.letters!r}"


def test_first_inner_list_only_modified():
    path = os.path.join(os.path.dirname(__file__), "04_appendToInnerList.py")
    module = load_module_from_path("assignment_04_appendToInnerList_inner", path)
    expected_second = ["x"]
    assert module.letters[1] == expected_second, f"expected={expected_second!r} actual={module.letters[1]!r}"
    expected_first = ["a", "b", "c"]
    assert module.letters[0] == expected_first, f"expected={expected_first!r} actual={module.letters[0]!r}"