import importlib.util
import os
import pytest

MODULE_FILENAME = "14_dispatcherFunction.py"
MODULE_NAME = "dispatcherFunction14"


def load_module():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_import_prints_expected_value(capsys):
    load_module()
    captured = capsys.readouterr()
    out = captured.out
    assert out == "42\n", f"expected={repr('42\\n')} actual={repr(out)}"


def test_add_basic():
    m = load_module()
    expected = 5
    actual = m.add(2, 3)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_sub_basic():
    m = load_module()
    expected = 5
    actual = m.sub(8, 3)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_mul_basic():
    m = load_module()
    expected = 12
    actual = m.mul(3, 4)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_calculate_dispatches_correctly_add(monkeypatch):
    m = load_module()
    calls = {"add": 0, "sub": 0, "mul": 0}

    def add(a, b):
        calls["add"] += 1
        return 999

    def sub(a, b):
        calls["sub"] += 1
        return 888

    def mul(a, b):
        calls["mul"] += 1
        return 777

    monkeypatch.setattr(m, "add", add)
    monkeypatch.setattr(m, "sub", sub)
    monkeypatch.setattr(m, "mul", mul)

    expected = 999
    actual = m.calculate("+", 1, 2)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert calls == {"add": 1, "sub": 0, "mul": 0}, f"expected={{{'add': 1, 'sub': 0, 'mul': 0}}!r} actual={calls!r}"


def test_calculate_dispatches_correctly_sub(monkeypatch):
    m = load_module()
    calls = {"add": 0, "sub": 0, "mul": 0}

    def add(a, b):
        calls["add"] += 1
        return 999

    def sub(a, b):
        calls["sub"] += 1
        return 888

    def mul(a, b):
        calls["mul"] += 1
        return 777

    monkeypatch.setattr(m, "add", add)
    monkeypatch.setattr(m, "sub", sub)
    monkeypatch.setattr(m, "mul", mul)

    expected = 888
    actual = m.calculate("-", 7, 5)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert calls == {"add": 0, "sub": 1, "mul": 0}, f"expected={{{'add': 0, 'sub': 1, 'mul': 0}}!r} actual={calls!r}"


def test_calculate_dispatches_correctly_mul(monkeypatch):
    m = load_module()
    calls = {"add": 0, "sub": 0, "mul": 0}

    def add(a, b):
        calls["add"] += 1
        return 999

    def sub(a, b):
        calls["sub"] += 1
        return 888

    def mul(a, b):
        calls["mul"] += 1
        return 777

    monkeypatch.setattr(m, "add", add)
    monkeypatch.setattr(m, "sub", sub)
    monkeypatch.setattr(m, "mul", mul)

    expected = 777
    actual = m.calculate("*", 6, 7)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert calls == {"add": 0, "sub": 0, "mul": 1}, f"expected={{{'add': 0, 'sub': 0, 'mul': 1}}!r} actual={calls!r}"


def test_calculate_unsupported_returns_string(monkeypatch):
    m = load_module()

    def boom(*args, **kwargs):
        raise AssertionError("should not be called")

    monkeypatch.setattr(m, "add", boom)
    monkeypatch.setattr(m, "sub", boom)
    monkeypatch.setattr(m, "mul", boom)

    expected = "unsupported"
    actual = m.calculate("/", 10, 2)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        ("+", -2, 3, 1),
        ("-", -2, 3, -5),
        ("*", -2, 3, -6),
        ("+", 0, 0, 0),
        ("*", 0, 99, 0),
    ],
)
def test_calculate_numeric_results(op, a, b, expected):
    m = load_module()
    actual = m.calculate(op, a, b)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"