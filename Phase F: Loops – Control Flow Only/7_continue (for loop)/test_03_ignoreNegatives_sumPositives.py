import importlib.util
import pathlib
import sys


def _run_module_capture_stdout(module_name, file_path, capsys):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    out = capsys.readouterr().out
    return mod, out


def test_prints_expected_sum(capsys):
    file_path = pathlib.Path(__file__).with_name("03_ignoreNegatives_sumPositives.py")
    mod, out = _run_module_capture_stdout("a03_ignoreNegatives_sumPositives_run1", file_path, capsys)
    assert out.strip() == "11", f"expected={'11'} actual={out.strip()}"


def test_total_variable_matches_expected_after_execution(capsys):
    file_path = pathlib.Path(__file__).with_name("03_ignoreNegatives_sumPositives.py")
    mod, _ = _run_module_capture_stdout("a03_ignoreNegatives_sumPositives_run2", file_path, capsys)
    assert hasattr(mod, "total"), "expected=True actual=False"
    assert mod.total == 11, f"expected={11} actual={getattr(mod, 'total', None)}"


def test_numbers_list_unchanged(capsys):
    file_path = pathlib.Path(__file__).with_name("03_ignoreNegatives_sumPositives.py")
    mod, _ = _run_module_capture_stdout("a03_ignoreNegatives_sumPositives_run3", file_path, capsys)
    assert hasattr(mod, "numbers"), "expected=True actual=False"
    assert mod.numbers == [3, -1, 4, -2, 0, 6, -9], f"expected={[3, -1, 4, -2, 0, 6, -9]} actual={getattr(mod, 'numbers', None)}"