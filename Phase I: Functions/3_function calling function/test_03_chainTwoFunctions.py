import importlib.util
import io
import os
import contextlib
import pytest

MODULE_PATH = os.path.join(os.path.dirname(__file__), "03_chainTwoFunctions.py")


def load_module():
    spec = importlib.util.spec_from_file_location("chain_two_functions", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        spec.loader.exec_module(module)
    return module, stdout.getvalue()


def test_module_prints_expected_output():
    _, out = load_module()
    expected = "GRACE\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


@pytest.mark.parametrize(
    "s, expected",
    [
        ("  grace  ", "grace"),
        ("grace  ", "grace"),
        ("  grace", "grace"),
        ("grace", "grace"),
        ("   ", ""),
        ("", ""),
        ("\t grace \n", "grace"),
        ("  gr ace  ", "gr ace"),
        ("  GrAcE  ", "GrAcE"),
    ],
)
def test_strip_spaces_behavior(s, expected):
    m, _ = load_module()
    actual = m.strip_spaces(s)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


@pytest.mark.parametrize(
    "s, expected",
    [
        ("  grace  ", "GRACE"),
        ("grace", "GRACE"),
        ("  GrAcE  ", "GRACE"),
        ("  gr ace  ", "GR ACE"),
        ("   ", ""),
        ("", ""),
        ("\t grace \n", "GRACE"),
    ],
)
def test_normalize_name_behavior(s, expected):
    m, _ = load_module()
    actual = m.normalize_name(s)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_normalize_name_calls_strip_spaces(monkeypatch):
    m, _ = load_module()

    called = {"count": 0}

    def spy_strip_spaces(x):
        called["count"] += 1
        return x.strip()

    monkeypatch.setattr(m, "strip_spaces", spy_strip_spaces)
    actual = m.normalize_name("  a  ")
    expected = "A"
    assert called["count"] == 1, f"expected={1!r} actual={called['count']!r}"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_strip_spaces_returns_string_type():
    m, _ = load_module()
    actual = m.strip_spaces("  x  ")
    assert isinstance(actual, str), f"expected={str!r} actual={type(actual)!r}"


def test_normalize_name_returns_string_type():
    m, _ = load_module()
    actual = m.normalize_name("  x  ")
    assert isinstance(actual, str), f"expected={str!r} actual={type(actual)!r}"