import importlib.util
import os
import sys
import pytest


def _load_module(path):
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_output_list(capsys):
    path = os.path.join(os.path.dirname(__file__), "08_splitAndFilterEmpty.py")
    _load_module(path)
    out = capsys.readouterr().out.strip()
    assert out != ""
    printed = eval(out, {"__builtins__": {}})
    expected = ["a", "b", "c"]
    assert printed == expected, f"expected={expected!r} actual={printed!r}"


def test_no_empty_items_in_output(capsys):
    path = os.path.join(os.path.dirname(__file__), "08_splitAndFilterEmpty.py")
    _load_module(path)
    out = capsys.readouterr().out.strip()
    printed = eval(out, {"__builtins__": {}})
    actual = any(item == "" for item in printed)
    expected = False
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_all_items_are_strings(capsys):
    path = os.path.join(os.path.dirname(__file__), "08_splitAndFilterEmpty.py")
    _load_module(path)
    out = capsys.readouterr().out.strip()
    printed = eval(out, {"__builtins__": {}})
    actual = all(isinstance(x, str) for x in printed)
    expected = True
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_split_delimiter_is_comma():
    path = os.path.join(os.path.dirname(__file__), "08_splitAndFilterEmpty.py")
    module = _load_module(path)
    expected = ["a", "", "b", "", "", "c", ""]
    actual = module.raw
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_filtered_is_nonempty_and_matches_printed(capsys):
    path = os.path.join(os.path.dirname(__file__), "08_splitAndFilterEmpty.py")
    module = _load_module(path)
    out = capsys.readouterr().out.strip()
    printed = eval(out, {"__builtins__": {}})
    expected = printed
    actual = module.filtered
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert len(module.filtered) > 0