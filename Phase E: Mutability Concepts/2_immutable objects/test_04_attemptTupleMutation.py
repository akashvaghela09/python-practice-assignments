import importlib
import sys


def test_attempt_tuple_mutation_output(capsys):
    module_name = "04_attemptTupleMutation"
    if module_name in sys.modules:
        del sys.modules[module_name]
    importlib.import_module(module_name)

    out = capsys.readouterr().out.strip().splitlines()
    expected = ["error: TypeError", "tuple still: (1, 2, 3)"]
    assert out == expected, f"expected={expected} actual={out}"