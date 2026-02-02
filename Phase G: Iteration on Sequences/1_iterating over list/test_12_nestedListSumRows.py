import ast
import importlib.util
import pathlib
import sys


def _load_module(mod_name, file_path):
    spec = importlib.util.spec_from_file_location(mod_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


def test_prints_expected_row_sums(capsys):
    import importlib
    import 12_nestedListSumRows as m  # noqa: E999,F401


def test_runtime_output_matches_expected(capsys):
    file_path = pathlib.Path(__file__).with_name("12_nestedListSumRows.py")
    mod_name = "mod12_nestedListSumRows_runtime"
    _load_module(mod_name, file_path)
    out = capsys.readouterr().out.strip()
    expected = str([6, 9, 6])
    assert out == expected, f"expected={expected} actual={out}"


def test_row_sums_variable_is_correct_when_present():
    file_path = pathlib.Path(__file__).with_name("12_nestedListSumRows.py")
    mod_name = "mod12_nestedListSumRows_vars"
    m = _load_module(mod_name, file_path)
    if hasattr(m, "row_sums"):
        actual = m.row_sums
        expected = [6, 9, 6]
        assert actual == expected, f"expected={expected} actual={actual}"


def test_no_blanks_left_in_source():
    file_path = pathlib.Path(__file__).with_name("12_nestedListSumRows.py")
    src = file_path.read_text(encoding="utf-8")
    assert "____" not in src, f"expected={'no blanks'} actual={'blanks found'}"


def test_source_is_valid_python():
    file_path = pathlib.Path(__file__).with_name("12_nestedListSumRows.py")
    src = file_path.read_text(encoding="utf-8")
    try:
        ast.parse(src)
        ok = True
    except SyntaxError:
        ok = False
    assert ok, f"expected={'valid'} actual={'invalid'}"