import importlib.util
import os
import re
import sys
from pathlib import Path


def _load_module_and_capture_output(module_path):
    name = "student_mod_01_basicArithmeticPrecedence"
    spec = importlib.util.spec_from_file_location(name, str(module_path))
    module = importlib.util.module_from_spec(spec)

    captured = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        captured.append(sep.join(str(a) for a in args) + end)

    module.print = fake_print

    spec.loader.exec_module(module)
    return module, "".join(captured)


def test_file_exists():
    assert os.path.exists("01_basicArithmeticPrecedence.py")


def test_no_placeholder_tokens_left():
    src = Path("01_basicArithmeticPrecedence.py").read_text(encoding="utf-8")
    assert "__" not in src


def test_prints_exactly_14():
    module, out = _load_module_and_capture_output(Path("01_basicArithmeticPrecedence.py"))
    assert out == "14\n", f"expected={'14\\n'} actual={out!r}"


def test_result_variable_value_is_14():
    module, _ = _load_module_and_capture_output(Path("01_basicArithmeticPrecedence.py"))
    assert hasattr(module, "result")
    assert module.result == 14, f"expected={14!r} actual={module.result!r}"


def test_expression_uses_add_and_multiply_with_2_and_4():
    src = Path("01_basicArithmeticPrecedence.py").read_text(encoding="utf-8")
    compact = re.sub(r"\s+", "", src)
    assert "result=2+" in compact
    assert "*4" in compact
    assert "print(result)" in compact