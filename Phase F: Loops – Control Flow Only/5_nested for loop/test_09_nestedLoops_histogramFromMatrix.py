import ast
import importlib
import io
import contextlib
import pathlib


MODULE_NAME = "09_nestedLoops_histogramFromMatrix"


def _run_module_capture_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = importlib.import_module(MODULE_NAME)
    return mod, buf.getvalue()


def _parse_last_dict_from_stdout(stdout_text):
    lines = [ln.strip() for ln in stdout_text.splitlines() if ln.strip()]
    if not lines:
        return None
    last = lines[-1]
    try:
        val = ast.literal_eval(last)
    except Exception:
        return None
    return val


def _expected_from_grid(grid):
    d = {}
    for row in grid:
        for v in row:
            d[v] = d.get(v, 0) + 1
    return d


def test_freq_variable_exists_and_is_dict():
    mod, _ = _run_module_capture_stdout()
    assert hasattr(mod, "freq")
    assert isinstance(mod.freq, dict)


def test_freq_matches_grid_counts():
    mod, _ = _run_module_capture_stdout()
    expected = _expected_from_grid(mod.grid)
    assert mod.freq == expected


def test_stdout_prints_dict_matching_freq():
    mod, out = _run_module_capture_stdout()
    printed = _parse_last_dict_from_stdout(out)
    assert isinstance(printed, dict)
    assert printed == mod.freq


def test_grid_shape_and_contents_unchanged():
    mod, _ = _run_module_capture_stdout()
    assert isinstance(mod.grid, list)
    assert all(isinstance(r, list) for r in mod.grid)
    flat = [v for row in mod.grid for v in row]
    expected_flat = [1, 2, 2, 3, 1, 2]
    assert flat == expected_flat


def test_uses_nested_loops_and_not_counter():
    src = pathlib.Path(f"{MODULE_NAME}.py").read_text(encoding="utf-8")
    tree = ast.parse(src)

    for_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.For)]
    assert len(for_nodes) >= 2

    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            for alias in n.names:
                assert alias.name != "collections"
        if isinstance(n, ast.Attribute) and n.attr == "Counter":
            assert False

    assert "Counter(" not in src
    assert "collections.Counter" not in src