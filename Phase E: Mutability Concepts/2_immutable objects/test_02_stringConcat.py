import importlib.util
import pathlib


def _run_module_capture_stdout(module_filename, monkeypatch):
    captured = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        captured.append(sep.join(str(a) for a in args) + end)

    monkeypatch.setattr("builtins.print", fake_print)
    path = pathlib.Path(__file__).resolve().parent / module_filename
    spec = importlib.util.spec_from_file_location(module_filename[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, "".join(captured)


def test_stdout_lines(monkeypatch):
    _, out = _run_module_capture_stdout("02_stringConcat.py", monkeypatch)
    lines = [ln.rstrip("\n") for ln in out.splitlines()]
    assert lines == ["original: hello", "new: hello world", "same object? False"], f"expected {['original: hello', 'new: hello world', 'same object? False']} got {lines}"


def test_s_and_t_values_and_identity(monkeypatch):
    mod, _ = _run_module_capture_stdout("02_stringConcat.py", monkeypatch)
    assert hasattr(mod, "s")
    assert hasattr(mod, "t")
    assert mod.s == "hello", f"expected {'hello'} got {mod.s}"
    assert mod.t == "hello world", f"expected {'hello world'} got {mod.t}"
    assert id(mod.s) != id(mod.t), f"expected {False} got {id(mod.s) == id(mod.t)}"


def test_orig_id_matches_id_of_s(monkeypatch):
    mod, _ = _run_module_capture_stdout("02_stringConcat.py", monkeypatch)
    assert hasattr(mod, "orig_id")
    assert mod.orig_id == id(mod.s), f"expected {id(mod.s)} got {mod.orig_id}"