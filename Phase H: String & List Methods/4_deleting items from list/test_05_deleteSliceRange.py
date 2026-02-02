import importlib.util
import os
import sys

import pytest


def load_module_and_capture_stdout(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        raise
    return module


def test_letters_list_modified_correctly(capsys):
    file_path = os.path.join(os.path.dirname(__file__), "05_deleteSliceRange.py")
    module_name = "deleteSliceRange_05_testmod"
    module = load_module_and_capture_stdout(file_path, module_name)

    assert hasattr(module, "letters")
    expected = ["a", "e", "f"]
    actual = module.letters
    assert actual == expected, f"expected={expected} actual={actual}"

    out = capsys.readouterr().out.strip()
    assert out == f"letters: {expected}", f"expected={f'letters: {expected}'} actual={out}"


def test_no_extra_elements_or_missing_elements():
    file_path = os.path.join(os.path.dirname(__file__), "05_deleteSliceRange.py")
    module_name = "deleteSliceRange_05_testmod2"
    module = load_module_and_capture_stdout(file_path, module_name)

    expected = ["a", "e", "f"]
    actual = module.letters
    assert len(actual) == len(expected), f"expected={len(expected)} actual={len(actual)}"
    assert set(actual) == set(expected), f"expected={set(expected)} actual={set(actual)}"