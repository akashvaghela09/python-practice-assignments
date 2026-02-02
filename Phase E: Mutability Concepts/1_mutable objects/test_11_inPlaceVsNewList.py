import importlib.util
import os
import sys


def _load_module():
    filename = "11_inPlaceVsNewList.py"
    module_name = "inPlaceVsNewList_11"
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_main_output_exact(capsys):
    mod = _load_module()
    mod.main()
    out = capsys.readouterr().out
    expected = "same_object: True\nnums: [3, 1, 2]\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_main_prints_two_lines_only(capsys):
    mod = _load_module()
    mod.main()
    out = capsys.readouterr().out
    lines = [line for line in out.splitlines() if line != ""]
    expected_count = 2
    actual_count = len(lines)
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"


def test_main_has_required_prefixes(capsys):
    mod = _load_module()
    mod.main()
    out = capsys.readouterr().out
    lines = out.splitlines()
    expected_prefixes = ("same_object:", "nums:")
    actual_prefixes = (lines[0].split()[0] if lines else None, lines[1].split()[0] if len(lines) > 1 else None)
    assert actual_prefixes == expected_prefixes, f"expected={expected_prefixes!r} actual={actual_prefixes!r}"