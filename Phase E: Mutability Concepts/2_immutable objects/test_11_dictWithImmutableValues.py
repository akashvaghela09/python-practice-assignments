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
    path = Path(__file__).resolve().parent / "11_dictWithImmutableValues.py"
    out = _run_script(path)
    expected = "before: (1, 2)\nafter: (1, 2, 3)\n"
    assert out == expected, f"expected output:\n{expected}actual output:\n{out}"