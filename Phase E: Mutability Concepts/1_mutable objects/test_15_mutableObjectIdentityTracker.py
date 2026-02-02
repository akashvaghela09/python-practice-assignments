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
    path = Path(__file__).resolve().parent / "15_mutableObjectIdentityTracker.py"
    module = _load_module(path)

    module.main()
    out = capfd.readouterr().out

    expected = (
        "same_after_mutation: True\n"
        "same_after_shallow_copy: False\n"
        "alias_reflects_change: True\n"
        "final: {'a': [1, 2, 3, 4], 'b': [1, 2, 3, 4], 'c': [1, 2, 3]}\n"
    )
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"
