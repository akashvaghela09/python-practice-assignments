import builtins
import importlib
import io
import sys
import pytest

MODULE_NAME = "04_sumUntilZero"


def run_module_with_inputs(monkeypatch, inputs):
    it = iter(inputs)

    def fake_input(prompt=""):
        return next(it)

    monkeypatch.setattr(builtins, "input", fake_input)

    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]

    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        importlib.import_module(MODULE_NAME)
    finally:
        sys.stdout = old
    return buf.getvalue()


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (["5", "10", "-3", "0"], "Sum: 12\n"),
        (["0"], "Sum: 0\n"),
        (["1", "2", "3", "0"], "Sum: 6\n"),
        (["-5", "2", "0"], "Sum: -3\n"),
    ],
)
def test_sum_until_zero(monkeypatch, inputs, expected):
    out = run_module_with_inputs(monkeypatch, inputs)
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_stops_at_first_zero(monkeypatch):
    out = run_module_with_inputs(monkeypatch, ["7", "0", "1000"])
    expected = "Sum: 7\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_prints_exactly_one_line(monkeypatch):
    out = run_module_with_inputs(monkeypatch, ["3", "0"])
    lines = out.splitlines(True)
    expected = 1
    actual = len(lines)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert lines[0].endswith("\n"), f"expected={True!r} actual={lines[0].endswith(chr(10))!r}"