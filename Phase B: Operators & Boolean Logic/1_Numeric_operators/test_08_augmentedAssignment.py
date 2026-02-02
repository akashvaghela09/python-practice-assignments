import importlib
import io
import contextlib
import re

MODULE_NAME = "08_augmentedAssignment"


def _run_module_capture_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.invalidate_caches()
        importlib.import_module(MODULE_NAME)
    return buf.getvalue()


def test_output_exact():
    out = _run_module_capture_stdout()
    expected = "Score: 42\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_score_variable_is_42():
    importlib.invalidate_caches()
    mod = importlib.import_module(MODULE_NAME)
    expected = 42
    actual = getattr(mod, "score", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_uses_augmented_assignment_operators():
    importlib.invalidate_caches()
    mod = importlib.import_module(MODULE_NAME)
    src = open(mod.__file__, "r", encoding="utf-8").read()

    expected_ops = {"+=": True, "*=": True, "-=": True}
    actual_ops = {op: (op in src) for op in expected_ops}

    missing = [op for op, present in actual_ops.items() if not present]
    assert not missing, f"expected={sorted(expected_ops.keys())!r} actual={missing!r}"


def test_does_not_directly_assign_final_score_literal():
    importlib.invalidate_caches()
    mod = importlib.import_module(MODULE_NAME)
    src = open(mod.__file__, "r", encoding="utf-8").read()

    pattern = re.compile(r"^\s*score\s*=\s*42\s*$", re.MULTILINE)
    expected = False
    actual = bool(pattern.search(src))
    assert actual == expected, f"expected={expected!r} actual={actual!r}"