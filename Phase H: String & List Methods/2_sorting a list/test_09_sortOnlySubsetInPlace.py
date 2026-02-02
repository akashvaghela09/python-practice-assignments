import importlib.util
import pathlib
import sys


def load_module_from_filename(filename):
    path = pathlib.Path(__file__).resolve().parent / filename
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return module


def test_middle_slice_sorted_only_subset_in_place(capsys):
    mod = load_module_from_filename("09_sortOnlySubsetInPlace.py")
    expected = [100, 50, 1, 2, 3, 4, 9, 8, 7]
    assert getattr(mod, "nums", None) == expected, f"expected {expected} got {getattr(mod, 'nums', None)}"


def test_ends_untouched_and_outside_segment_unchanged(capsys):
    mod = load_module_from_filename("09_sortOnlySubsetInPlace.py")
    nums = getattr(mod, "nums", None)
    original = [100, 50, 4, 3, 2, 1, 9, 8, 7]
    assert nums[0:2] == original[0:2], f"expected {original[0:2]} got {nums[0:2]}"
    assert nums[7:] == original[7:], f"expected {original[7:]} got {nums[7:]}"
    assert nums[6] == original[6], f"expected {original[6]} got {nums[6]}"


def test_only_requested_indices_sorted_ascending(capsys):
    mod = load_module_from_filename("09_sortOnlySubsetInPlace.py")
    nums = getattr(mod, "nums", None)
    start = getattr(mod, "start", None)
    end_inclusive = getattr(mod, "end_inclusive", None)
    assert start == 2, f"expected {2} got {start}"
    assert end_inclusive == 6, f"expected {6} got {end_inclusive}"
    segment = nums[start : end_inclusive + 1]
    expected_segment = sorted([4, 3, 2, 1, 9])
    assert segment == expected_segment, f"expected {expected_segment} got {segment}"


def test_prints_final_list(capsys):
    load_module_from_filename("09_sortOnlySubsetInPlace.py")
    out = capsys.readouterr().out.strip().splitlines()
    expected_line = str([100, 50, 1, 2, 3, 4, 9, 8, 7])
    actual_line = out[-1] if out else ""
    assert actual_line == expected_line, f"expected {expected_line} got {actual_line}"