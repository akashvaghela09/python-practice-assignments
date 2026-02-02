import importlib.util
import pathlib
import ast
import re


def _load_module(path):
    spec = importlib.util.spec_from_file_location("mod_05_removeAndPop", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_as_script(path):
    import runpy
    return runpy.run_path(str(path))


def _parse_output(capsys):
    out = capsys.readouterr().out.strip().splitlines()
    removed = None
    remaining = None

    for line in out:
        m1 = re.match(r"^\s*removed:\s*(.+?)\s*$", line)
        if m1:
            try:
                removed = ast.literal_eval(m1.group(1))
            except Exception:
                removed = m1.group(1)
            continue
        m2 = re.match(r"^\s*remaining:\s*(.+?)\s*$", line)
        if m2:
            try:
                remaining = ast.literal_eval(m2.group(1))
            except Exception:
                remaining = m2.group(1)
            continue
    return removed, remaining, out


def test_stdout_removed_and_remaining(capsys):
    path = pathlib.Path(__file__).resolve().parent / "05_removeAndPop.py"
    _run_as_script(path)
    removed, remaining, _ = _parse_output(capsys)

    exp_removed = 3
    exp_remaining = [1, 2, 4]

    assert removed == exp_removed, f"expected {exp_removed!r} got {removed!r}"
    assert remaining == exp_remaining, f"expected {exp_remaining!r} got {remaining!r}"


def test_module_state_removed_and_nums(capsys):
    path = pathlib.Path(__file__).resolve().parent / "05_removeAndPop.py"
    mod = _load_module(path)
    _ = capsys.readouterr()

    exp_removed = 3
    exp_nums = [1, 2, 4]

    assert hasattr(mod, "removed"), "expected attribute missing"
    assert hasattr(mod, "nums"), "expected attribute missing"
    assert mod.removed == exp_removed, f"expected {exp_removed!r} got {mod.removed!r}"
    assert mod.nums == exp_nums, f"expected {exp_nums!r} got {mod.nums!r}"


def test_removed_is_int_and_nums_is_list():
    path = pathlib.Path(__file__).resolve().parent / "05_removeAndPop.py"
    mod = _load_module(path)

    assert isinstance(mod.removed, int), f"expected {int!r} got {type(mod.removed)!r}"
    assert isinstance(mod.nums, list), f"expected {list!r} got {type(mod.nums)!r}"


def test_only_first_three_removed_not_all():
    path = pathlib.Path(__file__).resolve().parent / "05_removeAndPop.py"
    mod = _load_module(path)

    exp_contains_three = False
    actual_contains_three = 3 in mod.nums
    assert actual_contains_three == exp_contains_three, f"expected {exp_contains_three!r} got {actual_contains_three!r}"


def test_no_extra_output_lines(capsys):
    path = pathlib.Path(__file__).resolve().parent / "05_removeAndPop.py"
    _run_as_script(path)
    _, _, lines = _parse_output(capsys)

    exp_lines = 2
    actual_lines = sum(1 for ln in lines if ln.strip() != "")
    assert actual_lines == exp_lines, f"expected {exp_lines!r} got {actual_lines!r}"