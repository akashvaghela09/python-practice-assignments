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


def test_access_granted_default():
    assignment_path = Path(__file__).resolve().parent / "04_loginCheck.py"
    out = _run_module(assignment_path)
    expected = "ACCESS GRANTED\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_access_denied_wrong_password_no_token():
    assignment_path = Path(__file__).resolve().parent / "04_loginCheck.py"
    out = _exec_with_overrides(
        assignment_path,
        {"username": "sam", "password": "wrong", "expected_password": "secret", "has_reset_token": False},
    )
    expected = "ACCESS DENIED\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_access_granted_with_token_even_if_wrong_password():
    assignment_path = Path(__file__).resolve().parent / "04_loginCheck.py"
    out = _exec_with_overrides(
        assignment_path,
        {"username": "sam", "password": "wrong", "expected_password": "secret", "has_reset_token": True},
    )
    expected = "ACCESS GRANTED\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_access_denied_empty_username_even_if_password_ok():
    assignment_path = Path(__file__).resolve().parent / "04_loginCheck.py"
    out = _exec_with_overrides(
        assignment_path,
        {"username": "", "password": "secret", "expected_password": "secret", "has_reset_token": True},
    )
    expected = "ACCESS DENIED\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"
