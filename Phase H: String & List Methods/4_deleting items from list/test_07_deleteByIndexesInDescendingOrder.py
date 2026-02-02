import ast
import importlib.util
import pathlib
import sys


FILE_NAME = "07_deleteByIndexesInDescendingOrder.py"


def _load_module(tmp_path, monkeypatch):
    src_path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    if not src_path.exists():
        src_path = pathlib.Path(FILE_NAME).resolve()
    assert src_path.exists()

    tmp_file = tmp_path / FILE_NAME
    tmp_file.write_text(src_path.read_text(encoding="utf-8"), encoding="utf-8")

    monkeypatch.chdir(tmp_path)

    spec = importlib.util.spec_from_file_location("mod_under_test", str(tmp_file))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["mod_under_test"] = mod
    spec.loader.exec_module(mod)
    return mod, tmp_file


def _expected_items():
    items = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    for i in sorted([1, 3, 4], reverse=True):
        del items[i]
    return items


def test_items_after_deletions(tmp_path, monkeypatch):
    mod, _ = _load_module(tmp_path, monkeypatch)
    expected = _expected_items()
    actual = getattr(mod, "items", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_indexes_to_delete_unchanged(tmp_path, monkeypatch):
    mod, _ = _load_module(tmp_path, monkeypatch)
    expected = [1, 3, 4]
    actual = getattr(mod, "indexes_to_delete", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_length_is_correct(tmp_path, monkeypatch):
    mod, _ = _load_module(tmp_path, monkeypatch)
    expected = len(_expected_items())
    actual = len(getattr(mod, "items", []))
    assert actual == expected, f"expected={expected} actual={actual}"


def test_deleted_elements_are_absent(tmp_path, monkeypatch):
    mod, _ = _load_module(tmp_path, monkeypatch)
    original = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    deleted = [original[i] for i in [1, 3, 4]]
    remaining = getattr(mod, "items", [])
    expected = all(x not in remaining for x in deleted)
    actual = all(x not in remaining for x in deleted)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_uses_del_statement(tmp_path, monkeypatch):
    _, tmp_file = _load_module(tmp_path, monkeypatch)
    tree = ast.parse(tmp_file.read_text(encoding="utf-8"))
    has_del = any(isinstance(n, ast.Delete) for n in ast.walk(tree))
    expected = True
    actual = has_del
    assert actual == expected, f"expected={expected} actual={actual}"


def test_does_not_use_pop_remove_or_comprehension_filter(tmp_path, monkeypatch):
    _, tmp_file = _load_module(tmp_path, monkeypatch)
    tree = ast.parse(tmp_file.read_text(encoding="utf-8"))

    forbidden_calls = {"pop", "remove"}
    used_forbidden = False
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            fn = n.func
            if isinstance(fn, ast.Attribute) and fn.attr in forbidden_calls:
                used_forbidden = True
            if isinstance(fn, ast.Name) and fn.id in forbidden_calls:
                used_forbidden = True

    uses_filtering_reassign = False
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id == "items":
                    if isinstance(n.value, (ast.ListComp, ast.GeneratorExp, ast.Call)):
                        uses_filtering_reassign = uses_filtering_reassign or isinstance(n.value, ast.ListComp)

    expected = False
    actual = used_forbidden or uses_filtering_reassign
    assert actual == expected, f"expected={expected} actual={actual}"