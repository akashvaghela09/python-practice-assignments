import importlib.util
import sys
from pathlib import Path


def _load_module():
    path = Path(__file__).resolve().parent / "08_copyingTuples.py"
    spec = importlib.util.spec_from_file_location("mod08_copyingTuples", str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_slice_copy_creates_same_object():
    mod = _load_module()
    assert hasattr(mod, "t")
    assert hasattr(mod, "t2")
    expected = True
    actual = (mod.t2 is mod.t)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_slice_copy_has_same_value():
    mod = _load_module()
    expected = True
    actual = (mod.t2 == mod.t)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_output_lines(capsys):
    _load_module()
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 2
    expected0 = "same object: True"
    expected1 = "same value: True"
    actual0 = out[0].strip()
    actual1 = out[1].strip()
    assert actual0 == expected0, f"expected={expected0} actual={actual0}"
    assert actual1 == expected1, f"expected={expected1} actual={actual1}"