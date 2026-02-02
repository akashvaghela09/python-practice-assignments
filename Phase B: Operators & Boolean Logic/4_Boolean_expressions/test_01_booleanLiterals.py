import importlib.util
import pathlib
import re


def _load_source():
    path = pathlib.Path(__file__).resolve().parent / "01_booleanLiterals.py"
    return path.read_text(encoding="utf-8")


def test_no_placeholders_left():
    src = _load_source()
    assert "???" not in src, "expected vs actual: placeholder removed vs found"


def test_only_three_prints_present():
    src = _load_source()
    prints = re.findall(r'^\s*print\s*\(', src, flags=re.MULTILINE)
    assert len(prints) == 3, f"expected vs actual: 3 vs {len(prints)}"


def test_running_file_prints_expected(capsys):
    path = pathlib.Path(__file__).resolve().parent / "01_booleanLiterals.py"
    spec = importlib.util.spec_from_file_location("boolean_literals_01", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    out = capsys.readouterr().out
    expected = "True\nFalse\nTrue\n"
    assert out == expected, f"expected vs actual: {expected!r} vs {out!r}"