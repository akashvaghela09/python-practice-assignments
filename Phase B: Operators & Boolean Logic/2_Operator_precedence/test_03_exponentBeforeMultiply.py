import importlib.util
import pathlib
import re


def _load_module(path):
    spec = importlib.util.spec_from_file_location("student_mod", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_file_exists():
    path = pathlib.Path(__file__).resolve().parent / "03_exponentBeforeMultiply.py"
    assert path.exists()


def test_no_blanks_remaining():
    path = pathlib.Path(__file__).resolve().parent / "03_exponentBeforeMultiply.py"
    src = path.read_text(encoding="utf-8")
    assert "__" not in src


def test_prints_19_exactly(capsys):
    path = pathlib.Path(__file__).resolve().parent / "03_exponentBeforeMultiply.py"
    _load_module(path)
    out = capsys.readouterr().out
    assert out == "19\n", f"expected={repr('19\\n')} actual={repr(out)}"


def test_result_value_is_19(capsys):
    path = pathlib.Path(__file__).resolve().parent / "03_exponentBeforeMultiply.py"
    mod = _load_module(path)
    _ = capsys.readouterr()
    expected = 19
    actual = getattr(mod, "result", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"