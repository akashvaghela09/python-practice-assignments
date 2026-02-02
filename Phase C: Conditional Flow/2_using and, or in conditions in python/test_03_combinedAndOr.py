import importlib.util
import pathlib
import sys
import types
import pytest


MODULE_FILENAME = "03_combinedAndOr.py"


def _load_module_from_path(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_file_exists_and_has_no_placeholder_underscores():
    path = pathlib.Path(__file__).resolve().parent / MODULE_FILENAME
    assert path.exists(), f"expected={MODULE_FILENAME!r} actual={'missing'!r}"
    content = path.read_text(encoding="utf-8")
    assert "____" not in content, f"expected={'no_placeholder'!r} actual={'placeholder_found'!r}"


def test_prints_discount_for_student_age20_not_veteran(capsys):
    path = pathlib.Path(__file__).resolve().parent / MODULE_FILENAME
    module_name = "student_discount_case1"
    _load_module_from_path(path, module_name)
    out = capsys.readouterr().out.strip()
    expected = "DISCOUNT"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_prints_no_discount_when_age_changed_to_30_student_true_not_veteran(monkeypatch, capsys):
    path = pathlib.Path(__file__).resolve().parent / MODULE_FILENAME
    code = path.read_text(encoding="utf-8")

    ns = {"__name__": "__main__", "__file__": str(path)}
    ns["is_student"] = True
    ns["age"] = 30
    ns["is_veteran"] = False

    exec(compile(code, str(path), "exec"), ns, ns)
    out = capsys.readouterr().out.strip()
    expected = "NO DISCOUNT"
    assert out == expected, f"expected={expected!r} actual={out!r}"


@pytest.mark.parametrize(
    "is_student,age,is_veteran,expected",
    [
        (True, 25, False, "DISCOUNT"),
        (True, 26, False, "NO DISCOUNT"),
        (False, 20, True, "DISCOUNT"),
        (False, 30, False, "NO DISCOUNT"),
        (True, 30, True, "DISCOUNT"),
    ],
)
def test_logic_matrix_via_exec(is_student, age, is_veteran, expected, capsys):
    path = pathlib.Path(__file__).resolve().parent / MODULE_FILENAME
    code = path.read_text(encoding="utf-8")

    ns = {"__name__": "__main__", "__file__": str(path)}
    ns["is_student"] = is_student
    ns["age"] = age
    ns["is_veteran"] = is_veteran

    exec(compile(code, str(path), "exec"), ns, ns)
    out = capsys.readouterr().out.strip()
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_output_is_exact_single_line(capsys):
    path = pathlib.Path(__file__).resolve().parent / MODULE_FILENAME
    module_name = "student_discount_output_format"
    _load_module_from_path(path, module_name)
    raw = capsys.readouterr().out
    stripped_lines = [ln for ln in raw.splitlines() if ln.strip() != ""]
    assert len(stripped_lines) == 1, f"expected={1!r} actual={len(stripped_lines)!r}"
    assert stripped_lines[0] in ("DISCOUNT", "NO DISCOUNT"), f"expected={'valid_message'!r} actual={stripped_lines[0]!r}"