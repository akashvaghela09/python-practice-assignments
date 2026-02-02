import importlib
import io
import sys


def test_print_aligned_table_output():
    module_name = "08_printAlignedTable"
    if module_name in sys.modules:
        del sys.modules[module_name]

    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        importlib.import_module(module_name)
    finally:
        sys.stdout = old

    actual = buf.getvalue()
    expected = "Item      Qty\nApples      3\nBananas    12\n"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_print_aligned_table_line_count():
    module_name = "08_printAlignedTable"
    if module_name in sys.modules:
        del sys.modules[module_name]

    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        importlib.import_module(module_name)
    finally:
        sys.stdout = old

    actual_lines = buf.getvalue().splitlines()
    expected_lines = ["Item      Qty", "Apples      3", "Bananas    12"]
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"