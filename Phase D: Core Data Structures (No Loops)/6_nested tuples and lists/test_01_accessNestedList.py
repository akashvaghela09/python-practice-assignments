import importlib.util
import os
import sys


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prints_42(capsys):
    path = os.path.join(os.path.dirname(__file__), "01_accessNestedList.py")
    module_name = "assignment_01_accessNestedList"
    if module_name in sys.modules:
        del sys.modules[module_name]

    _load_module(path, module_name)
    captured = capsys.readouterr()
    expected = "42\n"
    actual = captured.out
    assert expected == actual, f"expected={expected!r} actual={actual!r}"


def test_value_is_42():
    path = os.path.join(os.path.dirname(__file__), "01_accessNestedList.py")
    module_name = "assignment_01_accessNestedList_value"
    if module_name in sys.modules:
        del sys.modules[module_name]

    mod = _load_module(path, module_name)
    expected = 42
    actual = getattr(mod, "value", None)
    assert expected == actual, f"expected={expected!r} actual={actual!r}"


def test_value_comes_from_nested_indexing():
    path = os.path.join(os.path.dirname(__file__), "01_accessNestedList.py")
    module_name = "assignment_01_accessNestedList_nested"
    if module_name in sys.modules:
        del sys.modules[module_name]

    mod = _load_module(path, module_name)
    expected = mod.nested[1][2]
    actual = mod.value
    assert expected == actual, f"expected={expected!r} actual={actual!r}"