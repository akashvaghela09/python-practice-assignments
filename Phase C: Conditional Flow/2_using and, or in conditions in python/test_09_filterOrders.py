import importlib.util
import os
import sys


def _load_module_safely(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_expected_output_exact(capfd):
    file_path = os.path.join(os.path.dirname(__file__), "09_filterOrders.py")
    mod_name = "filterOrders09_run_output"

    _load_module_safely(mod_name, file_path)
    out, err = capfd.readouterr()

    expected = "MANUAL REVIEW COUNT: 3\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"
    assert err == "", f"expected={''!r} actual={err!r}"


def test_print_format_prefix(capfd):
    file_path = os.path.join(os.path.dirname(__file__), "09_filterOrders.py")
    mod_name = "filterOrders09_run_prefix"

    _load_module_safely(mod_name, file_path)
    out, _ = capfd.readouterr()

    assert out.startswith("MANUAL REVIEW COUNT: "), f"expected={'MANUAL REVIEW COUNT: '!r} actual={out[:20]!r}"


def test_syntax_is_valid_python():
    file_path = os.path.join(os.path.dirname(__file__), "09_filterOrders.py")
    with open(file_path, "r", encoding="utf-8") as f:
        src = f.read()
    try:
        compile(src, file_path, "exec")
    except SyntaxError as e:
        assert False, f"expected={'valid syntax'!r} actual={str(e)!r}"