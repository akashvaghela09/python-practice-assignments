import ast
import importlib.util
import os
import sys
import pytest


MODULE_NAME = "08_replaceStringsCaseInsensitive"
FILE_NAME = MODULE_NAME + ".py"


def _load_module_from_path(path):
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules.pop(MODULE_NAME, None)
    spec.loader.exec_module(module)
    return module


def _capture_stdout_of_module(path):
    import io
    import contextlib

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        module = _load_module_from_path(path)
    return module, buf.getvalue()


@pytest.fixture(scope="module")
def module_path():
    return os.path.join(os.path.dirname(__file__), FILE_NAME)


def test_printed_list_matches_expected(module_path):
    _, out = _capture_stdout_of_module(module_path)
    expected = "['Y', 'no', 'Y', 'maybe', 'Y']"
    actual = out.strip()
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_answers_variable_is_correct_list(module_path):
    module, _ = _capture_stdout_of_module(module_path)
    expected = ['Y', 'no', 'Y', 'maybe', 'Y']
    actual = getattr(module, "answers", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_no_new_list_named_answers_created_via_literal_reassignment(module_path):
    # Ensure transformation isn't done by simply replacing the initial list literal with the final list.
    with open(module_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    assignments = [n for n in tree.body if isinstance(n, ast.Assign)]
    assert assignments, f"expected={'at least one assignment'} actual={'none'}"

    first = assignments[0]
    assert any(isinstance(t, ast.Name) and t.id == "answers" for t in first.targets), (
        f"expected={'answers assignment'} actual={'different assignment'}"
    )
    assert isinstance(first.value, ast.List), f"expected={'list literal'} actual={type(first.value).__name__}"

    initial_elts = []
    for e in first.value.elts:
        if isinstance(e, ast.Constant) and isinstance(e.value, str):
            initial_elts.append(e.value)
        else:
            initial_elts.append(None)

    expected_initial = ["Yes", "no", "YES", "maybe", "yes"]
    assert initial_elts == expected_initial, f"expected={expected_initial!r} actual={initial_elts!r}"