import ast
import importlib.util
import sys
from pathlib import Path


def _load_module(tmp_path, monkeypatch):
    src = Path("15_groupConsecutiveRuns.py")
    dst = tmp_path / "15_groupConsecutiveRuns.py"
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    monkeypatch.syspath_prepend(str(tmp_path))
    spec = importlib.util.spec_from_file_location("15_groupConsecutiveRuns", str(dst))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["15_groupConsecutiveRuns"] = mod
    spec.loader.exec_module(mod)
    return mod, dst


def _expected_runs(nums):
    runs = []
    cur = []
    for n in nums:
        if not cur or n == cur[-1]:
            cur.append(n)
        else:
            runs.append(cur)
            cur = [n]
    if cur:
        runs.append(cur)
    return runs


def test_printed_output_matches_expected_runs(capsys, tmp_path, monkeypatch):
    mod, _ = _load_module(tmp_path, monkeypatch)
    captured = capsys.readouterr()
    out = captured.out.strip()
    printed = ast.literal_eval(out)

    expected = _expected_runs(getattr(mod, "nums"))
    assert printed == expected, f"expected={expected} actual={printed}"


def test_runs_variable_exists_and_correct(capsys, tmp_path, monkeypatch):
    mod, _ = _load_module(tmp_path, monkeypatch)
    _ = capsys.readouterr()

    expected = _expected_runs(mod.nums)
    actual = getattr(mod, "runs")
    assert actual == expected, f"expected={expected} actual={actual}"


def test_runs_is_list_of_lists_and_preserves_elements(capsys, tmp_path, monkeypatch):
    mod, _ = _load_module(tmp_path, monkeypatch)
    _ = capsys.readouterr()

    runs = mod.runs
    assert isinstance(runs, list), f"expected={list} actual={type(runs)}"
    assert all(isinstance(r, list) for r in runs), f"expected={True} actual={all(isinstance(r, list) for r in runs)}"

    flattened = [x for r in runs for x in r]
    assert flattened == mod.nums, f"expected={mod.nums} actual={flattened}"

    for r in runs:
        if r:
            assert all(x == r[0] for x in r), f"expected={True} actual={all(x == r[0] for x in r)}"


def test_edge_transitions_count_matches_change_points(capsys, tmp_path, monkeypatch):
    mod, _ = _load_module(tmp_path, monkeypatch)
    _ = capsys.readouterr()

    nums = mod.nums
    expected_runs_count = 0
    if nums:
        expected_runs_count = 1 + sum(1 for i in range(1, len(nums)) if nums[i] != nums[i - 1])

    actual_runs_count = len(mod.runs)
    assert actual_runs_count == expected_runs_count, f"expected={expected_runs_count} actual={actual_runs_count}"