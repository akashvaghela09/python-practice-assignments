import importlib.util
import os
import sys
import pytest


MODULE_FILENAME = "10_customRangeGenerator.py"
MODULE_NAME = "customRangeGenerator_10"


def _load_module():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


def _expected(start, stop, step):
    return list(range(start, stop, step))


def test_import_and_has_my_range(capsys):
    try:
        m = _load_module()
    except Exception as e:
        pytest.fail(f"expected importable module, actual error={type(e).__name__}: {e}")
    assert hasattr(m, "my_range")
    assert callable(m.my_range)


@pytest.mark.parametrize(
    "start,stop,step",
    [
        (2, 11, 3),
        (0, 1, 1),
        (5, 5, 2),
        (0, 10, 1),
        (0, 10, 2),
        (1, 10, 3),
        (-5, 6, 2),
        (-5, -4, 1),
        (-5, -5, 1),
        (7, 8, 10),
        (7, 7, 10),
        (9, 0, 1),
        (9, 0, 4),
        (-1, -10, 2),
        (100, 130, 7),
    ],
)
def test_matches_builtin_range_for_positive_step(start, stop, step):
    try:
        m = _load_module()
    except Exception as e:
        pytest.fail(f"expected importable module, actual error={type(e).__name__}: {e}")

    expected = _expected(start, stop, step)
    try:
        actual = m.my_range(start, stop, step)
    except Exception as e:
        pytest.fail(
            f"expected my_range to return list, actual error={type(e).__name__}: {e}"
        )

    if actual != expected:
        pytest.fail(f"expected={expected} actual={actual}")


def test_returns_list_type():
    try:
        m = _load_module()
    except Exception as e:
        pytest.fail(f"expected importable module, actual error={type(e).__name__}: {e}")

    out = m.my_range(0, 3, 1)
    if not isinstance(out, list):
        pytest.fail(f"expected={list} actual={type(out)}")


def test_does_not_mutate_return_between_calls():
    try:
        m = _load_module()
    except Exception as e:
        pytest.fail(f"expected importable module, actual error={type(e).__name__}: {e}")

    a = m.my_range(0, 5, 2)
    b = m.my_range(0, 5, 2)
    if a is b:
        pytest.fail(f"expected=different_objects actual=same_object")
    a.append("sentinel")
    expected_b = _expected(0, 5, 2)
    if b != expected_b:
        pytest.fail(f"expected={expected_b} actual={b}")