import importlib.util
import os
import re


def _load_module_capture_stdout(module_filename):
    path = os.path.join(os.path.dirname(__file__), module_filename)
    spec = importlib.util.spec_from_file_location("student_mod", path)
    mod = importlib.util.module_from_spec(spec)

    import builtins

    printed = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        printed.append(sep.join(str(a) for a in args) + end)

    orig_print = builtins.print
    builtins.print = fake_print
    try:
        spec.loader.exec_module(mod)
    finally:
        builtins.print = orig_print

    out = "".join(printed)
    return mod, out


def _parse_list_line(out, key):
    m = re.search(rf"^{re.escape(key)}=(.*)$", out, flags=re.MULTILINE)
    if not m:
        return None, None
    raw = m.group(1).strip()
    try:
        val = eval(raw, {})
    except Exception:
        val = None
    return val, raw


def test_expected_stdout_lists():
    _, out = _load_module_capture_stdout("02_listSlicing.py")

    middle_val, middle_raw = _parse_list_line(out, "middle")
    last_two_val, last_two_raw = _parse_list_line(out, "last_two")

    exp_middle = ["b", "c", "d"]
    exp_last_two = ["e", "f"]

    assert middle_val == exp_middle, f"expected={exp_middle!r} actual={middle_raw!r}"
    assert last_two_val == exp_last_two, f"expected={exp_last_two!r} actual={last_two_raw!r}"


def test_variables_exist_and_are_lists():
    mod, _ = _load_module_capture_stdout("02_listSlicing.py")

    assert hasattr(mod, "letters"), "expected='letters' actual=missing"
    assert hasattr(mod, "middle"), "expected='middle' actual=missing"
    assert hasattr(mod, "last_two"), "expected='last_two' actual=missing"

    assert isinstance(mod.letters, list), f"expected={list} actual={type(mod.letters)}"
    assert isinstance(mod.middle, list), f"expected={list} actual={type(mod.middle)}"
    assert isinstance(mod.last_two, list), f"expected={list} actual={type(mod.last_two)}"


def test_slices_correct_and_do_not_modify_original():
    mod, _ = _load_module_capture_stdout("02_listSlicing.py")

    exp_letters = ["a", "b", "c", "d", "e", "f"]
    exp_middle = ["b", "c", "d"]
    exp_last_two = ["e", "f"]

    assert mod.letters == exp_letters, f"expected={exp_letters!r} actual={mod.letters!r}"
    assert mod.middle == exp_middle, f"expected={exp_middle!r} actual={mod.middle!r}"
    assert mod.last_two == exp_last_two, f"expected={exp_last_two!r} actual={mod.last_two!r}"

    assert mod.middle is not mod.letters, "expected=different_objects actual=same_object"
    assert mod.last_two is not mod.letters, "expected=different_objects actual=same_object"


def test_output_contains_only_required_lines_in_order():
    _, out = _load_module_capture_stdout("02_listSlicing.py")
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    expected_prefixes = ["middle=", "last_two="]

    actual_prefixes = []
    for ln in lines:
        if ln.startswith("middle="):
            actual_prefixes.append("middle=")
        elif ln.startswith("last_two="):
            actual_prefixes.append("last_two=")

    assert actual_prefixes == expected_prefixes, f"expected={expected_prefixes!r} actual={actual_prefixes!r}"