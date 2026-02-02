import importlib
import sys


def test_output_lines_and_values(capsys):
    module_name = "14_updateInventory"
    if module_name in sys.modules:
        del sys.modules[module_name]

    m = importlib.import_module(module_name)
    out = capsys.readouterr().out.splitlines()

    assert len(out) == 4, f"expected=4 actual={len(out)}"

    expected_lines = [
        "start=30",
        "after_sold1=23",
        "after_received=35",
        "after_sold2=30",
    ]
    for i, (exp, act) in enumerate(zip(expected_lines, out)):
        assert act == exp, f"expected={exp} actual={act}"


def test_final_stock_and_vars_defined(capsys):
    module_name = "14_updateInventory"
    if module_name in sys.modules:
        del sys.modules[module_name]

    m = importlib.import_module(module_name)
    capsys.readouterr()

    for name in ["stock", "after_sold1", "after_received", "after_sold2"]:
        assert hasattr(m, name), f"expected=True actual={hasattr(m, name)}"

    assert m.stock == 30, f"expected=30 actual={getattr(m, 'stock', None)}"
    assert m.after_sold1 == 23, f"expected=23 actual={getattr(m, 'after_sold1', None)}"
    assert m.after_received == 35, f"expected=35 actual={getattr(m, 'after_received', None)}"
    assert m.after_sold2 == 30, f"expected=30 actual={getattr(m, 'after_sold2', None)}"