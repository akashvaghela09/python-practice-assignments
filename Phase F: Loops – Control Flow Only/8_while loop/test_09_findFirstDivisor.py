import importlib.util
import io
import os
import re
import contextlib
import pytest

MODULE_FILE = "09_findFirstDivisor.py"


def load_module_from_path(path):
    spec = importlib.util.spec_from_file_location("student_mod_09", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_script_capture_stdout(path):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        load_module_from_path(path)
    return buf.getvalue()


def extract_smallest_divisor(output):
    m = re.search(r"Smallest divisor:\s*(-?\d+)\s*$", output.strip(), flags=re.MULTILINE)
    if not m:
        return None
    return int(m.group(1))


def smallest_divisor_ref(n):
    d = 2
    while d * d <= n and n % d != 0:
        d += 1
    return d if n % d == 0 else n


@pytest.mark.parametrize("n", [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 25, 27, 49, 91, 121, 143, 169])
def test_smallest_divisor_matches_reference(tmp_path, n):
    src = os.path.join(os.getcwd(), MODULE_FILE)
    assert os.path.exists(src), f"expected={MODULE_FILE} actual=missing"
    code = open(src, "r", encoding="utf-8").read()

    patched = re.sub(r"^number\s*=\s*91\s*$", f"number = {n}", code, flags=re.MULTILINE)
    if patched == code:
        patched = f"number = {n}\n" + code

    dst = tmp_path / MODULE_FILE
    dst.write_text(patched, encoding="utf-8")

    out = run_script_capture_stdout(str(dst))
    actual = extract_smallest_divisor(out)
    expected = smallest_divisor_ref(n)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_prints_expected_line_format_for_91():
    src = os.path.join(os.getcwd(), MODULE_FILE)
    assert os.path.exists(src), f"expected={MODULE_FILE} actual=missing"
    out = run_script_capture_stdout(src)
    m = re.search(r"^Smallest divisor:\s*(\d+)\s*$", out.strip(), flags=re.MULTILINE)
    actual = m.group(0) if m else None
    expected = "Smallest divisor: 7"
    assert actual == expected, f"expected={expected} actual={actual}"


def test_uses_while_loop_in_source():
    src = os.path.join(os.getcwd(), MODULE_FILE)
    assert os.path.exists(src), f"expected={MODULE_FILE} actual=missing"
    code = open(src, "r", encoding="utf-8").read()
    has_while = bool(re.search(r"^\s*while\s+", code, flags=re.MULTILINE))
    assert has_while is True, f"expected={True} actual={has_while}"