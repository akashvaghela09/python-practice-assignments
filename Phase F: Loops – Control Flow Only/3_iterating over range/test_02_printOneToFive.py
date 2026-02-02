import importlib.util
import io
import os
import re
import sys


def _load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_script_capture_stdout(file_path):
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        _load_module("student_module_02_printOneToFive", file_path)
    finally:
        sys.stdout = old
    return buf.getvalue()


def test_prints_numbers_1_to_5_each_on_own_line(capsys):
    file_path = os.path.join(os.path.dirname(__file__), "02_printOneToFive.py")
    out = _run_script_capture_stdout(file_path)

    lines = out.splitlines()
    expected = ["1", "2", "3", "4", "5"]
    assert lines == expected, f"expected={expected!r} actual={lines!r}"


def test_no_extra_whitespace_or_blank_lines(capsys):
    file_path = os.path.join(os.path.dirname(__file__), "02_printOneToFive.py")
    out = _run_script_capture_stdout(file_path)

    assert out.endswith("\n"), f"expected={True!r} actual={out.endswith(chr(10))!r}"
    lines = out.splitlines()
    expected_len = 5
    assert len(lines) == expected_len, f"expected={expected_len!r} actual={len(lines)!r}"
    stripped = [s.strip() for s in lines]
    assert stripped == lines, f"expected={lines!r} actual={stripped!r}"


def test_source_uses_range_with_two_arguments():
    file_path = os.path.join(os.path.dirname(__file__), "02_printOneToFive.py")
    with open(file_path, "r", encoding="utf-8") as f:
        src = f.read()

    src_nc = re.sub(r"#.*", "", src)
    range_calls = re.findall(r"\brange\s*\(([^)]*)\)", src_nc)
    assert range_calls, f"expected={True!r} actual={False!r}"

    has_two_args = any(len([p.strip() for p in call.split(",") if p.strip()]) == 2 for call in range_calls)
    assert has_two_args, f"expected={True!r} actual={has_two_args!r}"


def test_source_prints_loop_variable_not_constant():
    file_path = os.path.join(os.path.dirname(__file__), "02_printOneToFive.py")
    with open(file_path, "r", encoding="utf-8") as f:
        src = f.read()

    src_nc = re.sub(r"#.*", "", src)
    m = re.search(r"for\s+([A-Za-z_]\w*)\s+in\s+range\s*\(", src_nc)
    assert m is not None, f"expected={True!r} actual={False!r}"
    var = m.group(1)

    print_uses_var = re.search(rf"\bprint\s*\(\s*{re.escape(var)}\s*\)", src_nc) is not None or re.search(
        rf"\bprint\s+{re.escape(var)}\b", src_nc
    ) is not None
    assert print_uses_var, f"expected={True!r} actual={print_uses_var!r}"