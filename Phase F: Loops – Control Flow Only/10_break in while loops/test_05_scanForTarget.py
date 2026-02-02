import builtins
import importlib.util
import os
import sys
import pytest


FILE_NAME = "05_scanForTarget.py"


def _run_with_inputs(inputs):
    outputs = []

    def fake_input(prompt=""):
        return inputs.pop(0)

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        outputs.append(sep.join(str(a) for a in args) + end)

    spec = importlib.util.spec_from_file_location("scan_module", os.path.join(os.getcwd(), FILE_NAME))
    module = importlib.util.module_from_spec(spec)

    old_input = builtins.input
    old_print = builtins.print
    try:
        builtins.input = fake_input
        builtins.print = fake_print
        spec.loader.exec_module(module)
    finally:
        builtins.input = old_input
        builtins.print = old_print

    text = "".join(outputs).replace("\r\n", "\n").replace("\r", "\n")
    return text


@pytest.mark.timeout(1)
def test_found_target_prints_exactly_found_target():
    out = _run_with_inputs(["java", "ruby", "python", "STOP"])
    expected = "Found target\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


@pytest.mark.timeout(1)
def test_not_found_prints_exactly_not_found():
    out = _run_with_inputs(["java", "ruby", "STOP"])
    expected = "Not found\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


@pytest.mark.timeout(1)
def test_target_before_stop_ignores_later_stop():
    out = _run_with_inputs(["python", "STOP"])
    expected = "Found target\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


@pytest.mark.timeout(1)
def test_stop_immediately_not_found():
    out = _run_with_inputs(["STOP"])
    expected = "Not found\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


@pytest.mark.timeout(1)
def test_output_is_single_line_only():
    out = _run_with_inputs(["java", "STOP"])
    expected = "Not found\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"