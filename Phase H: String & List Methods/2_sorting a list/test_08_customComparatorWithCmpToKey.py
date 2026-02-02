import importlib
import ast
import inspect
import pathlib
import sys


MODULE_NAME = "08_customComparatorWithCmpToKey"


def load_module():
    if MODULE_NAME in sys.modules:
        return importlib.reload(sys.modules[MODULE_NAME])
    return importlib.import_module(MODULE_NAME)


def test_versions_sorted_value():
    m = load_module()
    assert hasattr(m, "versions_sorted"), "versions_sorted missing"
    expected = ["1.2", "1.9", "1.10", "2.0"]
    actual = m.versions_sorted
    assert actual == expected, f"expected={expected} actual={actual}"


def test_versions_not_mutated():
    m = load_module()
    assert hasattr(m, "versions"), "versions missing"
    expected = ["1.9", "1.10", "1.2", "2.0"]
    actual = m.versions
    assert actual == expected, f"expected={expected} actual={actual}"


def test_compare_versions_contract_and_numeric_order():
    m = load_module()
    assert callable(getattr(m, "compare_versions", None)), "compare_versions missing"

    cv = m.compare_versions

    def sign(x):
        return (x > 0) - (x < 0)

    pairs = [
        ("1.2", "1.9", -1),
        ("1.9", "1.10", -1),
        ("1.10", "2.0", -1),
        ("1.10", "1.2", 1),
        ("1.9", "1.2", 1),
        ("2.0", "1.10", 1),
        ("1.2", "1.2", 0),
        ("2.0", "2.0", 0),
    ]
    for a, b, exp in pairs:
        res = cv(a, b)
        assert isinstance(res, int), f"expected={int} actual={type(res)}"
        assert sign(res) == exp, f"expected={exp} actual={sign(res)}"
        inv = cv(b, a)
        assert sign(inv) == -exp, f"expected={-exp} actual={sign(inv)}"


def test_compare_versions_returns_only_minus1_0_1():
    m = load_module()
    cv = m.compare_versions
    vals = [
        cv("1.2", "1.9"),
        cv("1.9", "1.2"),
        cv("1.10", "1.10"),
        cv("2.0", "1.10"),
    ]
    actual_set = set(vals)
    expected_subset = {-1, 0, 1}
    assert actual_set.issubset(expected_subset), f"expected={expected_subset} actual={actual_set}"


def test_uses_cmp_to_key_in_source_and_sorted_call():
    mod = load_module()
    file_path = pathlib.Path(inspect.getsourcefile(mod))
    src = file_path.read_text(encoding="utf-8")
    assert "cmp_to_key" in src, f"expected={'cmp_to_key'} actual={src.find('cmp_to_key')}"
    tree = ast.parse(src)

    # Ensure versions_sorted is assigned via sorted(..., key=cmp_to_key(compare_versions)) pattern
    assign_nodes = [
        n for n in tree.body
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "versions_sorted" for t in n.targets)
    ]
    assert len(assign_nodes) == 1, f"expected={1} actual={len(assign_nodes)}"
    node = assign_nodes[0].value
    assert isinstance(node, ast.Call), f"expected={ast.Call} actual={type(node)}"
    func = node.func
    assert isinstance(func, ast.Name) and func.id == "sorted", f"expected={'sorted'} actual={getattr(func, 'id', None)}"

    key_kw = None
    for kw in node.keywords:
        if kw.arg == "key":
            key_kw = kw.value
            break
    assert key_kw is not None, f"expected={'key keyword'} actual={None}"

    # key should be cmp_to_key(compare_versions) call
    assert isinstance(key_kw, ast.Call), f"expected={ast.Call} actual={type(key_kw)}"
    assert isinstance(key_kw.func, ast.Name) and key_kw.func.id == "cmp_to_key", f"expected={'cmp_to_key'} actual={getattr(key_kw.func, 'id', None)}"
    assert len(key_kw.args) == 1, f"expected={1} actual={len(key_kw.args)}"
    arg0 = key_kw.args[0]
    assert isinstance(arg0, ast.Name) and arg0.id == "compare_versions", f"expected={'compare_versions'} actual={getattr(arg0, 'id', None)}"