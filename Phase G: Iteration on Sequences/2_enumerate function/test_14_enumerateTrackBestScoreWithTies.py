import importlib
import io
import re
import contextlib
import pytest

MODULE_NAME = "14_enumerateTrackBestScoreWithTies"


def _run_module_capture_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(MODULE_NAME)
    return buf.getvalue()


def _extract_int(label, text):
    m = re.search(rf"^{re.escape(label)}\s*:\s*(-?\d+)\s*$", text, flags=re.MULTILINE)
    if not m:
        return None
    return int(m.group(1))


def test_module_imports_without_error():
    importlib.invalidate_caches()
    importlib.import_module(MODULE_NAME)


def test_outputs_include_best_index_and_best_score_lines():
    importlib.invalidate_caches()
    out = _run_module_capture_stdout()
    assert re.search(r"^Best index:\s*-?\d+\s*$", out, flags=re.MULTILINE), f"expected pattern != actual output\nexpected: Best index: <int>\nactual: {out!r}"
    assert re.search(r"^Best score:\s*-?\d+\s*$", out, flags=re.MULTILINE), f"expected pattern != actual output\nexpected: Best score: <int>\nactual: {out!r}"


def test_best_score_is_max_and_index_is_first_occurrence():
    importlib.invalidate_caches()
    out = _run_module_capture_stdout()

    best_index = _extract_int("Best index", out)
    best_score = _extract_int("Best score", out)

    assert best_index is not None, f"expected != actual\nexpected: parsed int\nactual: {best_index!r}"
    assert best_score is not None, f"expected != actual\nexpected: parsed int\nactual: {best_score!r}"

    scores = [88, 99, 99, 70]
    expected_best_score = max(scores)
    expected_best_index = scores.index(expected_best_score)

    assert best_score == expected_best_score, f"expected != actual\nexpected: {expected_best_score}\nactual: {best_score}"
    assert best_index == expected_best_index, f"expected != actual\nexpected: {expected_best_index}\nactual: {best_index}"


def test_index_corresponds_to_reported_score():
    importlib.invalidate_caches()
    out = _run_module_capture_stdout()

    best_index = _extract_int("Best index", out)
    best_score = _extract_int("Best score", out)

    scores = [88, 99, 99, 70]
    assert 0 <= best_index < len(scores), f"expected != actual\nexpected: valid index range\nactual: {best_index}"
    actual_at_index = scores[best_index]
    assert actual_at_index == best_score, f"expected != actual\nexpected: {best_score}\nactual: {actual_at_index}"