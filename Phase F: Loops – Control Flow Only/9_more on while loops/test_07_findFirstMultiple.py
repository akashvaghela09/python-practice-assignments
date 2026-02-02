import importlib.util
import sys
from pathlib import Path
import pytest


MODULE_FILE = "07_findFirstMultiple.py"


def run_module_with_input(monkeypatch, inputs):
    it = iter([str(x) for x in inputs])

    def fake_input(prompt=""):
        return next(it)

    monkeypatch.setattr("builtins.input", fake_input)

    module_name = f"_test_module_07_{id(inputs)}"
    spec = importlib.util.spec_from_file_location(module_name, Path(MODULE_FILE))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_value(start, k):
    if start <= 0:
        return k
    r = start % k
    return start if r == 0 else start + (k - r)


@pytest.mark.parametrize(
    "start,k",
    [
        (17, 6),
        (18, 6),
        (1, 1),
        (1, 2),
        (2, 2),
        (3, 2),
        (99, 10),
        (100, 10),
        (101, 10),
        (999, 7),
        (0, 5),
        (-1, 5),
        (-10, 7),
    ],
)
def test_find_first_multiple(monkeypatch, capsys, start, k):
    run_module_with_input(monkeypatch, [start, k])
    out = capsys.readouterr().out.strip()
    assert out != ""
    actual = int(out)
    exp = expected_value(start, k)
    assert actual == exp, f"expected={exp} actual={actual}"


def test_output_is_single_integer_line(monkeypatch, capsys):
    run_module_with_input(monkeypatch, [17, 6])
    out = capsys.readouterr().out
    stripped = out.strip()
    assert stripped != ""
    _ = int(stripped)
    assert "\n" not in stripped, f"expected={1} actual={stripped.count(chr(10))}"


def test_no_extra_input_reads(monkeypatch, capsys):
    calls = {"n": 0}
    inputs = iter(["17", "6"])

    def fake_input(prompt=""):
        calls["n"] += 1
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)
    module_name = f"_test_module_07_calls_{id(calls)}"
    spec = importlib.util.spec_from_file_location(module_name, Path(MODULE_FILE))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    _ = capsys.readouterr()
    assert calls["n"] == 2, f"expected={2} actual={calls['n']}"