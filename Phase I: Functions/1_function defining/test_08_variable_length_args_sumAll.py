import importlib
import re
import sys
import pytest

MODULE_NAME = "08_variable_length_args_sumAll"


def _load_module(monkeypatch):
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    return importlib.import_module(MODULE_NAME)


def test_stdout_exact(monkeypatch, capsys):
    _load_module(monkeypatch)
    out = capsys.readouterr().out
    assert out == "10\n0\n", f"expected={repr('10\\n0\\n')} actual={repr(out)}"


def test_sum_all_exists_and_callable(monkeypatch, capsys):
    mod = _load_module(monkeypatch)
    capsys.readouterr()
    assert hasattr(mod, "sum_all"), f"expected={True} actual={hasattr(mod, 'sum_all')}"
    assert callable(getattr(mod, "sum_all", None)), f"expected={True} actual={callable(getattr(mod, 'sum_all', None))}"


@pytest.mark.parametrize(
    "args, expected",
    [
        ((), 0),
        ((0,), 0),
        ((1,), 1),
        ((1, 2, 3, 4), 10),
        ((-1, -2, -3), -6),
        ((-10, 20, -5), 5),
        ((1000000, 2, 3), 1000005),
    ],
)
def test_sum_all_various(monkeypatch, capsys, args, expected):
    mod = _load_module(monkeypatch)
    capsys.readouterr()
    actual = mod.sum_all(*args)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_sum_all_rejects_non_int(monkeypatch, capsys):
    mod = _load_module(monkeypatch)
    capsys.readouterr()
    with pytest.raises(TypeError):
        mod.sum_all(1, "2", 3)


def test_sum_all_accepts_large_number_of_args(monkeypatch, capsys):
    mod = _load_module(monkeypatch)
    capsys.readouterr()
    args = tuple(range(1, 501))
    expected = sum(args)
    actual = mod.sum_all(*args)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_source_uses_args_syntax():
    with open(f"{MODULE_NAME}.py", "r", encoding="utf-8") as f:
        src = f.read()
    has_def = bool(re.search(r"def\s+sum_all\s*\(\s*\*args\s*\)\s*:", src))
    assert has_def is True, f"expected={True} actual={has_def}"