import importlib.util
from pathlib import Path


def _load_module(path: Path):
    if not path.exists():
        raise AssertionError(f"Missing assignment file: {path}")
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_stdout_exact(capfd):
    path = Path(__file__).resolve().parent / "09_shallowCopyNestedList.py"
    module = _load_module(path)

    module.main()
    out = capfd.readouterr().out

    expected = "original: [[1, 99], [3, 4]]\nshallow: [[1, 99], [3, 4]]\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"
