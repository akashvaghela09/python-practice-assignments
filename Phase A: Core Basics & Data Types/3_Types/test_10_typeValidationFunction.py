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
    assignment_path = Path(__file__).resolve().parent / "10_typeValidationFunction.py"
    actual = _run_script(assignment_path)
    expected = "ok:int\nok:float\nerror:expected number\nok:bool\nerror:expected number\n"
    assert actual == expected, f"expected output:\n{expected}\nactual output:\n{actual}"


def test_classify_number_additional_cases():
    assignment_path = Path(__file__).resolve().parent / "10_typeValidationFunction.py"
    if not assignment_path.exists():
        pytest.fail(f"Missing assignment file: {assignment_path}")

    spec = importlib.util.spec_from_file_location(assignment_path.stem + "_mod", str(assignment_path))
    module = importlib.util.module_from_spec(spec)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        spec.loader.exec_module(module)  # type: ignore[union-attr]
    finally:
        sys.stdout = old_stdout

    assert hasattr(module, "classify_number"), "expected output:\n<function classify_number>\nactual output:\n<missing classify_number>"

    fn = module.classify_number
    assert fn(False) == "ok:bool", f"expected output:\nok:bool\nactual output:\n{fn(False)}"
    assert fn(0) == "ok:int", f"expected output:\nok:int\nactual output:\n{fn(0)}"
    assert fn(0.0) == "ok:float", f"expected output:\nok:float\nactual output:\n{fn(0.0)}"
    assert fn([]) == "error:expected number", f"expected output:\nerror:expected number\nactual output:\n{fn([])}"
