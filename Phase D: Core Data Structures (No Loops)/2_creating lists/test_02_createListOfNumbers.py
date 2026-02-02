import ast
import importlib.util
import io
import os
import re
import sys
from contextlib import redirect_stdout

FILE_NAME = "02_createListOfNumbers.py"


def _load_module(path):
    name = "mod_02_createListOfNumbers"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)
    return module, buf.getvalue()


def test_numbers_defined_as_list_literal():
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)

    assign_nodes = [
        n for n in tree.body
        if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "numbers" for t in n.targets)
    ]
    assert assign_nodes, "expected: assignment to numbers; actual: not found"

    node = assign_nodes[0].value
    assert isinstance(node, ast.List), f"expected: list literal; actual: {type(node).__name__}"
    assert len(node.elts) == 4, f"expected: 4 elements; actual: {len(node.elts)}"
    assert all(isinstance(e, ast.Constant) and isinstance(e.value, int) for e in node.elts), \
        "expected: int constants; actual: non-int element present"


def test_numbers_runtime_value_and_print_output():
    module, out = _load_module(os.path.join(os.getcwd(), FILE_NAME))

    assert hasattr(module, "numbers"), "expected: module has numbers; actual: missing"
    nums = getattr(module, "numbers")
    assert isinstance(nums, list), f"expected: list; actual: {type(nums).__name__}"

    expected = [10, 20, 30, 40]
    assert nums == expected, f"expected: {expected}; actual: {nums}"

    m = re.search(r"\[[^\]]*\]", out)
    assert m is not None, f"expected: printed list; actual: {out!r}"

    try:
        printed_val = ast.literal_eval(m.group(0))
    except Exception as e:
        assert False, f"expected: parseable list; actual: {m.group(0)!r}"

    assert printed_val == expected, f"expected: {expected}; actual: {printed_val}"