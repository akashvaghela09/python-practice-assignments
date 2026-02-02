import importlib.util
import pathlib
import types
import pytest

MODULE_NAME = "08_listProcessingWithHelpers"
FILE_NAME = "08_listProcessingWithHelpers.py"


def load_module():
    path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(path))
    mod = importlib.util.module_from_spec(spec)
    assert isinstance(spec.loader, importlib.abc.Loader)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mod(capsys):
    m = load_module()
    capsys.readouterr()
    return m


def test_print_output_exact(mod, capsys):
    m = load_module()
    out = capsys.readouterr().out
    expected = "[1, 5, 8, 1]\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


@pytest.mark.parametrize(
    "n,low,high,expected",
    [
        (0, 1, 8, 1),
        (5, 1, 8, 5),
        (10, 1, 8, 8),
        (-3, 1, 8, 1),
        (1, 1, 8, 1),
        (8, 1, 8, 8),
        (9, 9, 9, 9),
        (-10, -5, 5, -5),
        (10, -5, 5, 5),
        (-5, -5, 5, -5),
        (5, -5, 5, 5),
        (3.2, 1.1, 3.1, 3.1),
        (1.1, 1.1, 3.1, 1.1),
        (2.5, 1.1, 3.1, 2.5),
    ],
)
def test_clamp_values(mod, n, low, high, expected):
    actual = mod.clamp(n, low, high)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_clamp_all_basic(mod):
    nums = [0, 5, 10, -3]
    low, high = 1, 8
    expected = [1, 5, 8, 1]
    actual = mod.clamp_all(nums, low, high)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_clamp_all_returns_new_list_not_mutating(mod):
    nums = [0, 5, 10, -3]
    original = list(nums)
    res = mod.clamp_all(nums, 1, 8)
    assert nums == original, f"expected={original!r} actual={nums!r}"
    assert res is not nums, f"expected={False!r} actual={(res is nums)!r}"


def test_clamp_all_empty(mod):
    expected = []
    actual = mod.clamp_all([], 0, 1)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_clamp_all_calls_clamp_each_element(monkeypatch):
    m = load_module()
    calls = []

    def fake_clamp(n, low, high):
        calls.append((n, low, high))
        if n < low:
            return low
        if n > high:
            return high
        return n

    monkeypatch.setattr(m, "clamp", fake_clamp)
    nums = [2, -1, 9, 5]
    low, high = 0, 6
    expected_calls = [(2, low, high), (-1, low, high), (9, low, high), (5, low, high)]
    result = m.clamp_all(nums, low, high)
    expected_result = [2, 0, 6, 5]
    assert calls == expected_calls, f"expected={expected_calls!r} actual={calls!r}"
    assert result == expected_result, f"expected={expected_result!r} actual={result!r}"


def test_clamp_all_preserves_length_and_order(mod):
    nums = [3, 2, 1, 0, -1, 4, 10]
    low, high = 1, 3
    expected = [3, 2, 1, 1, 1, 3, 3]
    actual = mod.clamp_all(nums, low, high)
    assert len(actual) == len(nums), f"expected={len(nums)!r} actual={len(actual)!r}"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_clamp_all_accepts_iterable(mod):
    nums = (0, 2, 4)
    expected = [1, 2, 3]
    actual = mod.clamp_all(nums, 1, 3)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"