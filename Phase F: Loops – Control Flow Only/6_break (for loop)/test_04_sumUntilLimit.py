import importlib
import io
import os
import re
import sys


def _run_module_capture_stdout(module_name):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        if module_name in sys.modules:
            del sys.modules[module_name]
        importlib.import_module(module_name)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout


def _extract_last_int(output):
    ints = re.findall(r"-?\d+", output)
    if not ints:
        return None
    return int(ints[-1])


def test_prints_single_integer_line():
    out = _run_module_capture_stdout("04_sumUntilLimit")
    val = _extract_last_int(out)
    assert val is not None, f"expected int, actual output={out!r}"
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert lines, f"expected non-empty output, actual output={out!r}"
    assert lines[-1] == str(val), f"expected last line to be integer, actual last line={lines[-1]!r}"


def test_total_matches_algorithm_on_given_nums():
    out = _run_module_capture_stdout("04_sumUntilLimit")
    actual = _extract_last_int(out)
    assert actual is not None, f"expected int, actual output={out!r}"

    nums = [5, 4, 6, 2, 9]
    limit = 15
    expected = 0
    for n in nums:
        if expected + n > limit:
            break
        expected += n

    assert actual == expected, f"expected={expected}, actual={actual}"


def test_does_not_exceed_limit():
    out = _run_module_capture_stdout("04_sumUntilLimit")
    actual = _extract_last_int(out)
    assert actual is not None, f"expected int, actual output={out!r}"
    limit = 15
    assert actual <= limit, f"expected<={limit}, actual={actual}"


def test_has_break_condition_comment_present():
    fname = os.path.join(os.path.dirname(__file__), "04_sumUntilLimit.py")
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()
    assert "break" in content, f"expected to contain 'break', actual length={len(content)}"