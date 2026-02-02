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


def test_valid_default_password():
    assignment_path = Path(__file__).resolve().parent / "08_passwordPolicy.py"
    out = _run_module(assignment_path)
    expected = "VALID\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_invalid_with_space():
    assignment_path = Path(__file__).resolve().parent / "08_passwordPolicy.py"
    out = _exec_with_overrides(assignment_path, {"password": "abcd e1fg"})
    expected = "INVALID\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_invalid_too_short_even_with_digit():
    assignment_path = Path(__file__).resolve().parent / "08_passwordPolicy.py"
    out = _exec_with_overrides(assignment_path, {"password": "ab1cdef"})
    expected = "INVALID\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_valid_with_special_no_digit():
    assignment_path = Path(__file__).resolve().parent / "08_passwordPolicy.py"
    out = _exec_with_overrides(assignment_path, {"password": "abcdefgh!"})
    expected = "VALID\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_invalid_without_digit_or_special():
    assignment_path = Path(__file__).resolve().parent / "08_passwordPolicy.py"
    out = _exec_with_overrides(assignment_path, {"password": "abcdefgh"})
    expected = "INVALID\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"
