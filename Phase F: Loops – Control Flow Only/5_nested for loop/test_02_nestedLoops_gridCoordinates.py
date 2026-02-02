import importlib.util
import pathlib
import sys


def load_module(path):
    name = pathlib.Path(path).stem
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_printed_output_matches_expected_grid(capsys):
    path = pathlib.Path(__file__).resolve().parent / "02_nestedLoops_gridCoordinates.py"
    load_module(str(path))
    out = capsys.readouterr().out
    expected = "(0,0) (1,0) (2,0)\n(0,1) (1,1) (2,1)\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_lines_variable_created_and_correct():
    path = pathlib.Path(__file__).resolve().parent / "02_nestedLoops_gridCoordinates.py"
    mod = load_module(str(path))

    assert hasattr(mod, "lines")
    assert isinstance(mod.lines, list)

    expected_lines = ["(0,0) (1,0) (2,0)", "(0,1) (1,1) (2,1)"]
    actual_lines = mod.lines
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"


def test_width_and_height_preserved():
    path = pathlib.Path(__file__).resolve().parent / "02_nestedLoops_gridCoordinates.py"
    mod = load_module(str(path))

    assert hasattr(mod, "width")
    assert hasattr(mod, "height")
    assert mod.width == 3, f"expected={3!r} actual={mod.width!r}"
    assert mod.height == 2, f"expected={2!r} actual={mod.height!r}"


def test_no_trailing_spaces_in_lines():
    path = pathlib.Path(__file__).resolve().parent / "02_nestedLoops_gridCoordinates.py"
    mod = load_module(str(path))

    for line in mod.lines:
        assert line == line.strip(), f"expected={line.strip()!r} actual={line!r}"
        assert "  " not in line, f"expected={False!r} actual={('  ' in line)!r}"