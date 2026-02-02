import importlib.util
import os
import sys


def load_module():
    filename = "03_concatenationAndRepetition.py"
    module_name = "assignment_03_concatenationAndRepetition"
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_banner_value(capsys):
    mod = load_module()
    out = capsys.readouterr().out.strip()
    assert getattr(mod, "banner", None) == "---GO!---", f"expected={'---GO!---'} actual={getattr(mod, 'banner', None)!r}"
    assert out == "---GO!---", f"expected={'---GO!---'} actual={out!r}"


def test_components_and_lengths():
    mod = load_module()
    left = getattr(mod, "left", None)
    center = getattr(mod, "center", None)
    right = getattr(mod, "right", None)
    banner = getattr(mod, "banner", None)

    assert isinstance(left, str), f"expected={str} actual={type(left)}"
    assert isinstance(center, str), f"expected={str} actual={type(center)}"
    assert isinstance(right, str), f"expected={str} actual={type(right)}"
    assert isinstance(banner, str), f"expected={str} actual={type(banner)}"

    assert center == "GO!", f"expected={'GO!'} actual={center!r}"
    assert left == "---", f"expected={'---'} actual={left!r}"
    assert right == "---", f"expected={'---'} actual={right!r}"

    assert len(left) == 3, f"expected={3} actual={len(left)}"
    assert len(center) == 3, f"expected={3} actual={len(center)}"
    assert len(right) == 3, f"expected={3} actual={len(right)}"
    assert len(banner) == 9, f"expected={9} actual={len(banner)}"

    assert banner.startswith(left), f"expected={left!r} actual={banner!r}"
    assert banner.endswith(right), f"expected={right!r} actual={banner!r}"
    assert banner[3:6] == center, f"expected={center!r} actual={banner[3:6]!r}"


def test_no_placeholders_left_in_source():
    filename = "03_concatenationAndRepetition.py"
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    assert "__" not in src, f"expected={False} actual={'__' in src}"