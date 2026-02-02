import importlib.util
import pathlib
import sys
import pytest


def load_module():
    path = pathlib.Path(__file__).resolve().parent / "06_enumerateCountMatchesAtEvenIndices.py"
    spec = importlib.util.spec_from_file_location("mod06", str(path))
    module = importlib.util.module_from_spec(spec)
    return module, spec


def test_module_imports_and_has_required_names():
    module, spec = load_module()
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        pytest.fail(f"expected=module imports successfully actual={type(e).__name__}: {e}")

    for name in ["s", "vowels", "count"]:
        assert hasattr(module, name), f"expected={name} defined actual=missing"


def test_count_value_matches_spec_output():
    module, spec = load_module()
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        pytest.fail(f"expected=module imports successfully actual={type(e).__name__}: {e}")

    expected = 3
    actual = getattr(module, "count", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_count_computed_matches_reference_logic_from_module_data():
    module, spec = load_module()
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        pytest.fail(f"expected=module imports successfully actual={type(e).__name__}: {e}")

    s = module.s
    vowels = module.vowels
    expected = sum(1 for i, ch in enumerate(s) if i % 2 == 0 and ch in vowels)
    actual = module.count
    assert actual == expected, f"expected={expected} actual={actual}"


def test_printed_output_is_integer_line(capsys):
    module, spec = load_module()
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        pytest.fail(f"expected=module executes and prints output actual={type(e).__name__}: {e}")

    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 1, f"expected=1 line actual={len(out)}"
    line = out[0].strip()
    assert line.lstrip("-").isdigit(), f"expected=integer string actual={line!r}"
    expected = str(module.count)
    actual = line
    assert actual == expected, f"expected={expected} actual={actual}"


def test_uses_enumerate_in_source():
    path = pathlib.Path(__file__).resolve().parent / "06_enumerateCountMatchesAtEvenIndices.py"
    try:
        src = path.read_text(encoding="utf-8")
    except Exception as e:
        pytest.fail(f"expected=read source actual={type(e).__name__}: {e}")

    expected = True
    actual = "enumerate" in src
    assert actual == expected, f"expected={expected} actual={actual}"