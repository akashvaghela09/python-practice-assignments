import pytest

from 14_dataclass_argument_validation import UserInput


def assert_raises(exc_type, msg, func, *args, **kwargs):
    with pytest.raises(exc_type) as ei:
        func(*args, **kwargs)
    actual = str(ei.value)
    assert actual == msg, f"expected={msg!r} actual={actual!r}"


def test_valid_construction():
    u = UserInput("alice_1", 30, "a@b.com")
    assert u.username == "alice_1", f"expected={'alice_1'!r} actual={u.username!r}"
    assert u.age == 30, f"expected={30!r} actual={u.age!r}"
    assert u.email == "a@b.com", f"expected={'a@b.com'!r} actual={u.email!r}"


@pytest.mark.parametrize(
    "username",
    ["ab", "a" * 21, "a!", "a-b", "a b", "äbc", "a.b", ""],
)
def test_invalid_username_value(username):
    assert_raises(ValueError, "invalid username", UserInput, username, 30, "a@b.com")


@pytest.mark.parametrize("username", [None, 123, ["alice"], {"u": "alice"}, b"alice"])
def test_invalid_username_type(username):
    assert_raises(TypeError, "username must be a str", UserInput, username, 30, "a@b.com")


@pytest.mark.parametrize(
    "age",
    [12, 121, -1, 0, 999999],
)
def test_invalid_age_value(age):
    assert_raises(ValueError, "invalid age", UserInput, "alice_1", age, "a@b.com")


@pytest.mark.parametrize("age", [True, False])
def test_invalid_age_type_bool(age):
    assert_raises(TypeError, "age must be an int", UserInput, "alice_1", age, "a@b.com")


@pytest.mark.parametrize("age", [None, 13.0, "30", b"30", [30]])
def test_invalid_age_type_non_int(age):
    assert_raises(TypeError, "age must be an int", UserInput, "alice_1", age, "a@b.com")


@pytest.mark.parametrize("age", [13, 120])
def test_age_boundary_values(age):
    u = UserInput("alice_1", age, "a@b.com")
    assert u.age == age, f"expected={age!r} actual={u.age!r}"


@pytest.mark.parametrize(
    "email",
    [
        "ab.com",
        "a@@b.com",
        "a@b",
        "a@b.",
        "a@.com",
        "@b.com",
        "a@bcom",
        "a@b..com",
        "a@bcom.",
        "a@bcom..",
        "a@bcom.c",
    ],
)
def test_invalid_email_value(email):
    assert_raises(ValueError, "invalid email", UserInput, "alice_1", 30, email)


@pytest.mark.parametrize("email", [None, 123, ["a@b.com"], {"e": "a@b.com"}, b"a@b.com"])
def test_invalid_email_type(email):
    assert_raises(TypeError, "email must be a str", UserInput, "alice_1", 30, email)


def test_valid_email_with_multiple_dots_after_at():
    u = UserInput("alice_1", 30, "a@b.co.uk")
    assert u.email == "a@b.co.uk", f"expected={'a@b.co.uk'!r} actual={u.email!r}"


def test_expected_examples():
    u = UserInput("alice_1", 30, "a@b.com")
    assert u.username == "alice_1", f"expected={'alice_1'!r} actual={u.username!r}"

    assert_raises(ValueError, "invalid username", UserInput, "a!", 30, "a@b.com")
    assert_raises(TypeError, "age must be an int", UserInput, "alice", True, "a@b.com")