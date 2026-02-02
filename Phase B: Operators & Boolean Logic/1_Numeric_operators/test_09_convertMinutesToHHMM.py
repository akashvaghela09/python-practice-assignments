import importlib.util
import pathlib
import re


def load_module():
    path = pathlib.Path(__file__).resolve().parent / "09_convertMinutesToHHMM.py"
    spec = importlib.util.spec_from_file_location("m09_convertMinutesToHHMM", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prints_exact_output(capsys):
    load_module()
    out = capsys.readouterr().out
    expected = "135 minutes = 2h 15m\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_hours_and_minutes_values():
    m = load_module()
    expected_hours = 2
    expected_minutes = 15
    assert m.hours == expected_hours, f"expected={expected_hours!r} actual={m.hours!r}"
    assert m.minutes == expected_minutes, f"expected={expected_minutes!r} actual={m.minutes!r}"


def test_uses_integer_math_operators():
    path = pathlib.Path(__file__).resolve().parent / "09_convertMinutesToHHMM.py"
    src = path.read_text(encoding="utf-8")
    src_no_comments = "\n".join([line.split("#", 1)[0] for line in src.splitlines()])
    has_floor_div = re.search(r"\bhours\s*=\s*total_minutes\s*//\s*60\b", src_no_comments) is not None
    has_mod = re.search(r"\bminutes\s*=\s*total_minutes\s*%\s*60\b", src_no_comments) is not None
    expected = (True, True)
    actual = (has_floor_div, has_mod)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"