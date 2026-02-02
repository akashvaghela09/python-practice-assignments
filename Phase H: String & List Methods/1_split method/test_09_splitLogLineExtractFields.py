import importlib
import io
import contextlib
import sys


def run_module_capture(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(module_name)
    return buf.getvalue()


def test_output_fields_exact():
    out = run_module_capture("09_splitLogLineExtractFields").strip()
    expected = "2026-02-02 WARNING Disk almost full"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_output_has_three_fields():
    out = run_module_capture("09_splitLogLineExtractFields").strip()
    parts = out.split()
    expected_count = 3
    actual_count = len(parts)
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"


def test_output_contains_no_delimiters():
    out = run_module_capture("09_splitLogLineExtractFields").strip()
    expected = False
    actual = ("|" in out)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_module_exports_expected_names():
    if "09_splitLogLineExtractFields" in sys.modules:
        del sys.modules["09_splitLogLineExtractFields"]
    m = importlib.import_module("09_splitLogLineExtractFields")
    for name in ("log", "parts", "date", "level", "message"):
        expected = True
        actual = hasattr(m, name)
        assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_extracted_values_match_output_tokens():
    if "09_splitLogLineExtractFields" in sys.modules:
        del sys.modules["09_splitLogLineExtractFields"]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        m = importlib.import_module("09_splitLogLineExtractFields")
    out = buf.getvalue().strip()
    tokens = out.split()
    expected = (tokens[0], tokens[1], " ".join(tokens[2:]))
    actual = (getattr(m, "date", None), getattr(m, "level", None), getattr(m, "message", None))
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_parts_split_count():
    if "09_splitLogLineExtractFields" in sys.modules:
        del sys.modules["09_splitLogLineExtractFields"]
    m = importlib.import_module("09_splitLogLineExtractFields")
    expected = 3
    actual = len(getattr(m, "parts"))
    assert actual == expected, f"expected={expected!r} actual={actual!r}"