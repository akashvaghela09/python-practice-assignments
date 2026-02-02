import importlib
import pytest

mod = importlib.import_module("06_nestedCallsInExpression")


@pytest.mark.parametrize(
    "a,b",
    [
        (0, 0),
        (1, 2),
        (-1, 1),
        (-5, -7),
        (10, -3),
        (3.5, 2.25),
    ],
)
def test_add(a, b):
    expected = a + b
    actual = mod.add(a, b)
    assert actual == expected, f"expected={expected} actual={actual}"


@pytest.mark.parametrize(
    "n",
    [
        0,
        1,
        -1,
        7,
        -12,
        2.5,
        -3.75,
    ],
)
def test_double(n):
    expected = n * 2
    actual = mod.double(n)
    assert actual == expected, f"expected={expected} actual={actual}"


@pytest.mark.parametrize(
    "a,b,c",
    [
        (2, 3, 4),
        (0, 0, 0),
        (1, 2, 3),
        (-2, 5, 10),
        (10, -3, -4),
        (1.5, 2.25, -3.0),
        (-1.25, -2.75, 10.0),
    ],
)
def test_compute(a, b, c):
    expected = (a + b) * 2 + c
    actual = mod.compute(a, b, c)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_compute_calls_helpers(monkeypatch):
    calls = {"add": 0, "double": 0}

    def add_spy(a, b):
        calls["add"] += 1
        return a + b

    def double_spy(n):
        calls["double"] += 1
        return n * 2

    monkeypatch.setattr(mod, "add", add_spy)
    monkeypatch.setattr(mod, "double", double_spy)

    a, b, c = 6, -2, 9
    expected = (a + b) * 2 + c
    actual = mod.compute(a, b, c)

    assert actual == expected, f"expected={expected} actual={actual}"
    assert calls["add"] >= 1, f"expected={1} actual={calls['add']}"
    assert calls["double"] >= 1, f"expected={1} actual={calls['double']}"


def test_printed_example_output(capsys, monkeypatch):
    importlib.reload(mod)
    captured = capsys.readouterr()
    lines = [ln for ln in captured.out.splitlines() if ln.strip() != ""]
    assert len(lines) >= 1, f"expected={1} actual={len(lines)}"
    expected = "14"
    actual = lines[-1].strip()
    assert actual == expected, f"expected={expected} actual={actual}"