import ast
import importlib.util
import pathlib
import sys


def _load_module_from_path(path):
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return module


def test_no_placeholders_left_in_file():
    path = pathlib.Path(__file__).with_name("02_rangeWithStartStop.py")
    content = path.read_text(encoding="utf-8")
    assert "_____" not in content, "expected no placeholders, actual found placeholders"


def test_nums_list_correct():
    path = pathlib.Path(__file__).with_name("02_rangeWithStartStop.py")
    mod = _load_module_from_path(path)
    assert hasattr(mod, "nums"), "expected nums defined, actual missing"
    expected = [3, 4, 5, 6, 7]
    actual = mod.nums
    assert actual == expected, f"expected {expected}, actual {actual}"


def test_uses_range_and_list_with_two_args():
    path = pathlib.Path(__file__).with_name("02_rangeWithStartStop.py")
    tree = ast.parse(path.read_text(encoding="utf-8"))

    range_call = None
    list_call = None

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "list":
            if node.args and isinstance(node.args[0], ast.Call):
                inner = node.args[0]
                if isinstance(inner.func, ast.Name) and inner.func.id == "range":
                    list_call = node
                    range_call = inner
                    break

    assert range_call is not None, "expected use of list(range(...)), actual not found"
    assert len(range_call.args) == 2, f"expected {2}, actual {len(range_call.args)}"
    assert len(list_call.args) == 1, f"expected {1}, actual {len(list_call.args)}"
    assert not range_call.keywords, "expected no keywords, actual keywords found"