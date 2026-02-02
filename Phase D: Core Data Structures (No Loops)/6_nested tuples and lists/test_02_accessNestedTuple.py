import importlib.util
import io
import os
import sys


def load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_output_prints_alice(capsys):
    path = os.path.join(os.path.dirname(__file__), "02_accessNestedTuple.py")
    module_name = "mod_02_accessNestedTuple_output"
    load_module_from_path(module_name, path)
    captured = capsys.readouterr()
    expected = "alice\n"
    actual = captured.out
    assert expected == actual, f"expected={expected!r} actual={actual!r}"


def test_name_variable_is_alice():
    path = os.path.join(os.path.dirname(__file__), "02_accessNestedTuple.py")
    module_name = "mod_02_accessNestedTuple_name"
    saved_stdout = sys.stdout
    try:
        sys.stdout = io.StringIO()
        mod = load_module_from_path(module_name, path)
    finally:
        sys.stdout = saved_stdout

    expected = "alice"
    actual = getattr(mod, "name", None)
    assert expected == actual, f"expected={expected!r} actual={actual!r}"


def test_users_is_unchanged():
    path = os.path.join(os.path.dirname(__file__), "02_accessNestedTuple.py")
    module_name = "mod_02_accessNestedTuple_users"
    saved_stdout = sys.stdout
    try:
        sys.stdout = io.StringIO()
        mod = load_module_from_path(module_name, path)
    finally:
        sys.stdout = saved_stdout

    expected = ("root", ("bob", "carol"), ("dave", "alice"))
    actual = getattr(mod, "users", None)
    assert expected == actual, f"expected={expected!r} actual={actual!r}"