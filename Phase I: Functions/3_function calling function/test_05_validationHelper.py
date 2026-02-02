import importlib.util
import pathlib
import sys

import pytest


def _load_module():
    path = pathlib.Path(__file__).resolve().parent / "05_validationHelper.py"
    spec = importlib.util.spec_from_file_location("validationHelper_05", str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _assert_eq(actual, expected):
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def _assert_is(actual, expected):
    assert actual is expected, f"expected={expected!r} actual={actual!r}"


@pytest.fixture(scope="module")
def mod():
    return _load_module()


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, True),
        (1, False),
        (2, True),
        (3, False),
        (10, True),
        (11, False),
        (-2, True),
        (-3, False),
        (-10, True),
        (-11, False),
        (2_000_000, True),
        (2_000_001, False),
    ],
)
def test_is_even_basic(mod, n, expected):
    result = mod.is_even(n)
    _assert_is(result, expected)


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, "even"),
        (1, "odd"),
        (2, "even"),
        (7, "odd"),
        (-2, "even"),
        (-7, "odd"),
        (100, "even"),
        (101, "odd"),
    ],
)
def test_describe_parity_returns_string(mod, n, expected):
    result = mod.describe_parity(n)
    _assert_eq(result, expected)


def test_describe_parity_calls_is_even(monkeypatch, mod):
    calls = {"count": 0, "args": []}

    def fake_is_even(x):
        calls["count"] += 1
        calls["args"].append(x)
        return True

    monkeypatch.setattr(mod, "is_even", fake_is_even)
    out = mod.describe_parity(12345)
    _assert_eq(out, "even")
    _assert_eq(calls["count"], 1)
    _assert_eq(calls["args"], [12345])


def test_module_prints_expected_output_on_import(capsys):
    _load_module()
    captured = capsys.readouterr()
    _assert_eq(captured.out, "odd\n")