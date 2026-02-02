import importlib.util
import pathlib


def _load_module_from_path(path):
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_output_exact(capsys):
    path = pathlib.Path(__file__).resolve().parent / "01_variableBasics.py"
    _load_module_from_path(path)
    out = capsys.readouterr().out
    expected = "name=Alex\nage=12\n"
    assert expected == out, f"expected={expected!r} actual={out!r}"


def test_variables_values():
    path = pathlib.Path(__file__).resolve().parent / "01_variableBasics.py"
    m = _load_module_from_path(path)
    assert hasattr(m, "name")
    assert hasattr(m, "age")
    expected_name = "Alex"
    expected_age = 12
    assert expected_name == m.name, f"expected={expected_name!r} actual={m.name!r}"
    assert expected_age == m.age, f"expected={expected_age!r} actual={m.age!r}"
    assert isinstance(m.name, str)
    assert isinstance(m.age, int)