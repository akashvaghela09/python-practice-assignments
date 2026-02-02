import importlib
import io
import contextlib
import sys


def test_swap_with_unpacking_output_order_and_values():
    module_name = "02_swapWithUnpacking"
    if module_name in sys.modules:
        del sys.modules[module_name]

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = importlib.import_module(module_name)

    lines = [line.rstrip("\n") for line in buf.getvalue().splitlines() if line.strip() != ""]
    assert len(lines) == 2, f"expected=2 actual={len(lines)}"
    assert lines[0] == "right", f"expected={'right'} actual={lines[0]!r}"
    assert lines[1] == "left", f"expected={'left'} actual={lines[1]!r}"

    assert getattr(mod, "x", None) == "right", f"expected={'right'} actual={getattr(mod, 'x', None)!r}"
    assert getattr(mod, "y", None) == "left", f"expected={'left'} actual={getattr(mod, 'y', None)!r}"