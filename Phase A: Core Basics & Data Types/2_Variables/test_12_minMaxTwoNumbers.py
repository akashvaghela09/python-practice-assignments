import builtins
import importlib
import sys
import pytest

MODULE_NAME = "12_minMaxTwoNumbers"


def run_module_with_inputs(monkeypatch, capsys, inputs):
    it = iter([str(x) for x in inputs])

    def fake_input(prompt=None):
        return next(it)

    monkeypatch.setattr(builtins, "input", fake_input)

    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]

    importlib.import_module(MODULE_NAME)
    return capsys.readouterr().out


def parse_output(out):
    lines = [ln.rstrip("\n") for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 2, f"expected=2 actual={len(lines)}"
    assert lines[0].startswith("min="), f"expected=min= actual={lines[0]}"
    assert lines[1].startswith("max="), f"expected=max= actual={lines[1]}"
    min_s = lines[0][4:]
    max_s = lines[1][4:]
    try:
        min_v = int(min_s)
    except Exception:
        raise AssertionError(f"expected=int actual={min_s}")
    try:
        max_v = int(max_s)
    except Exception:
        raise AssertionError(f"expected=int actual={max_s}")
    return min_v, max_v


@pytest.mark.parametrize(
    "a,b",
    [
        (9, 2),
        (2, 9),
        (5, 5),
        (-1, 3),
        (3, -1),
        (-10, -20),
        (-20, -10),
        (0, 0),
        (0, 7),
        (7, 0),
    ],
)
def test_min_max_values(monkeypatch, capsys, a, b):
    out = run_module_with_inputs(monkeypatch, capsys, [a, b])
    min_v, max_v = parse_output(out)
    expected_min = a if a <= b else b
    expected_max = a if a >= b else b
    assert min_v == expected_min, f"expected={expected_min} actual={min_v}"
    assert max_v == expected_max, f"expected={expected_max} actual={max_v}"


def test_output_format_no_extra_lines(monkeypatch, capsys):
    out = run_module_with_inputs(monkeypatch, capsys, [1, 2])
    lines = [ln.rstrip("\n") for ln in out.splitlines()]
    nonempty = [ln for ln in lines if ln.strip() != ""]
    assert len(nonempty) == 2, f"expected=2 actual={len(nonempty)}"
    assert nonempty[0].startswith("min="), f"expected=min= actual={nonempty[0]}"
    assert nonempty[1].startswith("max="), f"expected=max= actual={nonempty[1]}"


def test_missing_variables_fail(monkeypatch, capsys):
    with pytest.raises(NameError):
        run_module_with_inputs(monkeypatch, capsys, [1, 2])