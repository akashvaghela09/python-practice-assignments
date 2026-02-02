import sys
import importlib.util
from pathlib import Path


def _run_script(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"Expected file does not exist: {path}")

    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)

    old_stdout = sys.stdout
    try:
        from io import StringIO
        buf = StringIO()
        sys.stdout = buf
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        return buf.getvalue()
    finally:
        sys.stdout = old_stdout


def test_stdout_exact_match():
    script_path = Path(__file__).resolve().parent / "01_printHello.py"
    actual = _run_script(script_path)
    expected = "Hello, world!\n"
    assert actual == expected, f"Expected output:\n{expected}\nActual output:\n{actual}"
