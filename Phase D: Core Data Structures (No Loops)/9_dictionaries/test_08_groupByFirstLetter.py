import importlib.util
import ast
import pathlib
import pytest


def load_module_from_filename(filename):
    path = pathlib.Path(__file__).resolve().parent / filename
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_printed_dict(output):
    text = output.strip()
    try:
        return ast.literal_eval(text)
    except Exception:
        return None


def test_groups_variable_is_correct_dict(capsys):
    mod = load_module_from_filename("08_groupByFirstLetter.py")
    expected = {"a": ["ant", "art"], "b": ["bat", "ball"], "c": ["cat"]}
    actual = getattr(mod, "groups", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_printed_output_is_correct_dict(capsys):
    load_module_from_filename("08_groupByFirstLetter.py")
    out = capsys.readouterr().out
    actual = parse_printed_dict(out)
    expected = {"a": ["ant", "art"], "b": ["bat", "ball"], "c": ["cat"]}
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_groups_contains_lists_for_each_key(capsys):
    mod = load_module_from_filename("08_groupByFirstLetter.py")
    groups = getattr(mod, "groups", None)
    expected_types = {"a": list, "b": list, "c": list}
    actual_types = {k: type(groups.get(k)) for k in expected_types} if isinstance(groups, dict) else None
    assert actual_types == expected_types, f"expected={expected_types!r} actual={actual_types!r}"


def test_groups_preserves_input_order_within_each_letter(capsys):
    mod = load_module_from_filename("08_groupByFirstLetter.py")
    words = getattr(mod, "words", None)
    groups = getattr(mod, "groups", None)

    expected = {}
    if isinstance(words, list):
        for w in words:
            expected.setdefault(w[0], []).append(w)

    actual = groups
    assert actual == expected, f"expected={expected!r} actual={actual!r}"