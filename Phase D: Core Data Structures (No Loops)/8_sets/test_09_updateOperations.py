import importlib.util
import pathlib
import sys
import types
import pytest


def _load_module_from_path(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_output_sets_after_updates(capsys):
    target = pathlib.Path(__file__).resolve().parent / "09_updateOperations.py"
    module_name = "update_ops_09_tested"

    if module_name in sys.modules:
        del sys.modules[module_name]

    _load_module_from_path(module_name, target)

    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 2, f"expected={2!r} actual={len(out)!r}"

    ns = {}
    exec("a=" + out[0] + "\n" + "b=" + out[1], {}, ns)

    a = ns["a"]
    b = ns["b"]

    assert isinstance(a, set), f"expected={set!r} actual={type(a)!r}"
    assert isinstance(b, set), f"expected={set!r} actual={type(b)!r}"

    assert a == {1, 2, 3, 4, 5}, f"expected={ {1,2,3,4,5}!r } actual={a!r}"
    assert b == {3, 4, 5}, f"expected={ {3,4,5}!r } actual={b!r}"


def test_uses_in_place_update_operations():
    target = pathlib.Path(__file__).resolve().parent / "09_updateOperations.py"
    text = target.read_text(encoding="utf-8")

    has_update = (".update(" in text) or ("|=" in text)
    has_intersection_update = (".intersection_update(" in text) or ("&=" in text)

    assert has_update, f"expected={True!r} actual={has_update!r}"
    assert has_intersection_update, f"expected={True!r} actual={has_intersection_update!r}"