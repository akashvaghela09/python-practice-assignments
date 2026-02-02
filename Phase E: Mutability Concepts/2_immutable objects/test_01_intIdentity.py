import sys
import importlib.util
from pathlib import Path


def _run_script(path: Path):
    if not path.exists():
        raise AssertionError(f"Missing assignment file: {path}")
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    mod = importlib.util.module_from_spec(spec)
    old_stdout = sys.stdout
    try:
        from io import StringIO
        buf = StringIO()
        sys.stdout = buf
        spec.loader.exec_module(mod)  # type: ignore[attr-defined]
        return buf.getvalue()
    finally:
        sys.stdout = old_stdout


def test_stdout_exact():
    path = Path(__file__).resolve().parent / "01_intIdentity.py"
    out = _run_script(path)
    lines = [ln for ln in out.splitlines() if ln != ""]
    assert len(lines) == 3, f"expected output:\n<3 non-empty lines>\nactual output:\n{out}"

    try:
        before = int(lines[0])
        after = int(lines[1])
    except Exception:
        raise AssertionError(f"expected output:\n<two integer ids then 'x is y? False'>\nactual output:\n{out}")

    assert before != after, f"expected output:\n<two different ids>\nactual output:\n{out}"
    assert lines[2] == "x is y? False", f"expected output:\nx is y? False\nactual output:\n{out}"