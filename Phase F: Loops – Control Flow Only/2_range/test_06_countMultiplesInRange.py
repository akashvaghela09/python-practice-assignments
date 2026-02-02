import importlib.util
import pathlib
import re

def _load_module():
    path = pathlib.Path(__file__).resolve().parent / "06_countMultiplesInRange.py"
    spec = importlib.util.spec_from_file_location("countMultiplesInRange06", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_counts_multiples_of_3_inclusive_1_to_30(capsys):
    module = _load_module()
    out = capsys.readouterr().out.strip()
    assert hasattr(module, "count")
    assert isinstance(module.count, int)

    expected = 0
    for n in range(1, 31):
        if n % 3 == 0:
            expected += 1

    assert module.count == expected, f"expected={expected} actual={module.count}"

    m = re.search(r"-?\d+", out)
    actual_printed = int(m.group(0)) if m else None
    assert actual_printed == expected, f"expected={expected} actual={actual_printed}"

def test_no_list_comprehensions_used():
    path = pathlib.Path(__file__).resolve().parent / "06_countMultiplesInRange.py"
    text = path.read_text(encoding="utf-8")
    assert "[" not in text, "expected=no_list_comp actual=bracket_found"
    assert " for " not in text or "[" not in text, "expected=no_list_comp actual=list_comp_like_found"

def test_uses_range_and_for_loop():
    path = pathlib.Path(__file__).resolve().parent / "06_countMultiplesInRange.py"
    text = path.read_text(encoding="utf-8")
    has_for = re.search(r"^\s*for\s+\w+\s+in\s+range\s*\(", text, flags=re.M) is not None
    has_range = "range(" in text
    assert has_for and has_range, f"expected={True} actual={has_for and has_range}"