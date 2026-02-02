import importlib
import io
import contextlib
import pytest

MODULE_NAME = "02_callWithArgument"


def _load_module():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = importlib.import_module(MODULE_NAME)
    return mod, buf.getvalue()


def test_import_prints_expected_output():
    mod, out = _load_module()
    expected = "Hi, Ada!\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_exclaim_appends_exclamation():
    mod, _ = _load_module()
    actual = mod.exclaim("Hello")
    expected = "Hello!"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_shout_calls_exclaim_for_name():
    mod, _ = _load_module()
    actual = mod.shout("Ada")
    expected = "Hi, Ada!"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_shout_works_with_another_name():
    mod, _ = _load_module()
    name = "Bob"
    actual = mod.shout(name)
    expected = f"Hi, {name}!"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_exclaim_preserves_existing_text_exactly():
    mod, _ = _load_module()
    text = "  spaced  "
    actual = mod.exclaim(text)
    expected = text + "!"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"