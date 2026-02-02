import importlib.util
import sys
from pathlib import Path


def _run_module_capture_stdout(module_filename):
    path = Path(__file__).resolve().parent / module_filename
    spec = importlib.util.spec_from_file_location(module_filename.replace(".py", ""), str(path))
    module = importlib.util.module_from_spec(spec)

    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)
    return buf.getvalue(), module


def test_output_username_correct():
    out, _ = _run_module_capture_stdout("07_validateUsernameStopAtSpace.py")
    actual = out.strip().splitlines()[-1] if out.strip().splitlines() else ""
    expected = "alice"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_username_stops_at_first_space_no_trailing_chars():
    out, _ = _run_module_capture_stdout("07_validateUsernameStopAtSpace.py")
    actual = out.strip().splitlines()[-1] if out.strip().splitlines() else ""
    assert "bob" not in actual.lower(), f"expected={'no-bob'!r} actual={actual!r}"


def test_username_contains_only_lowercase_letters():
    out, _ = _run_module_capture_stdout("07_validateUsernameStopAtSpace.py")
    actual = out.strip().splitlines()[-1] if out.strip().splitlines() else ""
    only_lower_letters = all("a" <= c <= "z" for c in actual)
    assert only_lower_letters, f"expected={'only a-z lowercase'!r} actual={actual!r}"


def test_prints_single_line_username():
    out, _ = _run_module_capture_stdout("07_validateUsernameStopAtSpace.py")
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    actual_count = len(lines)
    expected_count = 1
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"