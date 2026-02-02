import importlib.util
import os
import sys
import types
import pytest


def _load_module_no_stdout(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _expected_most_frequent_non_space(s: str):
    counts = {}
    for ch in s:
        if ch == " ":
            continue
        counts[ch] = counts.get(ch, 0) + 1
    if not counts:
        return None
    max_count = max(counts.values())
    candidates = [ch for ch, c in counts.items() if c == max_count]
    return sorted(candidates)[0]


@pytest.fixture(scope="module")
def mod():
    fname = "14_findMostFrequentChar.py"
    file_path = os.path.join(os.path.dirname(__file__), fname)
    module_name = "findMostFrequentChar_14_testmod"
    return module_name, file_path


def test_script_runs_without_error_and_prints_one_line(mod, capsys):
    module_name, file_path = mod
    try:
        _load_module_no_stdout(module_name, file_path)
    except Exception as e:
        pytest.fail(f"{type(e).__name__}: {e}")
    out = capsys.readouterr().out
    lines = [ln for ln in out.splitlines() if ln.strip() != "" or ln == ""]
    assert len(lines) == 1, f"expected one printed line, actual={len(lines)}"


def test_printed_value_matches_expected_for_given_string(mod, capsys):
    module_name, file_path = mod
    _load_module_no_stdout(module_name, file_path)
    out = capsys.readouterr().out
    printed = out.splitlines()[0].strip()
    m = _load_module_no_stdout(module_name + "_reload", file_path)
    assert hasattr(m, "s"), "expected s to exist"
    expected = _expected_most_frequent_non_space(m.s)
    expected_str = "None" if expected is None else str(expected)
    assert printed == expected_str, f"expected={expected_str} actual={printed}"


def test_most_common_variable_exists_and_matches_expected(mod, capsys):
    module_name, file_path = mod
    m = _load_module_no_stdout(module_name + "_varcheck", file_path)
    _ = capsys.readouterr()
    assert hasattr(m, "most_common"), "expected most_common to exist"
    assert hasattr(m, "s"), "expected s to exist"
    expected = _expected_most_frequent_non_space(m.s)
    actual = m.most_common
    assert actual == expected, f"expected={expected} actual={actual}"


def test_counts_is_dict_and_matches_expected_counts(mod, capsys):
    module_name, file_path = mod
    m = _load_module_no_stdout(module_name + "_countcheck", file_path)
    _ = capsys.readouterr()
    assert hasattr(m, "counts"), "expected counts to exist"
    assert isinstance(m.counts, dict), f"expected=dict actual={type(m.counts)}"
    assert hasattr(m, "s"), "expected s to exist"

    expected_counts = {}
    for ch in m.s:
        if ch == " ":
            continue
        expected_counts[ch] = expected_counts.get(ch, 0) + 1

    assert m.counts == expected_counts, f"expected={expected_counts} actual={m.counts}"