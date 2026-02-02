import importlib.util
import os
import sys

import pytest


def load_module_capture_output(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    captured = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        captured.append(sep.join(str(a) for a in args) + end)

    module.__dict__["print"] = fake_print
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        return None, "".join(captured), e
    return module, "".join(captured), None


def test_script_runs_without_error():
    path = os.path.join(os.path.dirname(__file__), "07_andOrPrecedence.py")
    module, out, err = load_module_capture_output(path, "mod_07_andOrPrecedence_runs")
    assert err is None, f"expected no error, actual {type(err).__name__ if err else None}"


def test_prints_access_granted_exactly():
    path = os.path.join(os.path.dirname(__file__), "07_andOrPrecedence.py")
    module, out, err = load_module_capture_output(path, "mod_07_andOrPrecedence_output")
    if err is not None:
        pytest.fail(f"expected successful execution, actual {type(err).__name__}")
    assert out == "ACCESS GRANTED\n", f"expected {'ACCESS GRANTED\\n'!r}, actual {out!r}"


def test_no_extra_output_lines():
    path = os.path.join(os.path.dirname(__file__), "07_andOrPrecedence.py")
    module, out, err = load_module_capture_output(path, "mod_07_andOrPrecedence_lines")
    if err is not None:
        pytest.fail(f"expected successful execution, actual {type(err).__name__}")
    lines = out.splitlines()
    assert len(lines) == 1, f"expected {1}, actual {len(lines)}"
    assert lines[0] == "ACCESS GRANTED", f"expected {'ACCESS GRANTED'!r}, actual {lines[0]!r}"


def test_contains_if_placeholder_filled():
    path = os.path.join(os.path.dirname(__file__), "07_andOrPrecedence.py")
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    assert "if __:" not in src, f"expected {'if __:'!r} absent, actual present"