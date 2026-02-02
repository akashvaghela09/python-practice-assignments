import importlib.util
import io
import os
import contextlib


def _run_module_capture_stdout(module_filename):
    spec = importlib.util.spec_from_file_location(
        "student_module", os.path.join(os.path.dirname(__file__), module_filename)
    )
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(module)
    return module, buf.getvalue()


def test_output_is_world():
    _, out = _run_module_capture_stdout("06_sliceSubstring.py")
    actual = out.strip()
    expected = "world"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_sub_variable_is_world():
    module, _ = _run_module_capture_stdout("06_sliceSubstring.py")
    actual = getattr(module, "sub", None)
    expected = "world"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_text_unchanged_and_substring_matches():
    module, _ = _run_module_capture_stdout("06_sliceSubstring.py")
    text = getattr(module, "text", None)
    sub = getattr(module, "sub", None)
    expected_text = "hello world"
    assert text == expected_text, f"expected={expected_text!r} actual={text!r}"
    expected_sub = text[6:] if isinstance(text, str) else None
    assert sub == expected_sub, f"expected={expected_sub!r} actual={sub!r}"