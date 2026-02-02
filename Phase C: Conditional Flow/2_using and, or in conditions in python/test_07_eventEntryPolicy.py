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


def test_enter_vip_guest_list_no_ticket_default():
    assignment_path = Path(__file__).resolve().parent / "07_eventEntryPolicy.py"
    out = _run_module(assignment_path)
    expected = "ENTER\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_deny_underage_without_accompanied_even_with_ticket():
    assignment_path = Path(__file__).resolve().parent / "07_eventEntryPolicy.py"
    out = _exec_with_overrides(
        assignment_path,
        {"has_ticket": True, "is_vip": False, "on_guest_list": False, "age": 16, "accompanied": False},
    )
    expected = "DENY\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_enter_regular_adult_with_ticket():
    assignment_path = Path(__file__).resolve().parent / "07_eventEntryPolicy.py"
    out = _exec_with_overrides(
        assignment_path,
        {"has_ticket": True, "is_vip": False, "on_guest_list": False, "age": 25, "accompanied": False},
    )
    expected = "ENTER\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_enter_underage_with_ticket_and_accompanied():
    assignment_path = Path(__file__).resolve().parent / "07_eventEntryPolicy.py"
    out = _exec_with_overrides(
        assignment_path,
        {"has_ticket": True, "is_vip": False, "on_guest_list": False, "age": 17, "accompanied": True},
    )
    expected = "ENTER\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"


def test_deny_vip_not_on_guest_list_without_ticket():
    assignment_path = Path(__file__).resolve().parent / "07_eventEntryPolicy.py"
    out = _exec_with_overrides(
        assignment_path,
        {"has_ticket": False, "is_vip": True, "on_guest_list": False, "age": 30, "accompanied": False},
    )
    expected = "DENY\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"
