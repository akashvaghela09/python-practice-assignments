import importlib.util
import io
import os
import contextlib
import pytest


def _load_module_from_path(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_and_capture(path, module_name):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _load_module_from_path(path, module_name)
    return buf.getvalue()


def test_output_lines_exact():
    path = os.path.join(os.path.dirname(__file__), "02_numericLiteralsAndUnderscores.py")
    out = _run_and_capture(path, "mod_02_numericLiteralsAndUnderscores_out")
    expected = "1000000\n255\n10\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_variables_defined_and_values():
    path = os.path.join(os.path.dirname(__file__), "02_numericLiteralsAndUnderscores.py")
    module = _load_module_from_path(path, "mod_02_numericLiteralsAndUnderscores_vars")
    assert hasattr(module, "million"), f"expected={'hasattr(million)'} actual={hasattr(module, 'million')}"
    assert hasattr(module, "hex_ff"), f"expected={'hasattr(hex_ff)'} actual={hasattr(module, 'hex_ff')}"
    assert hasattr(module, "binary_ten"), f"expected={'hasattr(binary_ten)'} actual={hasattr(module, 'binary_ten')}"
    expected_vals = (1000000, 255, 10)
    actual_vals = (module.million, module.hex_ff, module.binary_ten)
    assert actual_vals == expected_vals, f"expected={expected_vals!r} actual={actual_vals!r}"


@pytest.mark.parametrize("attr", ["million", "hex_ff", "binary_ten"])
def test_values_are_int(attr):
    path = os.path.join(os.path.dirname(__file__), "02_numericLiteralsAndUnderscores.py")
    module = _load_module_from_path(path, f"mod_02_numericLiteralsAndUnderscores_type_{attr}")
    val = getattr(module, attr)
    assert isinstance(val, int), f"expected={int!r} actual={type(val)!r}"