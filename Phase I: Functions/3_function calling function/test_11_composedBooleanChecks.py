import importlib
import pytest

mod = importlib.import_module("11_composedBooleanChecks")


@pytest.mark.parametrize(
    "s,low,high,expected",
    [
        ("", 0, 0, True),
        ("", 1, 1, False),
        ("a", 1, 1, True),
        ("ab", 1, 1, False),
        ("abc", 2, 3, True),
        ("abc", 4, 10, False),
        ("abcd", 2, 3, False),
        ("abcd", 2, 4, True),
    ],
)
def test_has_length_between_inclusive(s, low, high, expected, capsys):
    actual = mod.has_length_between(s, low, high)
    if actual != expected:
        print(f"expected={expected} actual={actual}")
    assert actual == expected


@pytest.mark.parametrize(
    "s,expected",
    [
        ("", True),
        ("a", True),
        ("Z", True),
        ("AdaLovelace", True),
        ("abcXYZ", True),
        ("abc123", False),
        ("123", False),
        ("abc_def", False),
        ("abc-def", False),
        ("abc def", False),
        ("ä", False),
        ("ß", False),
        ("Aß", False),
        ("\n", False),
    ],
)
def test_is_alpha_only_ascii_letters_only(s, expected, capsys):
    actual = mod.is_alpha_only(s)
    if actual != expected:
        print(f"expected={expected} actual={actual}")
    assert actual == expected


def test_is_valid_username_calls_helpers(monkeypatch, capsys):
    calls = {"len": 0, "alpha": 0}

    def fake_len(s, low, high):
        calls["len"] += 1
        return True

    def fake_alpha(s):
        calls["alpha"] += 1
        return True

    monkeypatch.setattr(mod, "has_length_between", fake_len)
    monkeypatch.setattr(mod, "is_alpha_only", fake_alpha)

    actual = mod.is_valid_username("Anything")
    expected = True
    if actual != expected:
        print(f"expected={expected} actual={actual}")
    assert actual == expected
    assert calls["len"] == 1
    assert calls["alpha"] == 1


@pytest.mark.parametrize(
    "len_ok,alpha_ok,expected",
    [
        (True, True, True),
        (True, False, False),
        (False, True, False),
        (False, False, False),
    ],
)
def test_is_valid_username_composition(monkeypatch, len_ok, alpha_ok, expected, capsys):
    def fake_len(s, low, high):
        return len_ok

    def fake_alpha(s):
        return alpha_ok

    monkeypatch.setattr(mod, "has_length_between", fake_len)
    monkeypatch.setattr(mod, "is_alpha_only", fake_alpha)

    actual = mod.is_valid_username("X")
    if actual != expected:
        print(f"expected={expected} actual={actual}")
    assert actual == expected


@pytest.mark.parametrize(
    "s,expected",
    [
        ("AdaLovelace", True),
        ("A", True),
        ("", True),
        ("A1", False),
        ("John_Doe", False),
    ],
)
def test_is_valid_username_matches_helpers_default_constraints(s, expected, capsys):
    # Infer intended constraints from direct helper usage by using a standard range likely expected.
    # Here we only verify behavior is consistent with both helpers when composed with the same inputs.
    # If is_valid_username uses different length bounds, this test will still catch inconsistencies
    # by checking implication with helpers for the returned result.
    actual = mod.is_valid_username(s)

    # If valid, it must be alpha-only and satisfy some inclusive length check; we can at least enforce alpha-only.
    if expected:
        if mod.is_alpha_only(s) is not True:
            print(f"expected={True} actual={mod.is_alpha_only(s)}")
        assert mod.is_alpha_only(s) is True
    else:
        # For clearly invalid alpha cases, it must be False.
        if mod.is_alpha_only(s) is False:
            if actual is not False:
                print(f"expected={False} actual={actual}")
            assert actual is False
            return

    if actual != expected:
        print(f"expected={expected} actual={actual}")
    assert actual == expected