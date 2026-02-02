import importlib.util
import os
import sys


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _expected():
    A = {"a", "b", "c", "d"}
    B = {"c", "d", "e"}
    return A - B, A ^ B


def test_diff_and_symdiff_values():
    path = os.path.join(os.path.dirname(__file__), "07_differenceAndSymmetricDifference.py")
    mod = _load_module(path, "assignment_07_diff_sym")

    exp_diff, exp_sym = _expected()

    assert hasattr(mod, "diff"), f"expected=hasattr(diff) actual={hasattr(mod, 'diff')}"
    assert hasattr(mod, "sym"), f"expected=hasattr(sym) actual={hasattr(mod, 'sym')}"

    assert isinstance(mod.diff, set), f"expected=set actual={type(mod.diff).__name__}"
    assert isinstance(mod.sym, set), f"expected=set actual={type(mod.sym).__name__}"

    assert mod.diff == exp_diff, f"expected={exp_diff} actual={mod.diff}"
    assert mod.sym == exp_sym, f"expected={exp_sym} actual={mod.sym}"


def test_printed_output_includes_expected_sets(capsys):
    path = os.path.join(os.path.dirname(__file__), "07_differenceAndSymmetricDifference.py")
    _load_module(path, "assignment_07_diff_sym_print")
    out = capsys.readouterr().out.strip().splitlines()

    exp_diff, exp_sym = _expected()

    assert len(out) == 2, f"expected=2 actual={len(out)}"
    assert out[0].startswith("A-B:"), f"expected=A-B: actual={out[0].split(':')[0] + ':' if ':' in out[0] else out[0]}"
    assert out[1].startswith("symdiff:"), f"expected=symdiff: actual={out[1].split(':')[0] + ':' if ':' in out[1] else out[1]}"

    assert str(exp_diff) in out[0], f"expected={str(exp_diff)} actual={out[0]}"
    assert str(exp_sym) in out[1], f"expected={str(exp_sym)} actual={out[1]}"