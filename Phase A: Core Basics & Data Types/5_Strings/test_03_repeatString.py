import importlib.util
import os
import sys


def _load_module(path, name="mod03"):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_result_repeats_laugh_count(capsys):
    path = os.path.join(os.path.dirname(__file__), "03_repeatString.py")
    mod = _load_module(path)

    assert hasattr(mod, "laugh")
    assert hasattr(mod, "count")
    assert hasattr(mod, "result")

    expected = mod.laugh * mod.count
    actual = mod.result
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_printed_output_matches_result(capsys):
    path = os.path.join(os.path.dirname(__file__), "03_repeatString.py")
    mod = _load_module(path, name="mod03_print")

    captured = capsys.readouterr()
    printed = captured.out.rstrip("\n")
    expected = str(mod.result)
    actual = printed
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_count_is_non_negative_int():
    path = os.path.join(os.path.dirname(__file__), "03_repeatString.py")
    mod = _load_module(path, name="mod03_count")

    assert isinstance(mod.count, int), f"expected={int.__name__!r} actual={type(mod.count).__name__!r}"
    assert mod.count >= 0, f"expected={True!r} actual={(mod.count >= 0)!r}"


def test_result_is_string():
    path = os.path.join(os.path.dirname(__file__), "03_repeatString.py")
    mod = _load_module(path, name="mod03_type")

    assert isinstance(mod.result, str), f"expected={str.__name__!r} actual={type(mod.result).__name__!r}"