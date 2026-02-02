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


def test_free_default_premium():
    assignment_path = Path(__file__).resolve().parent / "05_shippingRules.py"
    out = _run_module(assignment_path)
    expected = "FREE\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_standard_when_not_premium_and_below_threshold():
    assignment_path = Path(__file__).resolve().parent / "05_shippingRules.py"
    out = _exec_with_overrides(assignment_path, {"cart_total": 45, "is_domestic": True, "is_premium_member": False})
    expected = "STANDARD\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_free_when_over_threshold_and_domestic_not_premium():
    assignment_path = Path(__file__).resolve().parent / "05_shippingRules.py"
    out = _exec_with_overrides(assignment_path, {"cart_total": 50, "is_domestic": True, "is_premium_member": False})
    expected = "FREE\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_standard_when_over_threshold_but_not_domestic_and_not_premium():
    assignment_path = Path(__file__).resolve().parent / "05_shippingRules.py"
    out = _exec_with_overrides(assignment_path, {"cart_total": 100, "is_domestic": False, "is_premium_member": False})
    expected = "STANDARD\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"
