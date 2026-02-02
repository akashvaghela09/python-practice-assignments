import ast
import importlib.util
import pathlib


def _load_module(path):
    name = path.stem
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _extract_expected_from_source(source_text):
    tree = ast.parse(source_text)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            s = node.value
            if "Expected outcome" in s and "[" in s and "]" in s:
                start = s.find("[")
                end = s.rfind("]")
                if start != -1 and end != -1 and end > start:
                    try:
                        return ast.literal_eval(s[start : end + 1])
                    except Exception:
                        pass
    raise AssertionError("Could not extract expected list from source.")


def test_replacement_matches_expected_and_is_in_place(capsys):
    path = pathlib.Path(__file__).resolve().parent / "09_replaceUsingMappingParallelList.py"
    source = path.read_text(encoding="utf-8")
    expected = _extract_expected_from_source(source)

    module = _load_module(path)
    captured = capsys.readouterr()

    assert hasattr(module, "basket")
    assert hasattr(module, "old_names")
    assert hasattr(module, "new_names")

    actual_basket = module.basket
    assert actual_basket == expected, f"expected={expected} actual={actual_basket}"

    expected_old = ["apple"]
    expected_new = ["banana"]
    actual_old = module.old_names
    actual_new = module.new_names
    assert actual_old == expected_old, f"expected={expected_old} actual={actual_old}"
    assert actual_new == expected_new, f"expected={expected_new} actual={actual_new}"

    printed = captured.out.strip()
    assert printed == str(expected), f"expected={str(expected)} actual={printed}"


def test_does_not_create_new_basket_object_when_executed():
    path = pathlib.Path(__file__).resolve().parent / "09_replaceUsingMappingParallelList.py"
    module = _load_module(path)

    original_id = id(module.basket)

    module.basket[:] = ["apple", "orange", "kiwi", "orange", "apple"]
    module.old_names[:] = ["apple"]
    module.new_names[:] = ["banana"]
    assert id(module.basket) == original_id

    mapping = dict(zip(module.old_names, module.new_names))
    for i, item in enumerate(module.basket):
        if item in mapping:
            module.basket[i] = mapping[item]

    assert id(module.basket) == original_id