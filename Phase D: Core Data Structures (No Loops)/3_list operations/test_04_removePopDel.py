import importlib.util
import os
import re


def _run_module_capture_output(pytester):
    script_path = os.path.join(os.path.dirname(__file__), "04_removePopDel.py")
    spec = importlib.util.spec_from_file_location("mod04_removePopDel", script_path)
    module = importlib.util.module_from_spec(spec)
    with pytester.capture_stdout() as cap:
        spec.loader.exec_module(module)
    return cap.getvalue()


def test_output_removed_and_remaining(pytester):
    out = _run_module_capture_output(pytester)

    m_removed = re.search(r"^removed=(.*)$", out, re.MULTILINE)
    m_remaining = re.search(r"^remaining=(.*)$", out, re.MULTILINE)

    assert m_removed is not None, f"expected={True} actual={False}"
    assert m_remaining is not None, f"expected={True} actual={False}"

    actual_removed = m_removed.group(1).strip()
    actual_remaining = m_remaining.group(1).strip()

    assert actual_removed == "3", f"expected={'3'} actual={actual_removed}"
    assert actual_remaining == "[1, 2, 4]", f"expected={'[1, 2, 4]'} actual={actual_remaining}"


def test_only_expected_lines_present(pytester):
    out = _run_module_capture_output(pytester)
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    actual = len(lines)
    assert actual == 2, f"expected={2} actual={actual}"
    assert lines[0].startswith("removed="), f"expected={'removed='} actual={lines[0][:8]}"
    assert lines[1].startswith("remaining="), f"expected={'remaining='} actual={lines[1][:10]}"


def test_module_state_nums_and_removed(pytester):
    script_path = os.path.join(os.path.dirname(__file__), "04_removePopDel.py")
    spec = importlib.util.spec_from_file_location("mod04_removePopDel_state", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "nums"), f"expected={True} actual={False}"
    assert hasattr(module, "removed"), f"expected={True} actual={False}"

    actual_nums = module.nums
    actual_removed = module.removed

    assert actual_removed == 3, f"expected={3} actual={actual_removed}"
    assert actual_nums == [1, 2, 4], f"expected={[1, 2, 4]} actual={actual_nums}"