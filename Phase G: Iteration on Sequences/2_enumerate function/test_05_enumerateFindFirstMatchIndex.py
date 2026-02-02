import importlib.util
import os
import sys


def _load_module_and_capture_output():
    fname = "05_enumerateFindFirstMatchIndex.py"
    path = os.path.join(os.path.dirname(__file__), fname)
    spec = importlib.util.spec_from_file_location("assignment_mod_05", path)
    mod = importlib.util.module_from_spec(spec)

    captured = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        captured.append(sep.join(str(a) for a in args) + end)

    mod.__dict__["print"] = fake_print
    spec.loader.exec_module(mod)
    out = "".join(captured).strip()
    return mod, out


def test_outputs_single_integer_line():
    mod, out = _load_module_and_capture_output()
    assert out != "", f"expected non-empty output, got {out!r}"
    lines = out.splitlines()
    assert len(lines) == 1, f"expected 1 line, got {len(lines)}"
    s = lines[0].strip()
    assert s.lstrip("-").isdigit(), f"expected integer output, got {s!r}"


def test_found_index_matches_printed_value():
    mod, out = _load_module_and_capture_output()
    printed = int(out.splitlines()[0].strip())
    assert hasattr(mod, "found_index"), f"expected attribute 'found_index', got {dir(mod)}"
    assert mod.found_index == printed, f"expected {mod.found_index!r}, got {printed!r}"


def test_first_match_index_is_correct_for_given_data():
    mod, out = _load_module_and_capture_output()
    expected = next(i for i, v in enumerate(mod.nums) if v == mod.target)
    actual = int(out.splitlines()[0].strip())
    assert actual == expected, f"expected {expected!r}, got {actual!r}"
    assert mod.found_index == expected, f"expected {expected!r}, got {mod.found_index!r}"


def test_first_match_property_holds():
    mod, out = _load_module_and_capture_output()
    idx = int(out.splitlines()[0].strip())
    assert 0 <= idx < len(mod.nums), f"expected in-range index, got {idx!r}"
    assert mod.nums[idx] == mod.target, f"expected {mod.target!r}, got {mod.nums[idx]!r}"
    prior = [i for i, v in enumerate(mod.nums[:idx]) if v == mod.target]
    assert prior == [], f"expected {[]!r}, got {prior!r}"


def test_implementation_uses_enumerate_and_stops():
    fname = "05_enumerateFindFirstMatchIndex.py"
    path = os.path.join(os.path.dirname(__file__), fname)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    assert "enumerate" in src, f"expected {'enumerate'!r}, got {('enumerate' in src)!r}"
    assert "break" in src, f"expected {'break'!r}, got {('break' in src)!r}"