import importlib.util
import os
import sys
import pytest


def _load_module():
    filename = "04_popAndUseReturnedValue.py"
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("mod_04_popAndUseReturnedValue", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_removed_variable_exists_and_value():
    mod = _load_module()
    assert hasattr(mod, "removed"), f"expected removed to exist, actual missing"
    assert mod.removed == 200, f"expected {200!r}, actual {mod.removed!r}"


def test_data_list_updated_correctly():
    mod = _load_module()
    assert hasattr(mod, "data"), f"expected data to exist, actual missing"
    assert mod.data == [100, 300, 400], f"expected {[100, 300, 400]!r}, actual {mod.data!r}"


def test_removed_is_not_still_in_data():
    mod = _load_module()
    assert mod.removed not in mod.data, f"expected {mod.removed!r}, actual {mod.data!r}"


def test_stdout_format(capsys):
    _load_module()
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 2, f"expected {2!r}, actual {len(out)!r}"
    assert out[0].strip() == "removed: 200", f"expected {'removed: 200'!r}, actual {out[0].strip()!r}"
    assert out[1].strip() == "data: [100, 300, 400]", f"expected {'data: [100, 300, 400]'!r}, actual {out[1].strip()!r}"