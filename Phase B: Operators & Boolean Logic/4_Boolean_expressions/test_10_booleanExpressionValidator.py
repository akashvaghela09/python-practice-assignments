import importlib.util
import pathlib
import sys
import pytest


def _load_module():
    path = pathlib.Path(__file__).resolve().parent / "10_booleanExpressionValidator.py"
    spec = importlib.util.spec_from_file_location("mod10_booleanExpressionValidator", str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_import_does_not_raise():
    _load_module()


@pytest.fixture
def mod():
    return _load_module()


def test_module_prints_expected_lines_on_import(capsys):
    _load_module()
    out = capsys.readouterr().out
    assert out == "True\nFalse\nFalse\nTrue\n", f"expected={repr('True\\nFalse\\nFalse\\nTrue\\n')} actual={repr(out)}"


@pytest.mark.parametrize(
    "pw, expected",
    [
        ("tiger123", True),
        ("password", False),
        ("no digits", False),
        ("abc123 45", True),
        ("1234567", False),
        ("12345678", True),
        ("abcdefgh", False),
        ("abcd efgh1", False),
        ("pass word1", False),
        ("Password1", True),
        ("password1", True),
        ("pa ssword", False),
        ("", False),
        ("        1", False),
        ("        1x", False),
        ("a1b2c3d4", True),
    ],
)
def test_is_password_acceptable_cases(mod, pw, expected):
    actual = mod.is_password_acceptable(pw)
    assert actual is expected, f"expected={expected!r} actual={actual!r}"


def test_spaces_disallowed(mod):
    pw = "abcd1234 "
    expected = False
    actual = mod.is_password_acceptable(pw)
    assert actual is expected, f"expected={expected!r} actual={actual!r}"


def test_banned_exact_password_only(mod):
    expected = False
    actual = mod.is_password_acceptable("password")
    assert actual is expected, f"expected={expected!r} actual={actual!r}"

    expected2 = True
    actual2 = mod.is_password_acceptable("password2")
    assert actual2 is expected2, f"expected={expected2!r} actual={actual2!r}"


def test_requires_at_least_one_digit(mod):
    expected = False
    actual = mod.is_password_acceptable("abcdefgh")
    assert actual is expected, f"expected={expected!r} actual={actual!r}"

    expected2 = True
    actual2 = mod.is_password_acceptable("abcdefg1")
    assert actual2 is expected2, f"expected={expected2!r} actual={actual2!r}"


def test_length_rule(mod):
    expected = False
    actual = mod.is_password_acceptable("a1b2c3d")
    assert actual is expected, f"expected={expected!r} actual={actual!r}"

    expected2 = True
    actual2 = mod.is_password_acceptable("a1b2c3d4")
    assert actual2 is expected2, f"expected={expected2!r} actual={actual2!r}"


def test_return_type_bool(mod):
    actual = mod.is_password_acceptable("a1b2c3d4")
    assert isinstance(actual, bool), f"expected={bool!r} actual={type(actual)!r}"