import importlib.util
import io
import os
import contextlib
import pytest

MODULE_FILENAME = "17_formatUserMessage.py"


def load_module():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    spec = importlib.util.spec_from_file_location("student_mod_17", path)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return mod, buf.getvalue()


def test_message_variable_exact():
    mod, _ = load_module()
    assert hasattr(mod, "message")
    expected = "User Ada has 5 new messages."
    actual = mod.message
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_printed_output_exact():
    mod, out = load_module()
    expected = "User Ada has 5 new messages.\n"
    actual = out
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_uses_name_and_new_messages_variables():
    mod, _ = load_module()
    assert hasattr(mod, "name")
    assert hasattr(mod, "new_messages")
    expected = f"User {mod.name} has {mod.new_messages} new messages."
    actual = mod.message
    assert actual == expected, f"expected={expected!r} actual={actual!r}"