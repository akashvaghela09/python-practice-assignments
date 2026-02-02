import sys
import importlib.util
from pathlib import Path
import pytest


def _run_script_capture_stdout(script_path: Path) -> str:
    if not script_path.exists():
        pytest.fail(f"expected output:\nAda | Lovelace | 36\n\nactual output:\n<missing file: {script_path.name}>\n")

    spec = importlib.util.spec_from_file_location(script_path.stem, str(script_path))
    if spec is None or spec.loader is None:
        pytest.fail(f"expected output:\nAda | Lovelace | 36\n\nactual output:\n<could not load module>\n")

    module = importlib.util.module_from_spec(spec)
    old_stdout = sys.stdout
    try:
        from io import StringIO
        buf = StringIO()
        sys.stdout = buf
        spec.loader.exec_module(module)
        return buf.getvalue()
    finally:
        sys.stdout = old_stdout


def test_stdout_exact():
    script_path = Path(__file__).resolve().parent / "15_splitCSVLine.py"
    expected = "Ada | Lovelace | 36\n"
    actual = _run_script_capture_stdout(script_path)
    if actual != expected:
        pytest.fail(f"expected output:\n{expected}\nactual output:\n{actual}")
