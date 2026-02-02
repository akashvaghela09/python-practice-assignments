import importlib.util
import io
import os
import sys
import pytest

MODULE_FILENAME = "12_replaceInNestedImmutable.py"


def load_module(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    dst_path = tmp_path / MODULE_FILENAME
    dst_path.write_text(open(src_path, "r", encoding="utf-8").read(), encoding="utf-8")

    module_name = "mod_12_replace_nested_immutable"
    spec = importlib.util.spec_from_file_location(module_name, str(dst_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def capture_printed_output(mod):
    buf = io.StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = buf
        if hasattr(mod, "print"):
            pass
    finally:
        sys.stdout = old_stdout
    return buf.getvalue()


def test_prints_expected_tuple(tmp_path, capsys):
    load_module(tmp_path)
    out = capsys.readouterr().out
    expected = "('a', ('b', 'Z'), 'c')\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_new_data_is_correct_tuple(tmp_path, capsys):
    mod = load_module(tmp_path)
    capsys.readouterr()
    expected = ("a", ("b", "Z"), "c")
    actual = getattr(mod, "new_data", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_original_data_unchanged(tmp_path, capsys):
    mod = load_module(tmp_path)
    capsys.readouterr()
    expected = ("a", ("b", "x"), "c")
    actual = getattr(mod, "data", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_new_data_is_tuple_and_inner_tuple(tmp_path, capsys):
    mod = load_module(tmp_path)
    capsys.readouterr()
    new_data = getattr(mod, "new_data", None)
    assert isinstance(new_data, tuple), f"expected={tuple!r} actual={type(new_data)!r}"
    inner = None if new_data is None or len(new_data) < 2 else new_data[1]
    assert isinstance(inner, tuple), f"expected={tuple!r} actual={type(inner)!r}"


def test_new_data_does_not_share_inner_tuple(tmp_path, capsys):
    mod = load_module(tmp_path)
    capsys.readouterr()
    data = getattr(mod, "data", None)
    new_data = getattr(mod, "new_data", None)
    if not isinstance(data, tuple) or not isinstance(new_data, tuple):
        pytest.fail(f"expected={tuple!r} actual={(type(data), type(new_data))!r}")
    assert data[1] is not new_data[1], f"expected={'different_inner_tuple'!r} actual={'same_inner_tuple'!r}"