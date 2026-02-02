import importlib.util
import pathlib
import sys
import types

import pytest


def _load_module_without_running_print(module_name, file_path):
    source = pathlib.Path(file_path).read_text(encoding="utf-8")
    lines = source.splitlines(True)
    filtered = []
    for line in lines:
        if line.lstrip().startswith("print("):
            continue
        filtered.append(line)
    code = "".join(filtered)

    module = types.ModuleType(module_name)
    module.__file__ = str(file_path)
    exec(compile(code, str(file_path), "exec"), module.__dict__)
    sys.modules[module_name] = module
    return module


@pytest.fixture(scope="module")
def mod():
    return _load_module_without_running_print(
        "m01_callGreetFromMain", pathlib.Path(__file__).with_name("01_callGreetFromMain.py")
    )


def test_greet_exists_and_callable(mod):
    assert hasattr(mod, "greet")
    assert callable(mod.greet)


def test_main_exists_and_callable(mod):
    assert hasattr(mod, "main")
    assert callable(mod.main)


def test_greet_returns_hello(mod):
    expected = "Hello"
    actual = mod.greet()
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_main_returns_greet_value(mod):
    expected = "Hello"
    actual = mod.main()
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_main_matches_greet(mod):
    expected = mod.greet()
    actual = mod.main()
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_running_script_prints_hello(capsys):
    module_path = pathlib.Path(__file__).with_name("01_callGreetFromMain.py")
    spec = importlib.util.spec_from_file_location("run_01_callGreetFromMain", str(module_path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    out = capsys.readouterr().out
    expected = "Hello\n"
    actual = out
    assert actual == expected, f"expected={expected!r} actual={actual!r}"