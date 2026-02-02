import importlib.util
import io
import os
import sys


def load_module_and_capture_output():
    file_name = "04_floorDivision.py"
    module_name = "assignment_04_floorDivision"

    spec = importlib.util.spec_from_file_location(module_name, file_name)
    module = importlib.util.module_from_spec(spec)

    buf = io.StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = buf
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old_stdout

    return module, buf.getvalue()


def test_printed_output_exact():
    module, out = load_module_and_capture_output()
    assert out == "Full boxes: 6\n"


def test_full_boxes_is_int_and_correct():
    module, out = load_module_and_capture_output()
    expected = module.cookies // module.box_size
    assert isinstance(module.full_boxes, int), f"expected {int} got {type(module.full_boxes)}"
    assert module.full_boxes == expected, f"expected {expected} got {module.full_boxes}"


def test_full_boxes_uses_floor_division_operator_in_source():
    file_name = "04_floorDivision.py"
    with open(file_name, "r", encoding="utf-8") as f:
        src = f.read()

    assert "full_boxes" in src
    assert "//" in src
    assert "full_boxes = None" not in src