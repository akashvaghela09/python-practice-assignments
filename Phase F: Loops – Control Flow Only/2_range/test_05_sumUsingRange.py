import importlib.util
import io
import os
import contextlib
import re


def _run_script(path):
    spec = importlib.util.spec_from_file_location("target_module_05", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(module)
    return buf.getvalue()


def test_outputs_single_integer_5050():
    path = os.path.join(os.path.dirname(__file__), "05_sumUsingRange.py")
    out = _run_script(path)

    nums = re.findall(r"-?\d+", out)
    assert len(nums) == 1, f"expected 1 integer output, actual {len(nums)}"
    actual = int(nums[0])
    expected = 5050
    assert actual == expected, f"expected {expected}, actual {actual}"


def test_no_placeholders_left():
    path = os.path.join(os.path.dirname(__file__), "05_sumUsingRange.py")
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    expected = False
    actual = "_____" in src
    assert actual == expected, f"expected {expected}, actual {actual}"