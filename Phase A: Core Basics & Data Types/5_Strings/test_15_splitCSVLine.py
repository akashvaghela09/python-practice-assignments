import importlib.util
import io
import os
import contextlib


def run_module_capture_stdout(module_filename):
    path = os.path.join(os.path.dirname(__file__), module_filename)
    spec = importlib.util.spec_from_file_location("student_mod_15_splitCSVLine", path)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return mod, buf.getvalue()


def test_stdout_matches_expected_format():
    _, out = run_module_capture_stdout("15_splitCSVLine.py")
    expected = "Ada | Lovelace | 36\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_parts_is_list_and_has_three_fields():
    mod, _ = run_module_capture_stdout("15_splitCSVLine.py")
    expected = ["Ada", "Lovelace", "36"]
    assert isinstance(mod.parts, list), f"expected={list!r} actual={type(mod.parts)!r}"
    assert mod.parts == expected, f"expected={expected!r} actual={mod.parts!r}"


def test_join_of_parts_matches_output_without_newline():
    mod, out = run_module_capture_stdout("15_splitCSVLine.py")
    expected = "Ada | Lovelace | 36"
    actual = " | ".join(mod.parts)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert out.rstrip("\n") == expected, f"expected={expected!r} actual={out.rstrip(chr(10))!r}"