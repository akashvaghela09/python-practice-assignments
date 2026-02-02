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


def test_limited_access_default_staff_2fa_off_network():
    assignment_path = Path(__file__).resolve().parent / "10_accessControlMatrix.py"
    out = _run_module(assignment_path)
    expected = "LIMITED ACCESS\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_full_access_when_on_network_staff_2fa():
    assignment_path = Path(__file__).resolve().parent / "10_accessControlMatrix.py"
    out = _exec_with_overrides(
        assignment_path,
        {"role": "staff", "has_2fa": True, "is_on_network": True, "has_invite": False, "is_suspended": False},
    )
    expected = "FULL ACCESS\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_no_access_when_suspended_even_if_admin():
    assignment_path = Path(__file__).resolve().parent / "10_accessControlMatrix.py"
    out = _exec_with_overrides(
        assignment_path,
        {"role": "admin", "has_2fa": False, "is_on_network": False, "has_invite": False, "is_suspended": True},
    )
    expected = "NO ACCESS\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_limited_access_guest_with_invite():
    assignment_path = Path(__file__).resolve().parent / "10_accessControlMatrix.py"
    out = _exec_with_overrides(
        assignment_path,
        {"role": "guest", "has_2fa": False, "is_on_network": False, "has_invite": True, "is_suspended": False},
    )
    expected = "LIMITED ACCESS\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_no_access_guest_no_invite():
    assignment_path = Path(__file__).resolve().parent / "10_accessControlMatrix.py"
    out = _exec_with_overrides(
        assignment_path,
        {"role": "guest", "has_2fa": False, "is_on_network": False, "has_invite": False, "is_suspended": False},
    )
    expected = "NO ACCESS\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"
