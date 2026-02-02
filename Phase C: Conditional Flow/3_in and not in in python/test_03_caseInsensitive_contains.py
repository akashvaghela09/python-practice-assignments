import importlib.util
import os
import sys


def _load_module():
    fname = "03_caseInsensitive_contains.py"
    path = os.path.join(os.path.dirname(__file__), fname)
    spec = importlib.util.spec_from_file_location("case_insensitive_contains_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_output_exact(capsys):
    _load_module()
    out = capsys.readouterr().out
    expected = "True\nFalse\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_none_printed(capsys):
    _load_module()
    out = capsys.readouterr().out
    assert "None" not in out, f"expected={False!r} actual={('None' in out)!r}"


def test_prints_two_lines(capsys):
    _load_module()
    out = capsys.readouterr().out
    lines = out.splitlines()
    expected_count = 2
    actual_count = len(lines)
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"