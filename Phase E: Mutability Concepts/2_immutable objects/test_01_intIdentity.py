import importlib.util
import io
import os
import re
import contextlib
import pytest

MODULE_FILENAME = "01_intIdentity.py"


def load_module_from_path(path):
    spec = importlib.util.spec_from_file_location("mod_01_intIdentity", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_script_capture_stdout(path):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        module = load_module_from_path(path)
    return module, buf.getvalue()


def extract_last_int(s):
    m = re.search(r"(-?\d+)\s*$", s.strip())
    if not m:
        return None
    return int(m.group(1))


def test_prints_two_distinct_integer_ids_and_identity_false():
    module, out = run_script_capture_stdout(os.path.join(os.getcwd(), MODULE_FILENAME))
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) >= 3, f"expected>=3 got={len(lines)}"

    before_val = extract_last_int(lines[0])
    after_val = extract_last_int(lines[1])
    assert before_val is not None, f"expected=int got={lines[0]!r}"
    assert after_val is not None, f"expected=int got={lines[1]!r}"
    assert before_val != after_val, f"expected!={before_val} got={after_val}"

    assert lines[2].startswith("x is y?"), f"expected_prefix='x is y?' got={lines[2]!r}"
    assert lines[2].endswith("False"), f"expected=False got={lines[2]!r}"


def test_before_after_match_runtime_ids():
    module, out = run_script_capture_stdout(os.path.join(os.getcwd(), MODULE_FILENAME))
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    before_val = extract_last_int(lines[0])
    after_val = extract_last_int(lines[1])

    assert before_val == id(module.x), f"expected={id(module.x)} got={before_val}"
    assert after_val == id(module.y), f"expected={id(module.y)} got={after_val}"
    assert module.x is not module.y, f"expected=True got={module.x is not module.y}"


def test_before_after_not_none_and_are_ints():
    module, out = run_script_capture_stdout(os.path.join(os.getcwd(), MODULE_FILENAME))
    assert hasattr(module, "before"), "expected=attr got=missing"
    assert hasattr(module, "after"), "expected=attr got=missing"
    assert module.before is not None, f"expected!=None got={module.before!r}"
    assert module.after is not None, f"expected!=None got={module.after!r}"
    assert isinstance(module.before, int), f"expected=int got={type(module.before).__name__}"
    assert isinstance(module.after, int), f"expected=int got={type(module.after).__name__}"