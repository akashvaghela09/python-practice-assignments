import importlib.util
import os
import sys
import ast
import pytest


def _load_module():
    fname = "10_implementStableSortByKey.py"
    path = os.path.join(os.path.dirname(__file__), fname)
    spec = importlib.util.spec_from_file_location("assignment10", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _expected_sorted(items, key_func):
    return sorted(list(items), key=key_func)


def _is_stable_sorted(original, result, key_func):
    if len(original) != len(result):
        return False

    # same multiset of object identities
    orig_ids = [id(x) for x in original]
    res_ids = [id(x) for x in result]
    if sorted(orig_ids) != sorted(res_ids):
        return False

    # keys non-decreasing
    keys = [key_func(x) for x in result]
    if any(keys[i] > keys[i + 1] for i in range(len(keys) - 1)):
        return False

    # stability: within each key, relative order of ids preserved
    from collections import defaultdict

    orig_groups = defaultdict(list)
    res_groups = defaultdict(list)
    for x in original:
        orig_groups[key_func(x)].append(id(x))
    for x in result:
        res_groups[key_func(x)].append(id(x))

    if set(orig_groups.keys()) != set(res_groups.keys()):
        return False

    for k in orig_groups:
        if orig_groups[k] != res_groups[k]:
            return False

    return True


def _get_source():
    fname = "10_implementStableSortByKey.py"
    path = os.path.join(os.path.dirname(__file__), fname)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_no_builtin_sort_used_in_function():
    src = _get_source()
    tree = ast.parse(src)
    func_node = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "stable_sort_by_key":
            func_node = node
            break
    assert func_node is not None

    forbidden = []

    for node in ast.walk(func_node):
        if isinstance(node, ast.Call):
            # sorted(...)
            if isinstance(node.func, ast.Name) and node.func.id == "sorted":
                forbidden.append("sorted")
            # list.sort() or something.sort()
            if isinstance(node.func, ast.Attribute) and node.func.attr == "sort":
                forbidden.append(".sort")

    assert not forbidden, f"expected forbidden sort usage absent, actual found: {forbidden}"


def test_returns_new_list_and_does_not_mutate_input_simple():
    mod = _load_module()
    f = mod.stable_sort_by_key
    items = [("Ava", 3), ("Ben", 2), ("Cara", 3), ("Dan", 2)]
    orig = list(items)
    res = f(items, lambda x: x[1])

    assert items == orig, f"expected input unchanged {orig}, actual {items}"
    assert res is not items, f"expected new list object, actual same object"
    assert res == _expected_sorted(items, lambda x: x[1]), f"expected {_expected_sorted(items, lambda x: x[1])}, actual {res}"
    assert _is_stable_sorted(items, res, lambda x: x[1]), f"expected stable sorted, actual {res}"


def test_stability_with_duplicate_keys_objects():
    mod = _load_module()
    f = mod.stable_sort_by_key

    class Obj:
        def __init__(self, name, k):
            self.name = name
            self.k = k

        def __repr__(self):
            return f"Obj({self.name},{self.k})"

    a1 = Obj("a1", 2)
    a2 = Obj("a2", 1)
    a3 = Obj("a3", 2)
    a4 = Obj("a4", 1)
    a5 = Obj("a5", 2)
    items = [a1, a2, a3, a4, a5]
    orig = list(items)

    res = f(items, lambda o: o.k)

    assert items == orig, f"expected input unchanged {orig}, actual {items}"
    assert res is not items, f"expected new list object, actual same object"
    assert _is_stable_sorted(items, res, lambda o: o.k), f"expected stable sorted, actual {res}"

    expected = _expected_sorted(items, lambda o: o.k)
    assert [id(x) for x in res] == [id(x) for x in expected], f"expected {[id(x) for x in expected]}, actual {[id(x) for x in res]}"


def test_handles_empty_and_singleton():
    mod = _load_module()
    f = mod.stable_sort_by_key

    items = []
    res = f(items, lambda x: x)
    assert items == [], f"expected [], actual {items}"
    assert res == [], f"expected [], actual {res}"
    assert res is not items, f"expected new list object, actual same object"

    items2 = [("x", 1)]
    orig2 = list(items2)
    res2 = f(items2, lambda x: x[1])
    assert items2 == orig2, f"expected {orig2}, actual {items2}"
    assert res2 == items2, f"expected {items2}, actual {res2}"
    assert res2 is not items2, f"expected new list object, actual same object"


def test_sorted_pairs_variable_matches_expected_when_present():
    mod = _load_module()
    assert hasattr(mod, "pairs"), f"expected module to have pairs, actual missing"
    assert hasattr(mod, "sorted_pairs"), f"expected module to have sorted_pairs, actual missing"
    expected = _expected_sorted(mod.pairs, lambda x: x[1])
    assert mod.sorted_pairs == expected, f"expected {expected}, actual {mod.sorted_pairs}"


def test_does_not_depend_on_global_pairs():
    mod = _load_module()
    f = mod.stable_sort_by_key

    items = [("z", 5), ("a", 1), ("b", 1), ("y", 2)]
    res = f(items, lambda x: x[1])

    expected = _expected_sorted(items, lambda x: x[1])
    assert res == expected, f"expected {expected}, actual {res}"
    assert _is_stable_sorted(items, res, lambda x: x[1]), f"expected stable sorted, actual {res}"