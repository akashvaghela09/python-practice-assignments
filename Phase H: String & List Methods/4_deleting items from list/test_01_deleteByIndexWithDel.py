import ast
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout


MODULE_FILE = "01_deleteByIndexWithDel.py"


def load_module(path, name="student_module"):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_uses_del_statement_for_index_2():
    with open(MODULE_FILE, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=MODULE_FILE)

    dels = [n for n in ast.walk(tree) if isinstance(n, ast.Delete)]
    assert dels, "expected vs actual: del statement expected vs missing"

    found = False
    for d in dels:
        for target in d.targets:
            if isinstance(target, ast.Subscript):
                slc = target.slice
                idx = None
                if isinstance(slc, ast.Constant) and isinstance(slc.value, int):
                    idx = slc.value
                elif isinstance(slc, ast.Index) and isinstance(slc.value, ast.Constant) and isinstance(slc.value.value, int):
                    idx = slc.value.value
                if idx == 2:
                    found = True
                    break
        if found:
            break

    assert found, "expected vs actual: del fruits[2] expected vs not found"


def test_output_and_final_list():
    buf = io.StringIO()
    with redirect_stdout(buf):
        mod = load_module(os.path.abspath(MODULE_FILE), name="student_module_run")

    out = buf.getvalue().strip().splitlines()
    assert out, "expected vs actual: output line expected vs none"

    line = out[-1].strip()
    expected_list = ["apple", "banana", "date"]
    expected_line = f"fruits: {expected_list}"
    assert line == expected_line, f"expected vs actual: {expected_line} vs {line}"

    assert hasattr(mod, "fruits"), "expected vs actual: fruits variable expected vs missing"
    assert mod.fruits == expected_list, f"expected vs actual: {expected_list} vs {mod.fruits}"