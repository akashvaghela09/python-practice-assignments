import ast
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout

EXPECTED_LIST = [1, 2, 4, 5, 7, 8, 10, 11, 13, 14]


def load_module_from_filename(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("student_module_04", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)
    return module, buf.getvalue(), path


def parse_last_list_from_stdout(stdout):
    lines = [ln.strip() for ln in stdout.splitlines() if ln.strip()]
    if not lines:
        return None
    last = lines[-1]
    try:
        val = ast.literal_eval(last)
    except Exception:
        return None
    return val


def test_result_variable_matches_expected_list():
    module, stdout, _ = load_module_from_filename("04_skipDivisibleBy3.py")
    assert hasattr(module, "result"), "missing result variable"
    actual = module.result
    assert actual == EXPECTED_LIST, f"expected={EXPECTED_LIST} actual={actual}"


def test_printed_output_matches_expected_list_only():
    module, stdout, _ = load_module_from_filename("04_skipDivisibleBy3.py")
    actual_printed = parse_last_list_from_stdout(stdout)
    assert actual_printed == EXPECTED_LIST, f"expected={EXPECTED_LIST} actual={actual_printed}"


def test_result_contains_no_multiples_of_three_and_within_range():
    module, stdout, _ = load_module_from_filename("04_skipDivisibleBy3.py")
    actual = module.result
    multiples = [n for n in actual if isinstance(n, int) and n % 3 == 0]
    assert multiples == [], f"expected={[]} actual={multiples}"
    out_of_range = [n for n in actual if not isinstance(n, int) or n < 1 or n > 15]
    assert out_of_range == [], f"expected={[]} actual={out_of_range}"


def test_uses_continue_in_for_loop():
    _, _, path = load_module_from_filename("04_skipDivisibleBy3.py")
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    for_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.For)]
    assert len(for_nodes) >= 1, f"expected={True} actual={False}"
    continue_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.Continue)]
    assert len(continue_nodes) >= 1, f"expected={True} actual={False}"