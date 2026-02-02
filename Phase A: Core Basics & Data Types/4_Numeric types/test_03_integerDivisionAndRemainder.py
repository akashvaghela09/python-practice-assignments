import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout

def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_outputs_exact_lines():
    path = os.path.join(os.path.dirname(__file__), "03_integerDivisionAndRemainder.py")
    buf = io.StringIO()
    with redirect_stdout(buf):
        load_module(path, "assignment03_run")
    out = buf.getvalue().splitlines()
    expected = ["3", "2"]
    assert out == expected, f"expected={expected!r} actual={out!r}"

def test_quotient_and_remainder_values():
    path = os.path.join(os.path.dirname(__file__), "03_integerDivisionAndRemainder.py")
    module = load_module(path, "assignment03_vals")
    expected_q = module.numerator // module.denominator
    expected_r = module.numerator % module.denominator

    assert hasattr(module, "quotient"), "quotient missing"
    assert hasattr(module, "remainder"), "remainder missing"

    actual_q = module.quotient
    actual_r = module.remainder

    assert actual_q == expected_q, f"expected={expected_q!r} actual={actual_q!r}"
    assert actual_r == expected_r, f"expected={expected_r!r} actual={actual_r!r}"

def test_types_are_integers():
    path = os.path.join(os.path.dirname(__file__), "03_integerDivisionAndRemainder.py")
    module = load_module(path, "assignment03_types")
    assert isinstance(module.quotient, int), f"expected={int!r} actual={type(module.quotient)!r}"
    assert isinstance(module.remainder, int), f"expected={int!r} actual={type(module.remainder)!r}"