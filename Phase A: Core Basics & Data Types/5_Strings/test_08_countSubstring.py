import importlib.util
import pathlib
import sys
import types


def _run_module_capture_stdout(module_name: str, file_path: pathlib.Path):
    import builtins

    captured = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        s = sep.join(str(a) for a in args) + end
        captured.append(s)

    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    real_print = builtins.print
    builtins.print = fake_print
    try:
        spec.loader.exec_module(module)
    finally:
        builtins.print = real_print
    return module, "".join(captured)


def test_output_count_is_correct():
    file_path = pathlib.Path(__file__).with_name("08_countSubstring.py")
    module, out = _run_module_capture_stdout("mod08_countSubstring_out", file_path)
    actual = out.strip()
    expected = "2"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_count_variable_correct_value():
    file_path = pathlib.Path(__file__).with_name("08_countSubstring.py")
    module, _ = _run_module_capture_stdout("mod08_countSubstring_var", file_path)
    actual = getattr(module, "count", None)
    expected = 2
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_non_overlapping_logic_on_banana():
    file_path = pathlib.Path(__file__).with_name("08_countSubstring.py")
    module, _ = _run_module_capture_stdout("mod08_countSubstring_logic", file_path)

    ns = {
        "text": "banana",
        "count": module.count,
        "print": lambda *a, **k: None,
    }

    # Re-execute the module code to ensure it computes based on `text` and assigns `count`.
    # If count remains a placeholder constant unrelated to text, this will not help, but it
    # validates correct computation when code is written properly.
    source = file_path.read_text(encoding="utf-8")
    exec(compile(source, str(file_path), "exec"), ns)

    actual = ns.get("count", None)
    expected = 2
    assert actual == expected, f"expected={expected!r} actual={actual!r}"