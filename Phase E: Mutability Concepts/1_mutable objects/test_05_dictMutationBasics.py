import importlib.util
import os
import ast
import pytest

FILE_NAME = "05_dictMutationBasics.py"


def load_module():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    spec = importlib.util.spec_from_file_location("dict_mutation_basics_05", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, path


def run_main_capture(module, capsys):
    module.main()
    out = capsys.readouterr().out
    return out


def test_main_prints_exact_dictionary(capsys):
    module, _ = load_module()
    out = run_main_capture(module, capsys)
    expected = "{'name': 'Ada', 'age': 37}\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_temp_key_in_final_output(capsys):
    module, _ = load_module()
    out = run_main_capture(module, capsys)
    assert "temp" not in out, f"expected={'temp not present'!r} actual={out!r}"


def test_output_is_single_line(capsys):
    module, _ = load_module()
    out = run_main_capture(module, capsys)
    lines = out.splitlines(True)
    expected_count = 1
    actual_count = len(lines)
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"


def test_parsed_output_has_expected_keys_and_values(capsys):
    module, _ = load_module()
    out = run_main_capture(module, capsys)
    s = out.strip()
    parsed = ast.literal_eval(s)
    assert isinstance(parsed, dict), f"expected={'dict'!r} actual={type(parsed).__name__!r}"
    expected_keys = {"name", "age"}
    actual_keys = set(parsed.keys())
    assert actual_keys == expected_keys, f"expected={sorted(expected_keys)!r} actual={sorted(actual_keys)!r}"
    expected_name = "Ada"
    expected_age = 37
    assert parsed.get("name") == expected_name, f"expected={expected_name!r} actual={parsed.get('name')!r}"
    assert parsed.get("age") == expected_age, f"expected={expected_age!r} actual={parsed.get('age')!r}"


def test_has_main_function_defined():
    module, _ = load_module()
    assert hasattr(module, "main"), f"expected={'main exists'!r} actual={hasattr(module, 'main')!r}"
    assert callable(module.main), f"expected={'callable'!r} actual={type(module.main).__name__!r}"