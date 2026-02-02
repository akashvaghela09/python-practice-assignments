import ast
import importlib.util
import os
import sys
from contextlib import redirect_stdout
from io import StringIO


def _load_module():
    filename = "06_sortListOfTuples.py"
    module_name = "assignment_06_sortListOfTuples"
    path = os.path.join(os.path.dirname(__file__), filename)

    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod

    buf = StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(mod)
    out = buf.getvalue().strip()
    return mod, out


def _parse_printed_results(stdout_text):
    if not stdout_text:
        raise AssertionError(f"expected printed list, got {stdout_text!r}")
    try:
        value = ast.literal_eval(stdout_text.splitlines()[-1].strip())
    except Exception:
        raise AssertionError(f"expected parsable printed list, got {stdout_text!r}")
    return value


def test_results_sorted_descending_stable_and_inplace():
    mod, out = _load_module()

    original = [('Ava', 88), ('Ben', 75), ('Cara', 99), ('Dan', 75)]
    expected = [('Cara', 99), ('Ava', 88), ('Ben', 75), ('Dan', 75)]

    assert hasattr(mod, "results"), "missing results variable"
    assert isinstance(mod.results, list), f"expected list, got {type(mod.results).__name__}"

    actual = mod.results
    assert actual == expected, f"expected {expected!r}, got {actual!r}"

    printed = _parse_printed_results(out)
    assert printed == expected, f"expected {expected!r}, got {printed!r}"

    # Stable order among ties: Ben must remain before Dan for score 75
    tie_names = [name for name, score in actual if score == 75]
    expected_tie_names = ["Ben", "Dan"]
    assert tie_names == expected_tie_names, f"expected {expected_tie_names!r}, got {tie_names!r}"

    # Ensure it is a permutation of original elements
    assert sorted(actual) == sorted(original), f"expected {sorted(original)!r}, got {sorted(actual)!r}"


def test_no_additional_elements_or_structure_changes():
    mod, _ = _load_module()
    actual = mod.results

    assert all(isinstance(t, tuple) and len(t) == 2 for t in actual), f"expected list of 2-tuples, got {actual!r}"
    assert all(isinstance(t[0], str) and isinstance(t[1], int) for t in actual), f"expected (str,int) tuples, got {actual!r}"

    names = [t[0] for t in actual]
    scores = [t[1] for t in actual]
    expected_names = ["Cara", "Ava", "Ben", "Dan"]
    expected_scores = [99, 88, 75, 75]
    assert names == expected_names, f"expected {expected_names!r}, got {names!r}"
    assert scores == expected_scores, f"expected {expected_scores!r}, got {scores!r}"