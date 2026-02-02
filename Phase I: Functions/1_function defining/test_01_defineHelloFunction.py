import importlib.util
import os
import sys


def load_module():
    filename = "01_defineHelloFunction.py"
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("assignment_01_defineHelloFunction", path)
    module = importlib.util.module_from_spec(spec)
    return spec, module, path


def test_stdout_exact(capsys):
    spec, module, _ = load_module()
    spec.loader.exec_module(module)
    out = capsys.readouterr().out
    expected = "Hello!\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_say_hello_exists_and_returns_expected(capsys):
    spec, module, _ = load_module()
    spec.loader.exec_module(module)
    _ = capsys.readouterr()
    assert hasattr(module, "say_hello")
    actual = module.say_hello()
    expected = "Hello!"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_result_variable_matches_expected(capsys):
    spec, module, _ = load_module()
    spec.loader.exec_module(module)
    _ = capsys.readouterr()
    assert hasattr(module, "result")
    actual = module.result
    expected = "Hello!"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"