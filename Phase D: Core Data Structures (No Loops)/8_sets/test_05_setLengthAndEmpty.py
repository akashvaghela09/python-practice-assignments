import importlib.util
import pathlib
import re

import pytest


def _load_module(capsys):
    path = pathlib.Path(__file__).resolve().parent / "05_setLengthAndEmpty.py"
    spec = importlib.util.spec_from_file_location("m05_setLengthAndEmpty", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = capsys.readouterr().out
    return mod, out


def test_printed_output_two_lines(capsys):
    _, out = _load_module(capsys)
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 2, f"expected={2} actual={len(lines)}"
    assert all(re.fullmatch(r"\d+", ln) for ln in lines), f"expected={'digits'} actual={lines}"


def test_output_values(capsys):
    _, out = _load_module(capsys)
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    nums = list(map(int, lines))
    assert nums == [0, 2], f"expected={[0, 2]} actual={nums}"


def test_empty_is_set_and_mutated(capsys):
    mod, _ = _load_module(capsys)
    assert hasattr(mod, "empty"), f"expected={True} actual={hasattr(mod, 'empty')}"
    assert isinstance(mod.empty, set), f"expected={'set'} actual={type(mod.empty).__name__}"
    assert len(mod.empty) == 2, f"expected={2} actual={len(mod.empty)}"
    assert mod.empty == {"x", "y"}, f"expected={{{'x', 'y'}}} actual={mod.empty}"


def test_no_unexpected_names_in_set(capsys):
    mod, _ = _load_module(capsys)
    assert mod.empty.issubset({"x", "y"}), f"expected={True} actual={mod.empty}"