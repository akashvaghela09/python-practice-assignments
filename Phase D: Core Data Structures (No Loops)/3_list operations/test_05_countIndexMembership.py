import importlib.util
import pathlib
import sys
import re
import pytest

MODULE_FILE = pathlib.Path(__file__).with_name("05_countIndexMembership.py")


def load_module():
    spec = importlib.util.spec_from_file_location("mod05_countIndexMembership", MODULE_FILE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_module_executes_without_error(capsys):
    try:
        load_module()
    except SyntaxError as e:
        pytest.fail(f"expected=module runs without SyntaxError actual={e}")
    except Exception as e:
        pytest.fail(f"expected=module runs without exception actual={type(e).__name__}: {e}")
    out = capsys.readouterr().out
    assert isinstance(out, str)


def test_printed_output_format_and_values(capsys):
    load_module()
    out = capsys.readouterr().out.strip().splitlines()

    assert len(out) == 3, f"expected=3 lines actual={len(out)}"
    assert out[0].startswith("count_a="), f"expected=prefix count_a= actual={out[0]}"
    assert out[1].startswith("first_a_index="), f"expected=prefix first_a_index= actual={out[1]}"
    assert out[2].startswith("has_z="), f"expected=prefix has_z= actual={out[2]}"

    m1 = re.fullmatch(r"count_a=(-?\d+)", out[0])
    m2 = re.fullmatch(r"first_a_index=(-?\d+)", out[1])
    m3 = re.fullmatch(r"has_z=(True|False)", out[2])

    assert m1 is not None, f"expected=integer format actual={out[0]}"
    assert m2 is not None, f"expected=integer format actual={out[1]}"
    assert m3 is not None, f"expected=boolean format actual={out[2]}"

    expected_chars = ["a", "b", "a", "c", "a"]
    expected_count_a = expected_chars.count("a")
    expected_first_idx = expected_chars.index("a")
    expected_has_z = "z" in expected_chars

    actual_count_a = int(m1.group(1))
    actual_first_idx = int(m2.group(1))
    actual_has_z = (m3.group(1) == "True")

    assert actual_count_a == expected_count_a, f"expected={expected_count_a} actual={actual_count_a}"
    assert actual_first_idx == expected_first_idx, f"expected={expected_first_idx} actual={actual_first_idx}"
    assert actual_has_z == expected_has_z, f"expected={expected_has_z} actual={actual_has_z}"


def test_variables_exist_and_match_computed_values():
    mod = load_module()

    assert hasattr(mod, "chars"), "expected=chars variable actual=missing"
    assert hasattr(mod, "count_a"), "expected=count_a variable actual=missing"
    assert hasattr(mod, "first_a_index"), "expected=first_a_index variable actual=missing"
    assert hasattr(mod, "has_z"), "expected=has_z variable actual=missing"

    expected_count_a = mod.chars.count("a")
    expected_first_idx = mod.chars.index("a")
    expected_has_z = ("z" in mod.chars)

    assert mod.count_a == expected_count_a, f"expected={expected_count_a} actual={mod.count_a}"
    assert mod.first_a_index == expected_first_idx, f"expected={expected_first_idx} actual={mod.first_a_index}"
    assert mod.has_z == expected_has_z, f"expected={expected_has_z} actual={mod.has_z}"