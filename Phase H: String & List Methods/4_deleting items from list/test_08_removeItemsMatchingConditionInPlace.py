import importlib.util
import pathlib
import sys
import ast
import pytest


MODULE_NAME = "08_removeItemsMatchingConditionInPlace"


def load_module(tmp_path, monkeypatch):
    src = pathlib.Path(__file__).with_name(f"{MODULE_NAME}.py")
    dst = tmp_path / f"{MODULE_NAME}.py"
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    monkeypatch.syspath_prepend(str(tmp_path))

    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(dst))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = mod
    spec.loader.exec_module(mod)
    return mod, dst


def test_removes_negatives_in_place_and_preserves_order(tmp_path, monkeypatch, capsys):
    mod, _ = load_module(tmp_path, monkeypatch)

    original = getattr(mod, "nums", None)
    assert isinstance(original, list), f"expected={list} actual={type(original)}"

    before_id = id(original)
    before_copy = list(original)

    expected = [x for x in before_copy if x >= 0]

    # Must modify same list object
    assert id(mod.nums) == before_id, f"expected={before_id} actual={id(mod.nums)}"
    # Must remove all negatives
    assert all(x >= 0 for x in mod.nums), f"expected={True} actual={any(x < 0 for x in mod.nums)}"
    # Must match expected order/content
    assert mod.nums == expected, f"expected={expected} actual={mod.nums}"

    out = capsys.readouterr().out
    assert "nums:" in out, f"expected={'nums:'} actual={out}"


def test_does_not_use_list_reassignment_in_source(tmp_path, monkeypatch):
    _, src_path = load_module(tmp_path, monkeypatch)
    source = src_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    assigns_to_nums = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "nums":
                    assigns_to_nums.append(node)

    # Allow exactly one assignment: the initial definition
    expected_count = 1
    actual_count = len(assigns_to_nums)
    assert actual_count == expected_count, f"expected={expected_count} actual={actual_count}"


def test_does_not_build_new_list_via_listcomp_or_filter_assignment(tmp_path, monkeypatch):
    _, src_path = load_module(tmp_path, monkeypatch)
    source = src_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    bad = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "nums":
                    val = node.value
                    if isinstance(val, (ast.ListComp, ast.GeneratorExp, ast.Call, ast.BinOp)):
                        # if there were extra assignments, they would likely be rebuilding
                        bad = True

    expected = False
    actual = bad
    assert actual == expected, f"expected={expected} actual={actual}"