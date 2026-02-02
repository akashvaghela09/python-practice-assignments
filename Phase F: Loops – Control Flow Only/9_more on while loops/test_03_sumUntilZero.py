import runpy
import builtins
import pytest


def run_program(monkeypatch, inputs):
    it = iter(inputs)

    def fake_input(prompt=""):
        return next(it)

    monkeypatch.setattr(builtins, "input", fake_input)
    return runpy.run_module("03_sumUntilZero", run_name="__main__")


@pytest.mark.parametrize(
    "inputs, expected_total",
    [
        (["0"], 0),
        (["5", "-2", "7", "0"], 10),
        (["1", "2", "3", "0"], 6),
        (["-1", "-2", "-3", "0"], -6),
        (["10", "0", "999"], 10),
        (["0", "1", "2"], 0),
    ],
)
def test_sum_until_zero_total(monkeypatch, inputs, expected_total, capsys):
    ns = run_program(monkeypatch, inputs)
    out = capsys.readouterr().out.strip()

    assert ns.get("total") == expected_total, f"expected={expected_total} actual={ns.get('total')}"
    assert out == str(expected_total), f"expected={expected_total} actual={out}"


def test_reads_until_first_zero_only(monkeypatch, capsys):
    ns = run_program(monkeypatch, ["3", "4", "0", "100", "-50", "0"])
    out = capsys.readouterr().out.strip()
    expected_total = 7

    assert ns.get("total") == expected_total, f"expected={expected_total} actual={ns.get('total')}"
    assert out == str(expected_total), f"expected={expected_total} actual={out}"


def test_non_integer_input_raises(monkeypatch):
    with pytest.raises(ValueError):
        run_program(monkeypatch, ["1", "x", "0"])