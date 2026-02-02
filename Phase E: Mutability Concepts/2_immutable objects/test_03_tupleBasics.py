import importlib.util
import os
import re


def _load_module_capture_output():
    fname = "03_tupleBasics.py"
    path = os.path.join(os.path.dirname(__file__), fname)
    spec = importlib.util.spec_from_file_location("tuple_basics_mod", path)
    mod = importlib.util.module_from_spec(spec)

    import builtins
    printed = []

    original_print = builtins.print

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        s = sep.join(str(a) for a in args) + end
        printed.append(s.rstrip("\n"))

    builtins.print = fake_print
    try:
        spec.loader.exec_module(mod)
    finally:
        builtins.print = original_print

    return mod, printed


def _extract_kv(line, key):
    m = re.search(rf"\b{re.escape(key)}=([^\s]+)\b", line)
    if not m:
        return None
    return m.group(1)


def test_output_lines_expected():
    _, out = _load_module_capture_output()
    assert len(out) == 2, f"expected={2} actual={len(out)}"
    assert out[0] == "first=3 last=5", f"expected={'first=3 last=5'} actual={out[0]}"
    assert out[1] == "len=3", f"expected={'len=3'} actual={out[1]}"


def test_first_last_values_match_tuple_indices():
    mod, out = _load_module_capture_output()
    assert hasattr(mod, "nums"), "expected=attribute actual=missing"
    assert hasattr(mod, "first"), "expected=attribute actual=missing"
    assert hasattr(mod, "last"), "expected=attribute actual=missing"

    expected_first = mod.nums[0]
    expected_last = mod.nums[-1]
    assert mod.first == expected_first, f"expected={expected_first} actual={mod.first}"
    assert mod.last == expected_last, f"expected={expected_last} actual={mod.last}"

    first_s = _extract_kv(out[0], "first")
    last_s = _extract_kv(out[0], "last")
    assert first_s is not None, f"expected={'value'} actual={first_s}"
    assert last_s is not None, f"expected={'value'} actual={last_s}"
    assert int(first_s) == expected_first, f"expected={expected_first} actual={first_s}"
    assert int(last_s) == expected_last, f"expected={expected_last} actual={last_s}"


def test_length_n_matches_len_nums_and_output():
    mod, out = _load_module_capture_output()
    assert hasattr(mod, "n"), "expected=attribute actual=missing"
    expected_len = len(mod.nums)
    assert mod.n == expected_len, f"expected={expected_len} actual={mod.n}"

    n_s = _extract_kv(out[1], "len")
    assert n_s is not None, f"expected={'value'} actual={n_s}"
    assert int(n_s) == expected_len, f"expected={expected_len} actual={n_s}"


def test_nums_is_tuple_and_immutable():
    mod, _ = _load_module_capture_output()
    assert isinstance(mod.nums, tuple), f"expected={tuple} actual={type(mod.nums)}"
    try:
        mod.nums[0] = mod.nums[0]
        mutated = True
    except TypeError:
        mutated = False
    assert mutated is False, f"expected={False} actual={mutated}"