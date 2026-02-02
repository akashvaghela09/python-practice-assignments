import importlib.util
import io
import os
import sys


def _run_module_capture_stdout(module_filename):
    path = os.path.join(os.path.dirname(__file__), module_filename)
    spec = importlib.util.spec_from_file_location("student_module", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old
    return buf.getvalue(), module


def test_output_is_integer_count():
    out, _ = _run_module_capture_stdout("05_countBeforeStopWord.py")
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) >= 1, f"expected at least one output line, got {len(lines)}"
    last = lines[-1]
    assert last.lstrip("-").isdigit(), f"expected numeric output, got {last!r}"


def test_count_matches_words_before_stop():
    out, module = _run_module_capture_stdout("05_countBeforeStopWord.py")
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    actual = int(lines[-1])

    expected = 0
    for w in module.words:
        if w == "STOP":
            break
        expected += 1

    assert actual == expected, f"expected {expected}, got {actual}"


def test_does_not_count_stop_or_after():
    out, module = _run_module_capture_stdout("05_countBeforeStopWord.py")
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    actual = int(lines[-1])

    if "STOP" in module.words:
        stop_idx = module.words.index("STOP")
        assert actual <= stop_idx, f"expected <= {stop_idx}, got {actual}"
    else:
        assert actual == len(module.words), f"expected {len(module.words)}, got {actual}"