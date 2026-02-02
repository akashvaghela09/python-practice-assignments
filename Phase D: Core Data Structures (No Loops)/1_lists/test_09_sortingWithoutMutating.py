import importlib.util
import os
import sys


def _load_module():
    filename = "09_sortingWithoutMutating.py"
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("sortingWithoutMutating_09", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_sorted_scores_is_list_and_descending():
    mod = _load_module()
    assert isinstance(mod.sorted_scores, list), f"expected list, got {type(mod.sorted_scores)}"
    assert mod.sorted_scores == sorted(mod.scores, reverse=True), f"expected {sorted(mod.scores, reverse=True)}, got {mod.sorted_scores}"


def test_original_scores_unchanged_and_not_aliased():
    mod = _load_module()
    expected_original = [50, 20, 40, 10, 30]
    assert mod.scores == expected_original, f"expected {expected_original}, got {mod.scores}"
    assert mod.sorted_scores is not mod.scores, f"expected different objects, got same object"


def test_sorted_scores_is_permutation_of_original():
    mod = _load_module()
    assert sorted(mod.sorted_scores) == sorted(mod.scores), f"expected {sorted(mod.scores)}, got {sorted(mod.sorted_scores)}"


def test_print_output_matches_expected(capsys):
    mod = _load_module()
    captured = capsys.readouterr().out.strip().splitlines()
    expected_lines = [
        f"original: {mod.scores}",
        f"sorted: {mod.sorted_scores}",
    ]
    assert captured == expected_lines, f"expected {expected_lines}, got {captured}"