import importlib.util
import os
import re
import sys


def _load_module_from_filename(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    name = os.path.splitext(os.path.basename(filename))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_import_executes_and_prints_expected(capsys):
    _load_module_from_filename("12_frozenDataclassPoint.py")
    out = capsys.readouterr().out.strip().splitlines()

    assert len(out) == 2, f"expected={2!r} actual={len(out)!r}"
    assert out[0] == "Point(x=2, y=5)", f"expected={'Point(x=2, y=5)'!r} actual={out[0]!r}"
    assert out[1].startswith("mutate error:"), f"expected={'mutate error:'!r} actual={out[1][:12]!r}"

    m = re.fullmatch(r"mutate error:\s+([A-Za-z_][A-Za-z0-9_]*)", out[1])
    assert m is not None, f"expected={'mutate error: <ExceptionName>'!r} actual={out[1]!r}"
    assert m.group(1).endswith("FrozenInstanceError"), f"expected={'*FrozenInstanceError'!r} actual={m.group(1)!r}"


def test_point_is_frozen_dataclass_and_mutation_raises():
    mod = _load_module_from_filename("12_frozenDataclassPoint.py")

    assert hasattr(mod, "Point"), f"expected={True!r} actual={hasattr(mod, 'Point')!r}"
    Point = mod.Point

    assert hasattr(mod, "p"), f"expected={True!r} actual={hasattr(mod, 'p')!r}"
    p = mod.p

    assert isinstance(p, Point), f"expected={Point.__name__!r} actual={type(p).__name__!r}"
    assert getattr(p, "x") == 2, f"expected={2!r} actual={getattr(p, 'x')!r}"
    assert getattr(p, "y") == 5, f"expected={5!r} actual={getattr(p, 'y')!r}"

    assert getattr(Point, "__dataclass_params__", None) is not None, f"expected={'dataclass'!r} actual={getattr(Point, '__dataclass_params__', None)!r}"
    assert Point.__dataclass_params__.frozen is True, f"expected={True!r} actual={Point.__dataclass_params__.frozen!r}"

    try:
        p.x = 999
        raised = None
    except Exception as e:
        raised = e

    assert raised is not None, f"expected={'exception'!r} actual={None!r}"
    assert type(raised).__name__.endswith("FrozenInstanceError"), f"expected={'*FrozenInstanceError'!r} actual={type(raised).__name__!r}"


def test_point_repr_is_dataclass_style():
    mod = _load_module_from_filename("12_frozenDataclassPoint.py")
    p = mod.p
    assert repr(p) == "Point(x=2, y=5)", f"expected={'Point(x=2, y=5)'!r} actual={repr(p)!r}"