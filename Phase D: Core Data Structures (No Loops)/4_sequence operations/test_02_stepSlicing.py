import importlib
import contextlib
import io


def _import_module():
    mod_name = "02_stepSlicing"
    if mod_name in globals():
        globals().pop(mod_name, None)
    if mod_name in importlib.sys.modules:
        importlib.sys.modules.pop(mod_name, None)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = importlib.import_module(mod_name)
    out = buf.getvalue()
    return mod, out


def test_values():
    mod, _ = _import_module()
    assert getattr(mod, "evens") == "02468"
    assert getattr(mod, "odds") == "13579"
    assert getattr(mod, "reversed_digits") == "9876543210"


def test_printed_output_lines():
    _, out = _import_module()
    lines = [line.rstrip("\n") for line in out.splitlines()]
    assert len(lines) == 3
    assert lines[0] == "02468"
    assert lines[1] == "13579"
    assert lines[2] == "9876543210"