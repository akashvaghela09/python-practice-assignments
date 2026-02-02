import importlib.util
import os
import sys


def test_output_and_reassignment(capsys):
    module_name = "11_dictWithImmutableValues"
    file_name = module_name + ".py"
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    out = capsys.readouterr().out.strip().splitlines()
    expected = ['before: (1, 2)', 'after: (1, 2, 3)']
    assert out == expected, f"expected={expected!r} actual={out!r}"

    assert hasattr(module, "prefs")
    assert isinstance(module.prefs, dict)
    actual_dims = module.prefs.get("dims", None)
    expected_dims = (1, 2, 3)
    assert actual_dims == expected_dims, f"expected={expected_dims!r} actual={actual_dims!r}"
    assert isinstance(actual_dims, tuple)