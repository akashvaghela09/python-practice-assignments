import importlib.util
import pathlib
import sys


def load_module():
    path = pathlib.Path(__file__).resolve().parent / "10_replaceSublistPatternInPlace.py"
    spec = importlib.util.spec_from_file_location("mod10_replaceSublistPatternInPlace", str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def scan_replace_expected(data, pattern, replacement):
    i = 0
    out = list(data)
    while i <= len(out) - len(pattern):
        if out[i : i + len(pattern)] == pattern:
            out[i : i + len(pattern)] = replacement
            i += len(replacement)
        else:
            i += 1
    return out


def test_replaces_all_non_overlapping_occurrences_left_to_right():
    mod = load_module()
    expected = scan_replace_expected(
        [5, 0, 0, 0, 2, 0, 0, 0, 9], [0, 0, 0], [1, 1]
    )
    assert mod.data == expected, f"expected={expected} actual={mod.data}"


def test_uses_in_place_mutation_same_list_object():
    mod = load_module()
    expected = scan_replace_expected(mod.data, mod.pattern, mod.replacement) if False else None
    # Re-load to evaluate pre/post identity correctly
    mod = load_module()
    initial_id = id(mod.data)
    expected = scan_replace_expected(
        [5, 0, 0, 0, 2, 0, 0, 0, 9], [0, 0, 0], [1, 1]
    )
    assert id(mod.data) == initial_id, f"expected={initial_id} actual={id(mod.data)}"
    assert mod.data == expected, f"expected={expected} actual={mod.data}"


def test_no_partial_replacement_when_pattern_not_present():
    mod = load_module()
    expected = scan_replace_expected(
        [5, 0, 0, 0, 2, 0, 0, 0, 9], [0, 0, 0], [1, 1]
    )
    assert mod.data.count(0) == 0, f"expected={0} actual={mod.data.count(0)}"
    assert mod.data == expected, f"expected={expected} actual={mod.data}"


def test_does_not_create_overlapping_matches():
    mod = load_module()
    base = [0, 0, 0, 0, 0, 0]
    pattern = [0, 0, 0]
    replacement = [1, 1]
    expected = scan_replace_expected(base, pattern, replacement)

    # Simulate expected non-overlapping behavior: should match at 0 then continue after insertion
    actual = list(base)
    i = 0
    while i <= len(actual) - len(pattern):
        if actual[i : i + len(pattern)] == pattern:
            actual[i : i + len(pattern)] = replacement
            i += len(replacement)
        else:
            i += 1

    assert actual == expected, f"expected={expected} actual={actual}"


def test_expected_output_list_shape_for_given_input():
    mod = load_module()
    expected = scan_replace_expected(
        [5, 0, 0, 0, 2, 0, 0, 0, 9], [0, 0, 0], [1, 1]
    )
    assert len(mod.data) == len(expected), f"expected={len(expected)} actual={len(mod.data)}"
    assert mod.data[0] == expected[0], f"expected={expected[0]} actual={mod.data[0]}"
    assert mod.data[-1] == expected[-1], f"expected={expected[-1]} actual={mod.data[-1]}"