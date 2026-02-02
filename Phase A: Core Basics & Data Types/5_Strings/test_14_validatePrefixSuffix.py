import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout

MODULE_FILENAME = "14_validatePrefixSuffix.py"


def _run_module_capture_stdout(path):
    spec = importlib.util.spec_from_file_location("mod_14_validatePrefixSuffix", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)
    return module, buf.getvalue()


def test_prints_single_boolean_line_true(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    tmp_file = tmp_path / MODULE_FILENAME
    tmp_file.write_text(open(src_path, "r", encoding="utf-8").read(), encoding="utf-8")

    _, out = _run_module_capture_stdout(str(tmp_file))
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 1, f"expected=1 actual={len(lines)}"
    assert lines[0] in ("True", "False"), f"expected={'bool-string'} actual={lines[0]}"
    assert lines[0] == "True", f"expected=True actual={lines[0]}"


def test_is_valid_is_boolean_and_true(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    tmp_file = tmp_path / MODULE_FILENAME
    tmp_file.write_text(open(src_path, "r", encoding="utf-8").read(), encoding="utf-8")

    module, _ = _run_module_capture_stdout(str(tmp_file))
    assert hasattr(module, "is_valid"), f"expected={'has_is_valid'} actual={hasattr(module, 'is_valid')}"
    assert isinstance(module.is_valid, bool), f"expected=bool actual={type(module.is_valid).__name__}"
    assert module.is_valid is True, f"expected=True actual={module.is_valid}"


def test_filename_constant_is_expected_string(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    tmp_file = tmp_path / MODULE_FILENAME
    tmp_file.write_text(open(src_path, "r", encoding="utf-8").read(), encoding="utf-8")

    module, _ = _run_module_capture_stdout(str(tmp_file))
    assert hasattr(module, "filename"), f"expected={'has_filename'} actual={hasattr(module, 'filename')}"
    assert isinstance(module.filename, str), f"expected=str actual={type(module.filename).__name__}"
    assert module.filename == "test_strings.py", f"expected=test_strings.py actual={module.filename}"