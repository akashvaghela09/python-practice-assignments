import importlib.util
import os
import sys


def load_module():
    filename = "09_shallowCopyNestedList.py"
    module_name = "shallow_copy_nested_list_09"

    spec = importlib.util.spec_from_file_location(module_name, os.path.join(os.getcwd(), filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_main_output_exact(capsys):
    m = load_module()
    m.main()
    out = capsys.readouterr().out
    expected = "original: [[1, 99], [3, 4]]\nshallow: [[1, 99], [3, 4]]\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_main_output_two_lines_only(capsys):
    m = load_module()
    m.main()
    out = capsys.readouterr().out
    expected = "original: [[1, 99], [3, 4]]\nshallow: [[1, 99], [3, 4]]\n"
    assert out.count("\n") == expected.count("\n"), f"expected={expected.count(chr(10))} actual={out.count(chr(10))}"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_main_no_extra_whitespace(capsys):
    m = load_module()
    m.main()
    out = capsys.readouterr().out
    expected = "original: [[1, 99], [3, 4]]\nshallow: [[1, 99], [3, 4]]\n"
    assert out.strip("\n") == expected.strip("\n"), f"expected={expected.strip(chr(10))!r} actual={out.strip(chr(10))!r}"