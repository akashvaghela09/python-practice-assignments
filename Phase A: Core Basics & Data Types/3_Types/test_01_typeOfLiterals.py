import importlib.util
import pathlib
import sys


def _run_module_capture_output(module_name, file_path, capsys):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    out = capsys.readouterr().out
    return module, out


def test_prints_expected_types_in_order(capsys):
    file_path = pathlib.Path(__file__).with_name("01_typeOfLiterals.py")
    module, out = _run_module_capture_output("module_01_typeOfLiterals_run1", file_path, capsys)
    lines = [line.rstrip("\n") for line in out.splitlines()]
    assert lines == [
        "<class 'int'>",
        "<class 'float'>",
        "<class 'str'>",
        "<class 'bool'>",
    ], f"expected={[\"<class 'int'>\",\"<class 'float'>\",\"<class 'str'>\",\"<class 'bool'>\"]} actual={lines}"


def test_variables_exist_and_match_printed_types(capsys):
    file_path = pathlib.Path(__file__).with_name("01_typeOfLiterals.py")
    module, out = _run_module_capture_output("module_01_typeOfLiterals_run2", file_path, capsys)
    for name in ("a", "b", "c", "d"):
        assert hasattr(module, name), f"expected={'hasattr(module, '+name+')'} actual={hasattr(module, name)}"

    printed = [line.strip() for line in out.splitlines()]
    actual_types = [str(type(getattr(module, n))) for n in ("a", "b", "c", "d")]
    assert printed == actual_types, f"expected={printed} actual={actual_types}"


def test_bool_is_not_int(capsys):
    file_path = pathlib.Path(__file__).with_name("01_typeOfLiterals.py")
    module, _ = _run_module_capture_output("module_01_typeOfLiterals_run3", file_path, capsys)
    assert type(module.d) is bool, f"expected={bool} actual={type(module.d)}"
    assert type(module.a) is not bool, f"expected={'not bool'} actual={type(module.a)}"