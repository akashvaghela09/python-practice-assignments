import importlib.util
import pathlib
import re
import ast
import sys


def _load_module(path):
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _expected_set_from_source(source):
    m = re.search(r"^\s*nums\s*=\s*(\[[^\n]*\])\s*$", source, re.MULTILINE)
    assert m is not None
    nums = ast.literal_eval(m.group(1))
    return set(nums)


def test_no_placeholder_remaining():
    path = pathlib.Path(__file__).with_name("02_removeDuplicatesFromList.py")
    src = path.read_text(encoding="utf-8")
    assert "____" not in src


def test_unique_nums_is_set_and_matches_expected():
    path = pathlib.Path(__file__).with_name("02_removeDuplicatesFromList.py")
    src = path.read_text(encoding="utf-8")
    expected = _expected_set_from_source(src)

    mod = _load_module(path)

    assert hasattr(mod, "unique_nums")
    actual = mod.unique_nums
    assert isinstance(actual, set)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_printed_output_matches_set_repr(capsys):
    path = pathlib.Path(__file__).with_name("02_removeDuplicatesFromList.py")
    src = path.read_text(encoding="utf-8")
    expected = _expected_set_from_source(src)

    if "02_removeDuplicatesFromList" in sys.modules:
        del sys.modules["02_removeDuplicatesFromList"]

    mod = _load_module(path)
    out = capsys.readouterr().out.strip()

    expected_str = str(expected)
    assert out == expected_str, f"expected={expected_str} actual={out}"
    assert str(mod.unique_nums) == out, f"expected={out} actual={str(mod.unique_nums)}"