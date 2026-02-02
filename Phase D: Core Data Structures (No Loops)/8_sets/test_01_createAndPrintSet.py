import ast
import importlib.util
import pathlib
import re


TARGET_FILE = "01_createAndPrintSet.py"


def _load_module_from_path(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location("student_mod_01", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _extract_literal_set_or_set_call(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, ast.Set):
            return node
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "set":
            return node
    return None


def _eval_str_set_from_node(node: ast.AST):
    if isinstance(node, ast.Set):
        vals = []
        for elt in node.elts:
            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                vals.append(elt.value)
            else:
                raise TypeError("Non-string element in set literal")
        return set(vals)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "set":
        if len(node.args) != 1 or node.keywords:
            raise TypeError("Unsupported set() call")
        arg = node.args[0]
        if isinstance(arg, (ast.List, ast.Tuple, ast.Set)):
            vals = []
            for elt in arg.elts:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    vals.append(elt.value)
                else:
                    raise TypeError("Non-string element in set() iterable")
            return set(vals)
        raise TypeError("Unsupported set() argument type")
    raise TypeError("Unsupported node type")


def test_file_exists():
    path = pathlib.Path(TARGET_FILE)
    assert path.exists(), f"expected={True!r} actual={path.exists()!r}"


def test_source_parses_and_has_set_of_three_unique_strings():
    src = pathlib.Path(TARGET_FILE).read_text(encoding="utf-8")
    tree = ast.parse(src, filename=TARGET_FILE)

    node = _extract_literal_set_or_set_call(tree)
    assert node is not None, f"expected={'set-literal-or-set-call'!r} actual={None!r}"

    try:
        actual_set = _eval_str_set_from_node(node)
    except Exception as e:
        assert False, f"expected={'set-of-strings'!r} actual={type(e).__name__!r}"

    assert isinstance(actual_set, set), f"expected={set!r} actual={type(actual_set)!r}"
    assert len(actual_set) == 3, f"expected={3!r} actual={len(actual_set)!r}"
    assert all(isinstance(x, str) for x in actual_set), f"expected={True!r} actual={False!r}"


def test_running_prints_a_set_with_three_elements(capsys):
    path = pathlib.Path(TARGET_FILE)
    mod = _load_module_from_path(path)
    _ = mod

    captured = capsys.readouterr()
    out = captured.out.strip()
    assert out != "", f"expected={'non-empty output'!r} actual={out!r}"

    m = re.search(r"\{.*\}", out, flags=re.DOTALL)
    assert m is not None, f"expected={'set-repr'!r} actual={out!r}"

    set_repr = m.group(0)
    try:
        parsed = ast.literal_eval(set_repr)
    except Exception as e:
        assert False, f"expected={'parseable-set-repr'!r} actual={type(e).__name__!r}"

    assert isinstance(parsed, set), f"expected={set!r} actual={type(parsed)!r}"
    assert len(parsed) == 3, f"expected={3!r} actual={len(parsed)!r}"
    assert all(isinstance(x, str) for x in parsed), f"expected={True!r} actual={False!r}"


def test_module_exposes_fruits_as_set_of_three_unique_strings():
    mod = _load_module_from_path(pathlib.Path(TARGET_FILE))
    assert hasattr(mod, "fruits"), f"expected={True!r} actual={hasattr(mod, 'fruits')!r}"
    fruits = getattr(mod, "fruits")
    assert isinstance(fruits, set), f"expected={set!r} actual={type(fruits)!r}"
    assert len(fruits) == 3, f"expected={3!r} actual={len(fruits)!r}"
    assert all(isinstance(x, str) for x in fruits), f"expected={True!r} actual={False!r}"