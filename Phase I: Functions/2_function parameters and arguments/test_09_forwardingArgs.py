import importlib.util
import os
import sys
import types
import pytest

MODULE_FILENAME = "09_forwardingArgs.py"


def load_module_with_capture(monkeypatch):
    printed = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        s = sep.join(str(a) for a in args) + end
        printed.append(s)

    monkeypatch.setattr("builtins.print", fake_print)

    spec = importlib.util.spec_from_file_location("forwarding_mod", MODULE_FILENAME)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module, printed


def test_import_prints_exact_expected_output(monkeypatch):
    module, printed = load_module_with_capture(monkeypatch)
    actual = "".join(printed)
    expected = "6\n5\n"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_multiply_default_c(monkeypatch):
    module, _ = load_module_with_capture(monkeypatch)
    assert hasattr(module, "multiply")
    assert callable(module.multiply)
    expected = 12
    actual = module.multiply(3, 4)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_multiply_with_c(monkeypatch):
    module, _ = load_module_with_capture(monkeypatch)
    expected = 30
    actual = module.multiply(2, 3, c=5)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_call_multiply_forwards_args(monkeypatch):
    module, _ = load_module_with_capture(monkeypatch)
    assert hasattr(module, "call_multiply")
    assert callable(module.call_multiply)
    expected = module.multiply(7, 2)
    actual = module.call_multiply(7, 2)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_call_multiply_forwards_kwargs(monkeypatch):
    module, _ = load_module_with_capture(monkeypatch)
    expected = module.multiply(2, 3, c=4)
    actual = module.call_multiply(2, 3, c=4)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_call_multiply_mixed_forwarding(monkeypatch):
    module, _ = load_module_with_capture(monkeypatch)
    expected = module.multiply(2, 5, c=3)
    actual = module.call_multiply(*(2, 5), **{"c": 3})
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_call_multiply_raises_same_typeerror_on_bad_args(monkeypatch):
    module, _ = load_module_with_capture(monkeypatch)

    def call_direct():
        return module.multiply(1)

    def call_forward():
        return module.call_multiply(1)

    with pytest.raises(TypeError) as e1:
        call_direct()
    with pytest.raises(TypeError) as e2:
        call_forward()

    assert type(e1.value) is type(e2.value), f"expected={type(e1.value)!r} actual={type(e2.value)!r}"