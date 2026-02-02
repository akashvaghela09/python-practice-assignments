import builtins
import importlib.util
import io
import os
import sys
import types
import pytest

MODULE_FILE = "07_primeCheckWithBreak.py"


def _run_with_input(monkeypatch, inp: str):
    it = iter([inp])

    def fake_input(prompt=None):
        return next(it)

    monkeypatch.setattr(builtins, "input", fake_input)

    buf = io.StringIO()
    old_out = sys.stdout
    sys.stdout = buf
    try:
        name = f"mod_{os.path.splitext(MODULE_FILE)[0]}_{abs(hash(inp))}"
        spec = importlib.util.spec_from_file_location(name, MODULE_FILE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old_out
    return buf.getvalue()


@pytest.mark.parametrize(
    "n, expected",
    [
        ("29", "Prime\n"),
        ("30", "Not prime\n"),
    ],
)
def test_sample_outputs(monkeypatch, n, expected):
    out = _run_with_input(monkeypatch, n)
    assert out == expected, f"expected={expected!r} actual={out!r}"


@pytest.mark.parametrize(
    "n, expected",
    [
        ("-5", "Not prime\n"),
        ("0", "Not prime\n"),
        ("1", "Not prime\n"),
        ("2", "Prime\n"),
        ("3", "Prime\n"),
        ("4", "Not prime\n"),
        ("5", "Prime\n"),
        ("9", "Not prime\n"),
        ("49", "Not prime\n"),
        ("97", "Prime\n"),
        ("121", "Not prime\n"),
    ],
)
def test_various_numbers(monkeypatch, n, expected):
    out = _run_with_input(monkeypatch, n)
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_prints_exactly_one_line(monkeypatch):
    out = _run_with_input(monkeypatch, "11")
    lines = out.splitlines()
    assert len(lines) == 1, f"expected={1!r} actual={len(lines)!r}"
    assert lines[0] in ("Prime", "Not prime"), f"expected={('Prime','Not prime')!r} actual={(lines[0],)!r}"


def test_uses_break_in_while_loop():
    import ast

    with open(MODULE_FILE, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=MODULE_FILE)

    while_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.While)]
    assert len(while_nodes) >= 1, f"expected={'>=1'!r} actual={len(while_nodes)!r}"

    has_break_inside_while = False
    for w in while_nodes:
        if any(isinstance(x, ast.Break) for x in ast.walk(w)):
            has_break_inside_while = True
            break

    assert has_break_inside_while is True, f"expected={True!r} actual={has_break_inside_while!r}"


def test_does_not_use_for_loop():
    import ast

    with open(MODULE_FILE, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=MODULE_FILE)

    for_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.For)]
    assert len(for_nodes) == 0, f"expected={0!r} actual={len(for_nodes)!r}"