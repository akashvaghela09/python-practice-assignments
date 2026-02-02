import importlib.util
import os
import sys


def _load_module():
    file_name = "10_deepCopyNestedList.py"
    module_name = "deepcopy_nested_list_mod_10"

    file_path = os.path.join(os.path.dirname(__file__), file_name)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_main_output_exact(capfd):
    mod = _load_module()
    mod.main()
    out = capfd.readouterr().out
    expected = "original: [[1, 2], [3, 4]]\ndeep: [[1, 99], [3, 4]]\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_deep_copy_prevents_original_mutation(capfd):
    mod = _load_module()
    mod.main()
    out = capfd.readouterr().out.strip().splitlines()
    assert len(out) == 2, f"expected={2!r} actual={len(out)!r}"

    expected_original_line = "original: [[1, 2], [3, 4]]"
    assert out[0] == expected_original_line, f"expected={expected_original_line!r} actual={out[0]!r}"

    assert out[1].startswith("deep: "), f"expected={'deep: ...'!r} actual={out[1]!r}"
    assert "99" in out[1], f"expected={'...99...'!r} actual={out[1]!r}"
    assert "[1, 99]" in out[1], f"expected={'...[1, 99]...'!r} actual={out[1]!r}"