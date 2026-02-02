import importlib
import ast
import io
import os
import sys
import contextlib

MODULE_NAME = "07_replaceWithConditionInPlace"


def _load_module():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    return importlib.import_module(MODULE_NAME)


def _run_module_capture_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = _load_module()
    return mod, buf.getvalue()


def test_stdout_prints_expected_list():
    mod, out = _run_module_capture_stdout()
    expected = str([88, 0, 73, 0, 60])
    actual = out.strip().splitlines()[-1] if out.strip() else ""
    assert expected == actual, f"expected={expected!r} actual={actual!r}"


def test_scores_list_modified_in_place_values():
    mod, _ = _run_module_capture_stdout()
    expected = [88, 0, 73, 0, 60]
    actual = getattr(mod, "scores", None)
    assert expected == actual, f"expected={expected!r} actual={actual!r}"


def test_scores_mutation_occurs_via_index_assignment_not_rebind():
    module = _load_module()
    file_path = getattr(module, "__file__", None)
    assert file_path and os.path.exists(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)

    assigned_to_scores = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                assigned_to_scores.append(tgt)
        elif isinstance(node, ast.AnnAssign):
            assigned_to_scores.append(node.target)

    has_subscript_assignment = any(
        isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == "scores"
        for t in assigned_to_scores
    )
    has_rebind_after_init = False
    init_seen = False
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "scores" for t in node.targets):
            if not init_seen:
                init_seen = True
            else:
                has_rebind_after_init = True
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "scores":
            if not init_seen:
                init_seen = True
            else:
                has_rebind_after_init = True

    expected_subscript = True
    actual_subscript = has_subscript_assignment
    assert expected_subscript == actual_subscript, f"expected={expected_subscript!r} actual={actual_subscript!r}"

    expected_rebind = False
    actual_rebind = has_rebind_after_init
    assert expected_rebind == actual_rebind, f"expected={expected_rebind!r} actual={actual_rebind!r}"


def test_rule_applied_only_below_60():
    mod, _ = _run_module_capture_stdout()
    scores = mod.scores
    expected = [True, True, True, True, True]
    actual = [
        scores[0] == 88,
        scores[1] == 0,
        scores[2] == 73,
        scores[3] == 0,
        scores[4] == 60,
    ]
    assert expected == actual, f"expected={expected!r} actual={actual!r}"