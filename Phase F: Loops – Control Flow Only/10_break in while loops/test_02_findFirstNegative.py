import io
import os
import sys
import importlib.util
import contextlib
import builtins
import pytest

MODULE_FILENAME = "02_findFirstNegative.py"


def load_module_from_path(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_program_with_inputs(tmp_path, inputs):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    dst = tmp_path / MODULE_FILENAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    it = iter(inputs)

    def fake_input(prompt=None):
        return next(it)

    out = io.StringIO()
    old_input = builtins.input
    builtins.input = fake_input
    try:
        with contextlib.redirect_stdout(out):
            load_module_from_path(str(dst), "student_module")
    finally:
        builtins.input = old_input

    return out.getvalue()


def test_prints_first_negative_and_stops(tmp_path, capsys):
    try:
        output = run_program_with_inputs(tmp_path, ["4", "2", "-7", "9"])
    except StopIteration:
        pytest.fail("")

    expected = "First negative: -7\n"
    if output != expected:
        sys.stderr.write(f"expected={expected!r} actual={output!r}\n")
    assert output == expected


def test_stops_immediately_at_first_negative(tmp_path):
    try:
        output = run_program_with_inputs(tmp_path, ["-1", "999"])
    except StopIteration:
        pytest.fail("")

    expected = "First negative: -1\n"
    if output != expected:
        sys.stderr.write(f"expected={expected!r} actual={output!r}\n")
    assert output == expected


def test_ignores_non_negative_until_negative(tmp_path):
    try:
        output = run_program_with_inputs(tmp_path, ["0", "5", "3", "-2", "10"])
    except StopIteration:
        pytest.fail("")

    expected = "First negative: -2\n"
    if output != expected:
        sys.stderr.write(f"expected={expected!r} actual={output!r}\n")
    assert output == expected