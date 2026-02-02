import sys
import importlib.util
from pathlib import Path

def _run_module(path: Path):
    if not path.exists():
        raise AssertionError(f"Assignment file does not exist: {path}")

    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)

    old_stdout = sys.stdout
    try:
        from io import StringIO
        buf = StringIO()
        sys.stdout = buf
        spec.loader.exec_module(module)  # type: ignore
        return buf.getvalue()
    finally:
        sys.stdout = old_stdout


def _exec_with_overrides(path: Path, overrides: dict):
    if not path.exists():
        raise AssertionError(f"Assignment file does not exist: {path}")

    code = path.read_text(encoding="utf-8")
    glb = {"__name__": "__main__"}
    glb.update(overrides)

    old_stdout = sys.stdout
    try:
        from io import StringIO
        buf = StringIO()
        sys.stdout = buf
        exec(compile(code, str(path), "exec"), glb)
        return buf.getvalue()
    finally:
        sys.stdout = old_stdout


def test_discount_default_student_young():
    assignment_path = Path(__file__).resolve().parent / "03_combinedAndOr.py"
    out = _run_module(assignment_path)
    expected = "DISCOUNT\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_no_discount_when_student_old_not_veteran():
    assignment_path = Path(__file__).resolve().parent / "03_combinedAndOr.py"
    out = _exec_with_overrides(assignment_path, {"is_student": True, "age": 30, "is_veteran": False})
    expected = "NO DISCOUNT\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_discount_when_veteran_even_if_not_student():
    assignment_path = Path(__file__).resolve().parent / "03_combinedAndOr.py"
    out = _exec_with_overrides(assignment_path, {"is_student": False, "age": 40, "is_veteran": True})
    expected = "DISCOUNT\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"
