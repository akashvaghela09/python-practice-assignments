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


def test_manual_review_count_default_orders():
    assignment_path = Path(__file__).resolve().parent / "09_filterOrders.py"
    out = _run_module(assignment_path)
    expected = "MANUAL REVIEW COUNT: 3\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_manual_review_count_with_extra_order():
    assignment_path = Path(__file__).resolve().parent / "09_filterOrders.py"
    orders = [
        {"id": 1, "amount": 1500, "is_international": True,  "is_flagged": False},
        {"id": 2, "amount": 900,  "is_international": True,  "is_flagged": False},
        {"id": 3, "amount": 2500, "is_international": False, "is_flagged": False},
        {"id": 4, "amount": 120,  "is_international": False, "is_flagged": True},
        {"id": 5, "amount": 80,   "is_international": False, "is_flagged": True},
        {"id": 6, "amount": 1100, "is_international": False, "is_flagged": False},
        {"id": 7, "amount": 2100, "is_international": False, "is_flagged": False}
    ]
    out = _exec_with_overrides(assignment_path, {"orders": orders})
    expected = "MANUAL REVIEW COUNT: 4\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"
