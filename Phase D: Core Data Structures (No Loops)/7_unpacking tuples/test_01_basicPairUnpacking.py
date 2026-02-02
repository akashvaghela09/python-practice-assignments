import importlib.util
import pathlib
import sys


def _run_module_capture_stdout(module_name, file_path, capsys):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    out = capsys.readouterr().out
    return module, out


def test_outputs_two_lines_expected_values(capsys):
    file_path = pathlib.Path(__file__).with_name("01_basicPairUnpacking.py")
    module, out = _run_module_capture_stdout("mod_01_basicPairUnpacking_out", file_path, capsys)

    lines = [line.strip() for line in out.splitlines() if line.strip() != ""]
    assert len(lines) == 2, f"expected=2 actual={len(lines)}"

    expected = ["10", "20"]
    assert lines == expected, f"expected={expected} actual={lines}"


def test_variables_defined_and_unpacked_correctly(capsys):
    file_path = pathlib.Path(__file__).with_name("01_basicPairUnpacking.py")
    module, _ = _run_module_capture_stdout("mod_01_basicPairUnpacking_vars", file_path, capsys)

    assert hasattr(module, "pair"), "expected=True actual=False"
    assert hasattr(module, "a"), "expected=True actual=False"
    assert hasattr(module, "b"), "expected=True actual=False"

    assert isinstance(module.pair, tuple), f"expected=tuple actual={type(module.pair).__name__}"
    assert len(module.pair) == 2, f"expected=2 actual={len(module.pair)}"

    assert module.a == module.pair[0], f"expected={module.pair[0]} actual={module.a}"
    assert module.b == module.pair[1], f"expected={module.pair[1]} actual={module.b}"