import importlib.util
import io
import os
import sys
import pytest


def load_module(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_module_capture_stdout(path, module_name):
    old_stdout = sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    try:
        module = load_module(path, module_name)
    finally:
        sys.stdout = old_stdout
    return module, buf.getvalue()


def test_prints_expected_output():
    path = os.path.join(os.path.dirname(__file__), "07_ternary_with_multiple_conditions.py")
    _, out = run_module_capture_stdout(path, "m07_out")
    expected = "teen\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_label_variable_is_defined_and_correct():
    path = os.path.join(os.path.dirname(__file__), "07_ternary_with_multiple_conditions.py")
    module, out = run_module_capture_stdout(path, "m07_label")
    expected_label = "teen"
    assert hasattr(module, "label"), "expected label variable to exist"
    assert module.label == expected_label, f"expected={expected_label!r} actual={getattr(module, 'label', None)!r}"
    expected_out = expected_label + "\n"
    assert out == expected_out, f"expected={expected_out!r} actual={out!r}"


def test_age_is_teen_boundary_value():
    path = os.path.join(os.path.dirname(__file__), "07_ternary_with_multiple_conditions.py")
    module, _ = run_module_capture_stdout(path, "m07_age")
    assert hasattr(module, "age"), "expected age variable to exist"
    assert module.age == 19, f"expected={19!r} actual={getattr(module, 'age', None)!r}"