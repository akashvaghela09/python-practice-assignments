import sys
import importlib.util
from pathlib import Path
import pytest


def _run_script(path: Path):
    if not path.exists():
        pytest.fail(f"Assignment file does not exist: {path}")

    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    if spec is None or spec.loader is None:
        pytest.fail(f"Could not load assignment module: {path}")

    module = importlib.util.module_from_spec(spec)

    captured = []

    def _fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        text = sep.join(str(a) for a in args) + end
        captured.append(text)

    original_print = __builtins__["print"] if isinstance(__builtins__, dict) else __builtins__.print
    try:
        if isinstance(__builtins__, dict):
            __builtins__["print"] = _fake_print
        else:
            __builtins__.print = _fake_print
        spec.loader.exec_module(module)
    finally:
        if isinstance(__builtins__, dict):
            __builtins__["print"] = original_print
        else:
            __builtins__.print = original_print

    return "".join(captured)


def test_stdout_exact():
    assignment_path = Path(__file__).resolve().parent / "07_numericTypePromotion.py"
    actual = _run_script(assignment_path)
    expected = "<class 'float'>\n<class 'complex'>\n"
    assert actual == expected, f"expected output:\n{expected}\nactual output:\n{actual}"
