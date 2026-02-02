import io
import sys
import importlib.util
from pathlib import Path

import pytest


def _run_script(path: Path):
    if not path.exists():
        pytest.fail(f"Missing assignment file: {path}")

    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout


def test_stdout_exact():
    assignment_path = Path(__file__).resolve().parent / "01_typeOfLiterals.py"
    actual = _run_script(assignment_path)
    expected = "<class 'int'>\n<class 'float'>\n<class 'str'>\n<class 'bool'>\n"
    assert actual == expected, f"expected output:\n{expected}\nactual output:\n{actual}"
