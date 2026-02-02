import importlib.util
import sys
from pathlib import Path


def _load_module_capture_stdout(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_output_exact_lines(capsys):
    file_path = Path(__file__).resolve().parent / "03_stringComparisons.py"
    _load_module_capture_stdout("mod_03_stringComparisons", file_path)
    out = capsys.readouterr().out
    lines = [line.rstrip("\r") for line in out.splitlines()]
    expected = ["True", "False", "True"]
    assert lines == expected, f"expected={expected!r} actual={lines!r}"


def test_no_extra_whitespace_or_missing_newlines(capsys):
    file_path = Path(__file__).resolve().parent / "03_stringComparisons.py"
    _load_module_capture_stdout("mod_03_stringComparisons_ws", file_path)
    out = capsys.readouterr().out
    expected = "True\nFalse\nTrue\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_module_imports_without_syntax_error(capsys):
    file_path = Path(__file__).resolve().parent / "03_stringComparisons.py"
    try:
        _load_module_capture_stdout("mod_03_stringComparisons_import", file_path)
    except SyntaxError as e:
        assert False, f"expected={'no SyntaxError'} actual={type(e).__name__}"