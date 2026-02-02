import importlib.util
import inspect
import pathlib
import sys
import types
import pytest


MODULE_NAME = "08_positionalOnly_and_keywordOnly"
FILE_NAME = "08_positionalOnly_and_keywordOnly.py"


def _load_module_from_path(path: pathlib.Path) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(path))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules.pop(MODULE_NAME, None)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def mod(tmp_path, monkeypatch):
    cwd = pathlib.Path.cwd()
    module_path = cwd / FILE_NAME
    return _load_module_from_path(module_path)


def test_clamp_signature_positional_only_and_keyword_only(mod):
    sig = inspect.signature(mod.clamp)
    params = list(sig.parameters.values())
    assert [p.name for p in params] == ["x", "low", "high"]

    x, low, high = params
    assert x.kind == inspect.Parameter.POSITIONAL_ONLY
    assert low.kind == inspect.Parameter.KEYWORD_ONLY
    assert high.kind == inspect.Parameter.KEYWORD_ONLY
    assert low.default == 0
    assert high.default == 10


def test_clamp_behavior_default_bounds(mod):
    assert mod.clamp(-5) == 0
    assert mod.clamp(0) == 0
    assert mod.clamp(5) == 5
    assert mod.clamp(10) == 10
    assert mod.clamp(11) == 10


def test_clamp_behavior_custom_bounds(mod):
    assert mod.clamp(7, low=0, high=10) == 7
    assert mod.clamp(20, low=0, high=15) == 15
    assert mod.clamp(-1, low=-2, high=3) == -1
    assert mod.clamp(-5, low=-2, high=3) == -2
    assert mod.clamp(9, low=-2, high=3) == 3


def test_positional_only_enforced(mod):
    with pytest.raises(TypeError):
        mod.clamp(x=1, low=0, high=10)


def test_keyword_only_enforced(mod):
    with pytest.raises(TypeError):
        mod.clamp(1, 0, 10)
    with pytest.raises(TypeError):
        mod.clamp(1, 0, high=10)
    with pytest.raises(TypeError):
        mod.clamp(1, low=0, 10)  # type: ignore[arg-type]


def test_running_file_prints_exactly_expected_output(capsys):
    module_path = pathlib.Path.cwd() / FILE_NAME
    _load_module_from_path(module_path)
    out = capsys.readouterr().out
    assert out == "7\n15\n"