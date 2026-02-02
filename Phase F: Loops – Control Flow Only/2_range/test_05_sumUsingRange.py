import sys
import importlib.util
from pathlib import Path


def _run_script(script_path: Path):
    if not script_path.exists():
        raise AssertionError(f"Expected output:\n5050\nActual output:\n<missing file: {script_path.name}>")

    spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
    module = importlib.util.module_from_spec(spec)

    old_stdout = sys.stdout
    try:
        from io import StringIO
        buf = StringIO()
        sys.stdout = buf
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
        return buf.getvalue()
    finally:
        sys.stdout = old_stdout


def test_output_exact():
    script_path = Path(__file__).resolve().parent / "05_sumUsingRange.py"
    actual = _run_script(script_path)
    expected = "5050\n"
    if actual != expected:
        raise AssertionError(f"Expected output:\n{expected}Actual output:\n{actual}")
