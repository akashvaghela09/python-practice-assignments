import importlib.util
import io
import os
import sys


def load_module_capture_stdout(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old
    return module, buf.getvalue()


def test_output_exact_digits_only():
    module, out = load_module_capture_stdout(
        "m19_extractDigits", os.path.join(os.path.dirname(__file__), "19_extractDigits.py")
    )
    assert out.strip() == "5551234", f"expected={'5551234'} actual={out.strip()}"


def test_digits_variable_matches_extracted():
    module, _ = load_module_capture_stdout(
        "m19_extractDigits_2", os.path.join(os.path.dirname(__file__), "19_extractDigits.py")
    )
    expected = "".join(ch for ch in module.text if ch.isdigit())
    actual = getattr(module, "digits", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_digits_contains_only_digits_chars():
    module, _ = load_module_capture_stdout(
        "m19_extractDigits_3", os.path.join(os.path.dirname(__file__), "19_extractDigits.py")
    )
    actual = getattr(module, "digits", None)
    assert isinstance(actual, str), f"expected={str} actual={type(actual)}"
    assert all(ch.isdigit() for ch in actual), f"expected={'only digits'} actual={actual}"