import importlib.util
import os
import re
import sys


def _run_script_capture_stdout(script_path):
    spec = importlib.util.spec_from_file_location("caseconv_mod", script_path)
    module = importlib.util.module_from_spec(spec)

    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)
    return module, buf.getvalue()


def test_stdout_two_lines_exact(capsys):
    script_path = os.path.join(os.path.dirname(__file__), "12_caseConversion.py")
    _, out = _run_script_capture_stdout(script_path)
    lines = [line for line in out.splitlines() if line != ""]
    assert len(lines) == 2, f"expected={2!r} actual={len(lines)!r}"
    assert lines[0] == "PYTHON 101", f"expected={'PYTHON 101'!r} actual={lines[0]!r}"
    assert lines[1] == "python 101", f"expected={'python 101'!r} actual={lines[1]!r}"


def test_upper_lower_variables_and_values():
    script_path = os.path.join(os.path.dirname(__file__), "12_caseConversion.py")
    module, _ = _run_script_capture_stdout(script_path)

    assert hasattr(module, "text"), f"expected={True!r} actual={hasattr(module, 'text')!r}"
    assert hasattr(module, "upper"), f"expected={True!r} actual={hasattr(module, 'upper')!r}"
    assert hasattr(module, "lower"), f"expected={True!r} actual={hasattr(module, 'lower')!r}"

    assert isinstance(module.text, str), f"expected={str!r} actual={type(module.text)!r}"
    assert isinstance(module.upper, str), f"expected={str!r} actual={type(module.upper)!r}"
    assert isinstance(module.lower, str), f"expected={str!r} actual={type(module.lower)!r}"

    exp_upper = module.text.upper()
    exp_lower = module.text.lower()
    assert module.upper == exp_upper, f"expected={exp_upper!r} actual={module.upper!r}"
    assert module.lower == exp_lower, f"expected={exp_lower!r} actual={module.lower!r}"


def test_source_has_no_empty_todo_assignments():
    script_path = os.path.join(os.path.dirname(__file__), "12_caseConversion.py")
    with open(script_path, "r", encoding="utf-8") as f:
        src = f.read()

    # Avoid leaving upper/lower as empty strings
    m_upper = re.search(r"^\s*upper\s*=\s*(.+)$", src, re.MULTILINE)
    m_lower = re.search(r"^\s*lower\s*=\s*(.+)$", src, re.MULTILINE)

    assert m_upper is not None, f"expected={True!r} actual={False!r}"
    assert m_lower is not None, f"expected={True!r} actual={False!r}"

    upper_rhs = m_upper.group(1).split("#", 1)[0].strip()
    lower_rhs = m_lower.group(1).split("#", 1)[0].strip()

    assert upper_rhs not in ('""', "''"), f"expected={False!r} actual={upper_rhs in ('\"\"', \"''\")!r}"
    assert lower_rhs not in ('""', "''"), f"expected={False!r} actual={lower_rhs in ('\"\"', \"''\")!r}"