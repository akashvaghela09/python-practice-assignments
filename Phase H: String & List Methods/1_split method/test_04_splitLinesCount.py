import importlib.util
import pathlib
import sys


def load_module():
    path = pathlib.Path(__file__).resolve().parent / "04_splitLinesCount.py"
    spec = importlib.util.spec_from_file_location("split_lines_count_mod", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_prints_line_count_3(capsys):
    load_module()
    out = capsys.readouterr().out.strip()
    expected = "3"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_split_produces_three_lines():
    mod = load_module()
    expected = ["first line", "second line", "third line"]
    assert mod.lines == expected, f"expected={expected!r} actual={mod.lines!r}"
    expected_len = 3
    actual_len = len(mod.lines)
    assert actual_len == expected_len, f"expected={expected_len!r} actual={actual_len!r}"


def test_no_empty_strings_in_lines():
    mod = load_module()
    expected = False
    actual = any(s == "" for s in mod.lines)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"