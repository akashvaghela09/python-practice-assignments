import importlib.util
import io
import os
import sys
import types
import pytest

MODULE_FILENAME = "02_whileCountDown.py"


def _expected_lines():
    return [str(i) for i in range(5, 0, -1)]


def _import_module_capturing_stdout(tmp_path, monkeypatch):
    src_path = os.path.join(os.getcwd(), MODULE_FILENAME)
    if not os.path.exists(src_path):
        pytest.fail(f"Missing file: {MODULE_FILENAME}")

    dst_path = tmp_path / MODULE_FILENAME
    dst_path.write_text(open(src_path, "r", encoding="utf-8").read(), encoding="utf-8")

    monkeypatch.chdir(tmp_path)

    captured = io.StringIO()
    monkeypatch.setattr(sys, "stdout", captured)

    spec = importlib.util.spec_from_file_location("student_module", str(dst_path))
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
    except Exception as e:
        return None, captured.getvalue(), e
    return mod, captured.getvalue(), None


def test_runs_without_error_and_prints_countdown(tmp_path, monkeypatch):
    mod, out, err = _import_module_capturing_stdout(tmp_path, monkeypatch)
    assert err is None, f"expected no exception, actual {type(err).__name__ if err else None}"

    actual = out.splitlines()
    expected = _expected_lines()
    assert actual == expected, f"expected {expected}, actual {actual}"


def test_prints_exactly_five_lines(tmp_path, monkeypatch):
    mod, out, err = _import_module_capturing_stdout(tmp_path, monkeypatch)
    assert err is None, f"expected no exception, actual {type(err).__name__ if err else None}"

    actual_count = len(out.splitlines())
    expected_count = 5
    assert actual_count == expected_count, f"expected {expected_count}, actual {actual_count}"


def test_output_has_no_extra_whitespace_lines(tmp_path, monkeypatch):
    mod, out, err = _import_module_capturing_stdout(tmp_path, monkeypatch)
    assert err is None, f"expected no exception, actual {type(err).__name__ if err else None}"

    lines = out.splitlines()
    stripped_lines = [ln.strip() for ln in lines]
    assert stripped_lines == lines, f"expected {stripped_lines}, actual {lines}"


def test_final_line_is_one(tmp_path, monkeypatch):
    mod, out, err = _import_module_capturing_stdout(tmp_path, monkeypatch)
    assert err is None, f"expected no exception, actual {type(err).__name__ if err else None}"

    lines = out.splitlines()
    expected = _expected_lines()[-1]
    actual = lines[-1] if lines else None
    assert actual == expected, f"expected {expected}, actual {actual}"


def test_does_not_prompt_for_input(monkeypatch, tmp_path):
    def _bad_input(*args, **kwargs):
        raise AssertionError("input called")

    monkeypatch.setattr("builtins.input", _bad_input)

    mod, out, err = _import_module_capturing_stdout(tmp_path, monkeypatch)
    assert not isinstance(err, AssertionError), f"expected no input call error, actual {type(err).__name__ if err else None}"