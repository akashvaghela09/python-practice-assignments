import importlib.util
import os
import sys
import re
import pytest

FILE_NAME = "03_countVowels.py"


def _run_script_and_capture_stdout(path):
    spec = importlib.util.spec_from_file_location("student_module_03_countVowels", path)
    module = importlib.util.module_from_spec(spec)
    old_stdout = sys.stdout
    try:
        from io import StringIO
        buf = StringIO()
        sys.stdout = buf
        spec.loader.exec_module(module)
        output = buf.getvalue()
    finally:
        sys.stdout = old_stdout
    return output


def _extract_last_int(output):
    ints = re.findall(r"[-+]?\d+", output)
    if not ints:
        return None
    return int(ints[-1])


@pytest.fixture(scope="module")
def script_path():
    here = os.path.dirname(__file__)
    return os.path.join(here, FILE_NAME)


def test_file_exists(script_path):
    assert os.path.exists(script_path)


def test_no_placeholders_left(script_path):
    content = open(script_path, "r", encoding="utf-8").read()
    assert "____" not in content


def test_outputs_expected_count(capsys, script_path):
    expected = None
    text = "Education"
    vowels = set("aeiouAEIOU")
    expected = sum(1 for ch in text if ch in vowels)

    output = _run_script_and_capture_stdout(script_path)
    actual = _extract_last_int(output)

    assert actual is not None, f"expected={expected} actual={actual}"
    assert actual == expected, f"expected={expected} actual={actual}"


def test_prints_a_single_number_line(script_path):
    output = _run_script_and_capture_stdout(script_path).strip().splitlines()
    last = output[-1].strip() if output else ""
    assert re.fullmatch(r"[-+]?\d+", last) is not None, f"expected={'<integer>'} actual={last!r}"


def test_uses_for_loop_in_source(script_path):
    content = open(script_path, "r", encoding="utf-8").read()
    assert re.search(r"^\s*for\s+.+\s+in\s+.+:", content, flags=re.MULTILINE) is not None, f"expected={'<for-loop>'} actual={'<missing>'}"