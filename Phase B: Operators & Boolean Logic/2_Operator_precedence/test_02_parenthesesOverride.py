import importlib.util
import io
import os
import sys
import types
import pytest

FILE_NAME = "02_parenthesesOverride.py"


def load_module_from_path(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def run_file_capture_stdout(path):
    old_stdout = sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    try:
        g = {"__name__": "__main__", "__file__": path}
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
        exec(compile(code, path, "exec"), g, g)
    finally:
        sys.stdout = old_stdout
    return buf.getvalue()


@pytest.fixture(scope="module")
def assignment_path():
    here = os.path.dirname(__file__)
    return os.path.join(here, FILE_NAME)


def test_file_executes_without_placeholder(assignment_path):
    with open(assignment_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "__" not in content


def test_prints_expected_output_exactly(assignment_path):
    out = run_file_capture_stdout(assignment_path)
    expected = "20\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_result_value_is_20_on_import(assignment_path):
    module_name = "student_mod_02_parenthesesOverride"
    if module_name in sys.modules:
        del sys.modules[module_name]
    module = load_module_from_path(assignment_path, module_name)
    assert hasattr(module, "result")
    expected = 20
    actual = module.result
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_final_expression_uses_parentheses(assignment_path):
    with open(assignment_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    target_line = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("result") and "=" in stripped and "2 + 3 * 6" not in stripped and not stripped.startswith("#"):
            target_line = stripped
    assert target_line is not None

    rhs = target_line.split("=", 1)[1].strip()
    has_parens = ("(" in rhs) or (")" in rhs)
    expected = True
    actual = has_parens
    assert actual == expected, f"expected={expected!r} actual={actual!r}"