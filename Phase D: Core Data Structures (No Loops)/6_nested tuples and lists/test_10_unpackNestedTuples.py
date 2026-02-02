import importlib.util
import sys
from pathlib import Path


def load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    loader = spec.loader
    assert loader is not None
    loader.exec_module(module)
    return module


def test_stdout_exact(capsys):
    file_path = Path(__file__).resolve().parent / "10_unpackNestedTuples.py"
    module_name = "unpack_nested_tuples_10"
    if module_name in sys.modules:
        del sys.modules[module_name]

    load_module(module_name, file_path)
    out = capsys.readouterr().out
    expected = "Jane 34 NY\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_variables_set_correctly(capsys):
    file_path = Path(__file__).resolve().parent / "10_unpackNestedTuples.py"
    module_name = "unpack_nested_tuples_10_vars"
    if module_name in sys.modules:
        del sys.modules[module_name]

    mod = load_module(module_name, file_path)
    capsys.readouterr()

    actual = (getattr(mod, "name", object()), getattr(mod, "age", object()), getattr(mod, "state", object()))
    expected = ("Jane", 34, "NY")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_record_unchanged(capsys):
    file_path = Path(__file__).resolve().parent / "10_unpackNestedTuples.py"
    module_name = "unpack_nested_tuples_10_record"
    if module_name in sys.modules:
        del sys.modules[module_name]

    mod = load_module(module_name, file_path)
    capsys.readouterr()

    actual = getattr(mod, "record", None)
    expected = ("Jane", (34, "NY"))
    assert actual == expected, f"expected={expected!r} actual={actual!r}"