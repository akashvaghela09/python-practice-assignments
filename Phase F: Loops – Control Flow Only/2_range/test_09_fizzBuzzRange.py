import importlib
import sys
import types
import builtins
import pytest


MODULE_NAME = "09_fizzBuzzRange"


def _run_module_capture_output(monkeypatch):
    output = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        s = sep.join(str(a) for a in args) + end
        output.append(s)

    monkeypatch.setattr(builtins, "print", fake_print)

    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]

    importlib.import_module(MODULE_NAME)

    text = "".join(output)
    lines = text.splitlines()
    return lines, text


def test_fizzbuzz_prints_15_lines(monkeypatch):
    lines, _ = _run_module_capture_output(monkeypatch)
    assert len(lines) == 15, f"expected=15 actual={len(lines)}"


def test_fizzbuzz_exact_sequence(monkeypatch):
    lines, _ = _run_module_capture_output(monkeypatch)
    expected = [
        "1",
        "2",
        "Fizz",
        "4",
        "Buzz",
        "Fizz",
        "7",
        "8",
        "Fizz",
        "Buzz",
        "11",
        "Fizz",
        "13",
        "14",
        "FizzBuzz",
    ]
    assert lines == expected, f"expected={expected!r} actual={lines!r}"


@pytest.mark.parametrize(
    "idx, expected",
    [
        (0, "1"),
        (2, "Fizz"),
        (4, "Buzz"),
        (8, "Fizz"),
        (9, "Buzz"),
        (14, "FizzBuzz"),
    ],
)
def test_fizzbuzz_key_positions(monkeypatch, idx, expected):
    lines, _ = _run_module_capture_output(monkeypatch)
    actual = lines[idx] if idx < len(lines) else None
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_fizzbuzz_lines_are_nonempty(monkeypatch):
    lines, _ = _run_module_capture_output(monkeypatch)
    empties = [i for i, s in enumerate(lines) if s == ""]
    assert empties == [], f"expected={[]} actual={empties}"


def test_fizzbuzz_only_allowed_tokens(monkeypatch):
    lines, _ = _run_module_capture_output(monkeypatch)
    allowed = {str(i) for i in range(1, 16)} | {"Fizz", "Buzz", "FizzBuzz"}
    bad = [(i, s) for i, s in enumerate(lines) if s not in allowed]
    assert bad == [], f"expected={[]} actual={bad}"