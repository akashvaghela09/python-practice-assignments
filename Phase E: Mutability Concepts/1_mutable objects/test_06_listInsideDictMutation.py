import ast
import importlib.util
import pathlib


def load_module():
    path = pathlib.Path(__file__).resolve().parent / "06_listInsideDictMutation.py"
    spec = importlib.util.spec_from_file_location("m06_listInsideDictMutation", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_main_prints_expected(capsys):
    mod = load_module()
    mod.main()
    out = capsys.readouterr().out
    assert out.endswith("\n")
    printed = out.rstrip("\n")
    actual = ast.literal_eval(printed)
    expected = {"tags": ["python", "mutability", "lists"]}
    assert expected == actual, f"{expected!r} != {actual!r}"


def test_main_does_not_print_extra_lines(capsys):
    mod = load_module()
    mod.main()
    out = capsys.readouterr().out
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    actual = len(lines)
    expected = 1
    assert expected == actual, f"{expected!r} != {actual!r}"


def test_main_prints_dict_with_tags_key(capsys):
    mod = load_module()
    mod.main()
    printed = capsys.readouterr().out.strip()
    actual = ast.literal_eval(printed)
    expected = True
    assert expected == ("tags" in actual), f"{expected!r} != {('tags' in actual)!r}"


def test_main_tags_value_is_list(capsys):
    mod = load_module()
    mod.main()
    printed = capsys.readouterr().out.strip()
    data = ast.literal_eval(printed)
    actual = type(data.get("tags"))
    expected = list
    assert expected == actual, f"{expected!r} != {actual!r}"


def test_main_tags_length_is_three(capsys):
    mod = load_module()
    mod.main()
    printed = capsys.readouterr().out.strip()
    data = ast.literal_eval(printed)
    actual = len(data["tags"])
    expected = 3
    assert expected == actual, f"{expected!r} != {actual!r}"


def test_main_contains_lists_tag(capsys):
    mod = load_module()
    mod.main()
    printed = capsys.readouterr().out.strip()
    data = ast.literal_eval(printed)
    actual = "lists" in data["tags"]
    expected = True
    assert expected == actual, f"{expected!r} != {actual!r}"


def test_main_preserves_existing_order_prefix(capsys):
    mod = load_module()
    mod.main()
    printed = capsys.readouterr().out.strip()
    data = ast.literal_eval(printed)
    actual = data["tags"][:2]
    expected = ["python", "mutability"]
    assert expected == actual, f"{expected!r} != {actual!r}"


def test_main_last_element_is_lists(capsys):
    mod = load_module()
    mod.main()
    printed = capsys.readouterr().out.strip()
    data = ast.literal_eval(printed)
    actual = data["tags"][-1]
    expected = "lists"
    assert expected == actual, f"{expected!r} != {actual!r}"