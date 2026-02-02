import importlib
import os
import sys


def _load_module():
    module_name = "02_reassignVariable"
    if module_name in sys.modules:
        del sys.modules[module_name]
    return importlib.import_module(module_name)


def test_prints_expected_three_lines(capsys):
    _load_module()
    out = capsys.readouterr().out
    expected = "score=10\nscore=15\nscore=0\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_extra_output(capsys):
    _load_module()
    out = capsys.readouterr().out
    lines = out.splitlines()
    expected_count = 3
    actual_count = len(lines)
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"


def test_lines_exact_format(capsys):
    _load_module()
    out = capsys.readouterr().out
    lines = out.splitlines()
    expected = ["score=10", "score=15", "score=0"]
    assert lines == expected, f"expected={expected!r} actual={lines!r}"


def test_score_final_value(capsys):
    mod = _load_module()
    _ = capsys.readouterr().out
    expected = 0
    actual = getattr(mod, "score", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_score_is_int(capsys):
    mod = _load_module()
    _ = capsys.readouterr().out
    expected_type = int
    actual_type = type(getattr(mod, "score", None))
    assert actual_type is expected_type, f"expected={expected_type!r} actual={actual_type!r}"