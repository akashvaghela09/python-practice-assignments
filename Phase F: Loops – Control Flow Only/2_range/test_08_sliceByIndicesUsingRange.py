import importlib.util
import io
import os
import contextlib
import ast
import pytest

MODULE_FILE = "08_sliceByIndicesUsingRange.py"


def load_module():
    spec = importlib.util.spec_from_file_location("m08_sliceByIndicesUsingRange", MODULE_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_script_capture_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        load_module()
    return buf.getvalue()


def parse_last_list_from_output(output: str):
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
    if not lines:
        raise AssertionError("No output captured")
    last = lines[-1]
    try:
        val = ast.literal_eval(last)
    except Exception as e:
        raise AssertionError(f"expected: valid Python literal list, actual: {last!r}") from e
    if not isinstance(val, list):
        raise AssertionError(f"expected: list, actual: {type(val).__name__}")
    return val


def test_runs_without_placeholder_syntax_error():
    src = open(MODULE_FILE, "r", encoding="utf-8").read()
    try:
        compile(src, MODULE_FILE, "exec")
    except SyntaxError as e:
        pytest.fail(f"expected: no syntax error, actual: {e.msg}")


def test_stdout_is_expected_list():
    output = run_script_capture_stdout()
    result_list = parse_last_list_from_output(output)
    expected = [10, 12, 14, 16]
    assert result_list == expected, f"expected: {expected!r}, actual: {result_list!r}"


def test_result_variable_is_correct_when_imported():
    module = load_module()
    assert hasattr(module, "result"), "expected: result variable, actual: missing"
    expected = [10, 12, 14, 16]
    actual = module.result
    assert actual == expected, f"expected: {expected!r}, actual: {actual!r}"


def test_uses_range_with_three_arguments_and_step_two():
    src = open(MODULE_FILE, "r", encoding="utf-8").read()
    tree = ast.parse(src)

    range_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "range":
            range_calls.append(node)

    assert range_calls, "expected: range(...) call, actual: none found"

    found_three_args = False
    found_step_two = False

    for call in range_calls:
        if len(call.args) == 3:
            found_three_args = True
            step = call.args[2]
            if isinstance(step, ast.Constant) and step.value == 2:
                found_step_two = True

    assert found_three_args, "expected: range with 3 args, actual: not found"
    assert found_step_two, "expected: step of 2, actual: different"


def test_uses_append_in_loop():
    src = open(MODULE_FILE, "r", encoding="utf-8").read()
    tree = ast.parse(src)

    loop_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.For)]
    assert loop_nodes, "expected: for-loop, actual: none found"

    has_append = False
    for for_node in loop_nodes:
        for n in ast.walk(for_node):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "append":
                if isinstance(n.func.value, ast.Name) and n.func.value.id == "result":
                    has_append = True
                    break
        if has_append:
            break

    assert has_append, "expected: result.append(...) in loop, actual: not found"