import importlib.util
import pathlib
import sys


def _load_module(capsys):
    module_name = "01_booleanLiteral"
    file_path = pathlib.Path(__file__).resolve().parent / "01_booleanLiteral.py"
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    with capsys.disabled():
        pass
    spec.loader.exec_module(module)
    return module


def test_is_active_is_true(capsys):
    module = _load_module(capsys)
    expected = True
    actual = getattr(module, "is_active", None)
    assert actual is expected, f"expected={expected!r} actual={actual!r}"


def test_prints_true(capsys):
    _load_module(capsys)
    out = capsys.readouterr().out
    expected = "True\n"
    actual = out
    assert actual == expected, f"expected={expected!r} actual={actual!r}"