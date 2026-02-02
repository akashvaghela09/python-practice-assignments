import importlib
import ast
import sys


def _run_module_and_capture_stdout(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]
    import io
    import contextlib

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(module_name)
    return buf.getvalue()


def test_output_matches_expected():
    out = _run_module_and_capture_stdout("06_filter_stopwords")
    expected = "keep: ['quick', 'brown', 'fox']\n"
    assert expected == out, f"expected={expected!r} actual={out!r}"


def test_keep_value_is_correct_in_output():
    out = _run_module_and_capture_stdout("06_filter_stopwords")
    lines = [line for line in out.splitlines() if line.strip() != ""]
    assert len(lines) == 1, f"expected={1!r} actual={len(lines)!r}"

    line = lines[0]
    prefix = "keep: "
    assert line.startswith(prefix), f"expected={prefix!r} actual={line[:len(prefix)]!r}"

    actual_list = ast.literal_eval(line[len(prefix):])
    expected_list = ["quick", "brown", "fox"]
    assert expected_list == actual_list, f"expected={expected_list!r} actual={actual_list!r}"


def test_source_uses_not_in():
    with open("06_filter_stopwords.py", "r", encoding="utf-8") as f:
        src = f.read()
    assert " not in " in src, f"expected={' not in '!r} actual={src!r}"