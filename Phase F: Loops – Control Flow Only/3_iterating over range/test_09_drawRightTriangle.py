import builtins
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout

import pytest


ASSIGNMENT_FILE = "09_drawRightTriangle.py"


def load_module_with_input(monkeypatch, input_data: str):
    it = iter(input_data.splitlines())

    def fake_input(prompt=None):
        return next(it)

    monkeypatch.setattr(builtins, "input", fake_input)

    module_name = f"student_mod_{os.urandom(8).hex()}"
    spec = importlib.util.spec_from_file_location(module_name, ASSIGNMENT_FILE)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with redirect_stdout(buf):
        try:
            spec.loader.exec_module(mod)  # type: ignore[attr-defined]
        except Exception as e:
            return e, buf.getvalue()
    return None, buf.getvalue()


def expected_triangle(h: int) -> str:
    lines = ["#" * i for i in range(1, h + 1)]
    return "\n".join(lines) + ("\n" if h > 0 else "")


@pytest.mark.parametrize("h", [1, 2, 4, 7])
def test_triangle_basic_heights(monkeypatch, h):
    err, out = load_module_with_input(monkeypatch, f"{h}\n")
    assert err is None, f"expected={None!r} actual={err!r}"
    exp = expected_triangle(h)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_triangle_height_three_exact(monkeypatch):
    h = 3
    err, out = load_module_with_input(monkeypatch, f"{h}\n")
    assert err is None, f"expected={None!r} actual={err!r}"
    exp = expected_triangle(h)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_triangle_uses_only_hashes_and_newlines(monkeypatch):
    h = 6
    err, out = load_module_with_input(monkeypatch, f"{h}\n")
    assert err is None, f"expected={None!r} actual={err!r}"
    exp = expected_triangle(h)
    assert out == exp, f"expected={exp!r} actual={out!r}"
    allowed = set("#\n")
    assert set(out).issubset(allowed), f"expected={allowed!r} actual={set(out)!r}"


@pytest.mark.parametrize("h", [5, 8])
def test_line_lengths_increase_by_one(monkeypatch, h):
    err, out = load_module_with_input(monkeypatch, f"{h}\n")
    assert err is None, f"expected={None!r} actual={err!r}"
    lines = out.splitlines()
    exp_lines = expected_triangle(h).splitlines()
    assert lines == exp_lines, f"expected={exp_lines!r} actual={lines!r}"
    lengths = [len(line) for line in lines]
    exp_lengths = list(range(1, h + 1))
    assert lengths == exp_lengths, f"expected={exp_lengths!r} actual={lengths!r}"


def test_zero_height_produces_no_output(monkeypatch):
    h = 0
    err, out = load_module_with_input(monkeypatch, f"{h}\n")
    assert err is None, f"expected={None!r} actual={err!r}"
    exp = expected_triangle(h)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_negative_height_produces_no_output(monkeypatch):
    h = -3
    err, out = load_module_with_input(monkeypatch, f"{h}\n")
    assert err is None, f"expected={None!r} actual={err!r}"
    exp = expected_triangle(h)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_trailing_newline_present_for_positive(monkeypatch):
    h = 4
    err, out = load_module_with_input(monkeypatch, f"{h}\n")
    assert err is None, f"expected={None!r} actual={err!r}"
    exp = expected_triangle(h)
    assert out == exp, f"expected={exp!r} actual={out!r}"
    assert out.endswith("\n") is True, f"expected={True!r} actual={out.endswith(chr(10))!r}"


def test_no_extra_blank_lines(monkeypatch):
    h = 9
    err, out = load_module_with_input(monkeypatch, f"{h}\n")
    assert err is None, f"expected={None!r} actual={err!r}"
    exp = expected_triangle(h)
    assert out == exp, f"expected={exp!r} actual={out!r}"
    lines = out.splitlines()
    exp_lines = exp.splitlines()
    assert len(lines) == len(exp_lines), f"expected={len(exp_lines)!r} actual={len(lines)!r}"