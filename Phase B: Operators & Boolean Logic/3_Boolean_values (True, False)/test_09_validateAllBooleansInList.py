import importlib.util
import os
import pytest

MODULE_FILENAME = "09_validateAllBooleansInList.py"
MODULE_NAME = "assignment09_validateAllBooleansInList"


def _load_module():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_bools_true_when_all_are_exact_bools(capsys):
    m = _load_module()
    capsys.readouterr()
    actual = m.all_bools([True, False, True, True, False])
    expected = True
    assert actual == expected, f"expected={expected} actual={actual}"


@pytest.mark.parametrize(
    "values",
    [
        [True, 1, False],
        [0, False],
        [True, 2],
        [True, None],
        [True, "False"],
        [True, 0.0],
        [True, object()],
    ],
)
def test_all_bools_false_when_any_non_bool(values, capsys):
    m = _load_module()
    capsys.readouterr()
    actual = m.all_bools(values)
    expected = False
    assert actual == expected, f"expected={expected} actual={actual}"


def test_all_bools_empty_list_returns_false(capsys):
    m = _load_module()
    capsys.readouterr()
    actual = m.all_bools([])
    expected = False
    assert actual == expected, f"expected={expected} actual={actual}"


def test_all_bools_accepts_bool_subclass_but_requires_exact_type(capsys):
    m = _load_module()
    capsys.readouterr()

    class MyBool(bool):
        pass

    actual = m.all_bools([True, MyBool(True), False])
    expected = False
    assert actual == expected, f"expected={expected} actual={actual}"


def test_module_prints_three_lines_with_expected_outputs(capsys):
    _load_module()
    captured = capsys.readouterr()
    lines = [ln.strip() for ln in captured.out.splitlines() if ln.strip() != ""]
    assert len(lines) == 3, f"expected={3} actual={len(lines)}"

    expected_lines = ["True", "False", "False"]
    for i, (exp, act) in enumerate(zip(expected_lines, lines)):
        assert act == exp, f"expected={exp} actual={act}"