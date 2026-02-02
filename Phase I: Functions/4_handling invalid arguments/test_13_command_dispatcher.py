import pytest

from 13_command_dispatcher import dispatch


def test_add_valid_integers():
    expected = 5
    actual = dispatch("add", 2, 3)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_add_valid_floats():
    expected = 3.75
    actual = dispatch("add", 1.5, 2.25)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_pow_valid_zero_exponent():
    expected = 1
    actual = dispatch("pow", 7, 0)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_pow_valid_positive_exponent():
    expected = 8
    actual = dispatch("pow", 2, 3)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_echo_valid_string():
    expected = "hello"
    actual = dispatch("echo", "hello")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


@pytest.mark.parametrize("cmd", [None, 1, 1.0, [], {}, object()])
def test_command_must_be_str(cmd):
    with pytest.raises(TypeError) as ei:
        dispatch(cmd, 1, 2)
    assert str(ei.value) == "command must be a str"


def test_unknown_command_raises_value_error():
    with pytest.raises(ValueError) as ei:
        dispatch("noop")
    assert str(ei.value) == "unknown command"


@pytest.mark.parametrize(
    "args",
    [
        (),
        (1,),
        (1, 2, 3),
    ],
)
def test_add_wrong_number_of_arguments(args):
    with pytest.raises(TypeError) as ei:
        dispatch("add", *args)
    assert str(ei.value) == "wrong number of arguments"


@pytest.mark.parametrize(
    "args",
    [
        (1,),
        (1, 2, 3),
        (),
    ],
)
def test_pow_wrong_number_of_arguments(args):
    with pytest.raises(TypeError) as ei:
        dispatch("pow", *args)
    assert str(ei.value) == "wrong number of arguments"


@pytest.mark.parametrize(
    "args",
    [
        (),
        ("x", "y"),
        ("x",),
        ("x", 1),
    ],
)
def test_echo_wrong_number_of_arguments(args):
    with pytest.raises(TypeError) as ei:
        dispatch("echo", *args)
    assert str(ei.value) == "wrong number of arguments"


@pytest.mark.parametrize(
    "a,b",
    [
        ("1", 2),
        (1, "2"),
        ("1", "2"),
        (None, 2),
        (1, None),
        ([1], 2),
        (1, [2]),
    ],
)
def test_add_invalid_argument_types(a, b):
    with pytest.raises(TypeError) as ei:
        dispatch("add", a, b)
    assert str(ei.value) == "invalid argument type"


@pytest.mark.parametrize(
    "base,exp",
    [
        ("2", 3),
        (2, "3"),
        (None, 3),
        (2, None),
        ([2], 3),
        (2, [3]),
    ],
)
def test_pow_invalid_argument_types(base, exp):
    with pytest.raises(TypeError) as ei:
        dispatch("pow", base, exp)
    assert str(ei.value) == "invalid argument type"


@pytest.mark.parametrize(
    "s",
    [1, 1.0, None, [], {}, object()],
)
def test_echo_invalid_argument_type(s):
    with pytest.raises(TypeError) as ei:
        dispatch("echo", s)
    assert str(ei.value) == "invalid argument type"


@pytest.mark.parametrize(
    "exp",
    [-1, -2, 1.5, True, False],
)
def test_pow_invalid_exponent_values(exp):
    with pytest.raises(ValueError) as ei:
        dispatch("pow", 2, exp)
    assert str(ei.value) == "exponent must be a non-negative int"