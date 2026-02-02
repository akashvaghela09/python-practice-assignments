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
    path = Path(__file__).resolve().parent / "12_frozenDataclassPoint.py"
    out = _run_script(path)
    lines = out.splitlines()
    assert len(lines) == 2, f"expected output:\nPoint(x=2, y=5)\\nmutate error: FrozenInstanceError\\nactual output:\n{out}"
    assert lines[0] == "Point(x=2, y=5)", f"expected output:\nPoint(x=2, y=5)\nactual output:\n{out}"
    assert lines[1] == "mutate error: FrozenInstanceError", f"expected output:\nmutate error: FrozenInstanceError\nactual output:\n{out}"