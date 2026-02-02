import importlib.util
import pathlib
import sys


def _run_module_capture_stdout(path):
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    captured = []

    class _CapStdout:
        def write(self, s):
            captured.append(s)

        def flush(self):
            pass

    old_stdout = sys.stdout
    sys.stdout = _CapStdout()
    try:
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old_stdout

    out = "".join(captured)
    if out.endswith("\n"):
        out = out[:-1]
    return module, out


def test_output_exact_three_lines():
    path = pathlib.Path(__file__).resolve().parent / "08_parseMixedInput.py"
    _, out = _run_module_capture_stdout(path)
    expected = "42\n3.14\nTrue"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_types_and_values():
    path = pathlib.Path(__file__).resolve().parent / "08_parseMixedInput.py"
    mod, _ = _run_module_capture_stdout(path)

    assert hasattr(mod, "a")
    assert hasattr(mod, "b")
    assert hasattr(mod, "c")

    assert isinstance(mod.a, int), f"expected={int} actual={type(mod.a)}"
    assert isinstance(mod.b, float), f"expected={float} actual={type(mod.b)}"
    assert isinstance(mod.c, bool), f"expected={bool} actual={type(mod.c)}"

    assert mod.a == 42, f"expected={42!r} actual={mod.a!r}"
    assert mod.b == 3.14, f"expected={3.14!r} actual={mod.b!r}"
    assert mod.c is True, f"expected={True!r} actual={mod.c!r}"


def test_parts_structure_and_content():
    path = pathlib.Path(__file__).resolve().parent / "08_parseMixedInput.py"
    mod, _ = _run_module_capture_stdout(path)

    assert hasattr(mod, "parts")
    assert isinstance(mod.parts, (list, tuple)), f"expected={(list, tuple)} actual={type(mod.parts)}"
    assert len(mod.parts) == 3, f"expected={3!r} actual={len(mod.parts)!r}"

    expected = ["42", "3.14", "True"]
    actual = list(mod.parts)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"