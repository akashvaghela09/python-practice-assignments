import ast
import importlib.util
import pathlib
import re

FILE_NAME = "11_findCommonAttendees.py"


def _load_module_from_path(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location("mod_11_findCommonAttendees", str(path))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_no_placeholder_underscores_remain():
    src = pathlib.Path(FILE_NAME).read_text(encoding="utf-8")
    assert "____" not in src


def test_both_uses_intersection_semantics_via_output(capsys):
    module = _load_module_from_path(pathlib.Path(FILE_NAME))
    out = capsys.readouterr().out.strip()

    expected = module.event1 & module.event2
    actual = ast.literal_eval(out) if out else None

    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_prints_exact_intersection_set_content(capsys):
    module = _load_module_from_path(pathlib.Path(FILE_NAME))
    out = capsys.readouterr().out.strip()

    expected = module.event1 & module.event2
    actual = ast.literal_eval(out) if out else None

    assert isinstance(actual, set), f"expected={set!r} actual={type(actual)!r}"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_both_variable_matches_printed_value(capsys):
    module = _load_module_from_path(pathlib.Path(FILE_NAME))
    out = capsys.readouterr().out.strip()

    printed = ast.literal_eval(out) if out else None
    both_val = getattr(module, "both", None)

    assert printed == both_val, f"expected={both_val!r} actual={printed!r}"


def test_does_not_mutate_input_sets():
    module = _load_module_from_path(pathlib.Path(FILE_NAME))

    event1_before = {"Ava", "Noah", "Mia", "Liam"}
    event2_before = {"Noah", "Ava", "Ethan"}

    assert module.event1 == event1_before, f"expected={event1_before!r} actual={module.event1!r}"
    assert module.event2 == event2_before, f"expected={event2_before!r} actual={module.event2!r}"


def test_uses_intersection_operator_or_method_in_source():
    src = pathlib.Path(FILE_NAME).read_text(encoding="utf-8")
    normalized = re.sub(r"\s+", " ", src)
    uses_amp = "&" in normalized
    uses_intersection_method = ".intersection(" in normalized
    assert (uses_amp or uses_intersection_method) is True, f"expected={True!r} actual={False!r}"