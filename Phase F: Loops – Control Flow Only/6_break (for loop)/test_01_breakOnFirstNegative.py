import importlib.util
import pathlib
import sys


def _run_module_capture_stdout(path):
    spec = importlib.util.spec_from_file_location("student_mod_01", str(path))
    mod = importlib.util.module_from_spec(spec)

    import io
    import contextlib

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return buf.getvalue()


def test_break_on_first_negative_output_matches_expected(capsys):
    import 01_breakOnFirstNegative as _  # noqa: F401
    captured = capsys.readouterr().out
    expected = "4\n2\n7\n"
    assert expected == captured


def test_module_runs_without_extra_output_when_executed_directly(tmp_path):
    src = pathlib.Path(__file__).resolve().parent / "01_breakOnFirstNegative.py"
    code = src.read_text(encoding="utf-8")

    dst = tmp_path / "01_breakOnFirstNegative.py"
    dst.write_text(code, encoding="utf-8")

    out = _run_module_capture_stdout(dst)
    expected = "4\n2\n7\n"
    assert expected == out