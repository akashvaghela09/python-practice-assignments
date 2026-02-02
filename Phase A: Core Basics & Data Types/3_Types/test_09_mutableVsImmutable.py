import importlib.util
import os
import sys


def _load_module(path, name="mod09_mutableVsImmutable"):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_output_lines(capsys):
    path = os.path.join(os.path.dirname(__file__), "09_mutableVsImmutable.py")
    _load_module(path, name="mod09_output_check")
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 2
    assert out[0] == "True", f"expected {'True'} vs actual {out[0]!r}"
    assert out[1] == "False", f"expected {'False'} vs actual {out[1]!r}"


def test_list_mutation_keeps_identity_and_tuple_changes_identity():
    path = os.path.join(os.path.dirname(__file__), "09_mutableVsImmutable.py")
    mod = _load_module(path, name="mod09_state_check")

    assert getattr(mod, "nums_list", None) == [1, 2, 3, 4]
    assert getattr(mod, "nums_tuple", None) == (1, 2, 3, 4)

    list_before = getattr(mod, "list_id_before", None)
    list_after = getattr(mod, "list_id_after", None)
    tuple_before = getattr(mod, "tuple_id_before", None)
    tuple_after = getattr(mod, "tuple_id_after", None)

    assert list_before == list_after, f"expected {list_before!r} vs actual {list_after!r}"
    assert tuple_before != tuple_after, f"expected {tuple_before!r} vs actual {tuple_after!r}"