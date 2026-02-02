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


def test_stdout_exact_match_final_view():
    script_path = Path(__file__).resolve().parent / "09_printProgressLine.py"
    actual = _run_script(script_path)

    expected_final = "Loading... 100%\n"

    if actual == expected_final:
        assert True
        return

    if "\r" in actual:
        tail = actual.split("\r")[-1]
        assert tail == expected_final, f"Expected output:\n{expected_final}\nActual output:\n{tail}"
    else:
        assert actual == expected_final, f"Expected output:\n{expected_final}\nActual output:\n{actual}"
