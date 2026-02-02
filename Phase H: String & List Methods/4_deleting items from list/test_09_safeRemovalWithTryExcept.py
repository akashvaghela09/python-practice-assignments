import importlib.util
import pathlib
import sys


def load_module():
    path = pathlib.Path(__file__).resolve().parent / "09_safeRemovalWithTryExcept.py"
    spec = importlib.util.spec_from_file_location("safeRemovalWithTryExcept_09", str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_import_does_not_crash():
    load_module()


def test_fruits_list_after_execution_is_correct(capsys):
    module = load_module()
    expected = ["apple", "banana", "mango"]
    actual = getattr(module, "fruits", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_printed_output_matches_expected(capsys):
    load_module()
    captured = capsys.readouterr()
    expected = "fruits: ['apple', 'banana', 'mango']\n"
    actual = captured.out
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_no_unexpected_stderr(capsys):
    load_module()
    captured = capsys.readouterr()
    expected = ""
    actual = captured.err
    assert actual == expected, f"expected={expected!r} actual={actual!r}"