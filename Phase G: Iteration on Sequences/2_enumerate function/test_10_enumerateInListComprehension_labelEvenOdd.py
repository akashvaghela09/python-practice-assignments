import ast
import importlib.util
import io
import os
import re
import sys
import types
import pytest

MODULE_FILENAME = "10_enumerateInListComprehension_labelEvenOdd.py"
MODULE_NAME = "m10_enumerateInListComprehension_labelEvenOdd"


def _load_module():
    spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_FILENAME)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_module_capture_stdout():
    spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_FILENAME)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old
    return module, buf.getvalue()


def _expected_labels():
    nums = [10, 11, 12, 13]
    return [f"{i}: {'even' if i % 2 == 0 else 'odd'}" for i, _ in enumerate(nums)]


def test_module_runs_and_defines_labels():
    try:
        module = _load_module()
    except SyntaxError as e:
        pytest.fail(f"expected=module executes actual=SyntaxError({e})")
    except Exception as e:
        pytest.fail(f"expected=module executes actual={type(e).__name__}({e})")

    assert hasattr(module, "labels"), f"expected=module has labels actual={dir(module)}"
    assert isinstance(module.labels, list), f"expected=list actual={type(module.labels).__name__}"


def test_labels_correct_value_and_format():
    module = _load_module()
    expected = _expected_labels()
    actual = getattr(module, "labels", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"

    for item in actual:
        assert isinstance(item, str), f"expected=str actual={type(item).__name__}"
        assert re.fullmatch(r"\d+: (even|odd)", item) is not None, f"expected=pattern_match actual={item!r}"


def test_labels_length_matches_nums():
    module = _load_module()
    assert hasattr(module, "nums"), f"expected=module has nums actual={dir(module)}"
    assert len(module.labels) == len(module.nums), f"expected={len(module.nums)} actual={len(module.labels)}"


def test_uses_enumerate_in_list_comprehension():
    with open(MODULE_FILENAME, "r", encoding="utf-8") as f:
        src = f.read()

    try:
        tree = ast.parse(src, filename=MODULE_FILENAME)
    except SyntaxError as e:
        pytest.fail(f"expected=parseable_source actual=SyntaxError({e})")

    found_assignment = False
    found_listcomp = False
    found_enumerate = False

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "labels":
                    found_assignment = True
                    if isinstance(node.value, ast.ListComp):
                        found_listcomp = True
                        for sub in ast.walk(node.value):
                            if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id == "enumerate":
                                found_enumerate = True

    assert found_assignment, "expected=labels assignment actual=not_found"
    assert found_listcomp, "expected=list comprehension actual=not_listcomp"
    assert found_enumerate, "expected=enumerate_used actual=not_used"


def test_stdout_prints_labels_list():
    module, out = _run_module_capture_stdout()
    expected = repr(_expected_labels())
    actual = out.strip().splitlines()[-1] if out.strip().splitlines() else ""
    assert actual == expected, f"expected={expected!r} actual={actual!r}"