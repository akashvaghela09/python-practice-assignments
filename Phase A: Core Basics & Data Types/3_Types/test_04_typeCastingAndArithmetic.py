import importlib.util
import io
import os
import sys


def _run_script(path):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        spec = importlib.util.spec_from_file_location("target_module_04", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    return module, output


def test_script_prints_expected_output():
    path = os.path.join(os.path.dirname(__file__), "04_typeCastingAndArithmetic.py")
    module, output = _run_script(path)
    expected = "26\n"
    assert output == expected, f"expected={expected!r} actual={output!r}"


def test_result_variable_is_int_and_correct():
    path = os.path.join(os.path.dirname(__file__), "04_typeCastingAndArithmetic.py")
    module, _ = _run_script(path)
    expected_value = 26
    assert hasattr(module, "result"), f"expected={True!r} actual={hasattr(module, 'result')!r}"
    assert isinstance(module.result, int), f"expected={int!r} actual={type(module.result)!r}"
    assert module.result == expected_value, f"expected={expected_value!r} actual={module.result!r}"


def test_source_does_not_use_eval_for_conversion():
    path = os.path.join(os.path.dirname(__file__), "04_typeCastingAndArithmetic.py")
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    expected = False
    actual = "eval(" in src
    assert actual == expected, f"expected={expected!r} actual={actual!r}"