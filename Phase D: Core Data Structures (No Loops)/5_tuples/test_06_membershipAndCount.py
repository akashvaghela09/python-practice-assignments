import importlib.util
import os
import sys
import types
import pytest

MODULE_FILENAME = "06_membershipAndCount.py"


def load_module(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    dst = tmp_path / MODULE_FILENAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    name = "mod_06_membershipAndCount"
    spec = importlib.util.spec_from_file_location(name, str(dst))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def run_module_capture_stdout(tmp_path, capsys):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    dst = tmp_path / MODULE_FILENAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    name = "run_06_membershipAndCount"
    spec = importlib.util.spec_from_file_location(name, str(dst))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    out = capsys.readouterr().out
    return mod, out


def test_outputs_membership_and_count(tmp_path, capsys):
    mod, out = run_module_capture_stdout(tmp_path, capsys)
    data = getattr(mod, "data")
    expected_lines = [str(7 in data), str(data.count(2))]
    actual_lines = [line.rstrip("\n") for line in out.splitlines() if line.strip() != ""]
    assert actual_lines[:2] == expected_lines, f"expected={expected_lines!r} actual={actual_lines[:2]!r}"


def test_prints_two_lines(tmp_path, capsys):
    _, out = run_module_capture_stdout(tmp_path, capsys)
    actual_lines = [line.rstrip("\n") for line in out.splitlines() if line.strip() != ""]
    expected_count = 2
    assert len(actual_lines) == expected_count, f"expected={expected_count!r} actual={len(actual_lines)!r}"


def test_data_is_tuple_unchanged(tmp_path):
    mod = load_module(tmp_path)
    expected = (2, 7, 2, 9, 2)
    actual = getattr(mod, "data")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert isinstance(actual, tuple), f"expected={tuple!r} actual={type(actual)!r}"