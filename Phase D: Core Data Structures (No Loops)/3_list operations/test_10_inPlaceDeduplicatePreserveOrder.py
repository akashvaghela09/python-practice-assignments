import importlib.util
import os
import sys
import re


def _load_module_and_capture_stdout(monkeypatch):
    path = os.path.join(os.path.dirname(__file__), "10_inPlaceDeduplicatePreserveOrder.py")
    spec = importlib.util.spec_from_file_location("mod10_inPlaceDeduplicatePreserveOrder", path)
    module = importlib.util.module_from_spec(spec)

    captured = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        captured.append(sep.join(str(a) for a in args) + end)

    monkeypatch.setattr("builtins.print", fake_print)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module, "".join(captured)


def test_unique_variable_exists_and_is_list(monkeypatch):
    module, _ = _load_module_and_capture_stdout(monkeypatch)
    assert hasattr(module, "unique")
    assert isinstance(module.unique, list)


def test_unique_is_deduplicated_and_order_preserved(monkeypatch):
    module, _ = _load_module_and_capture_stdout(monkeypatch)
    items = module.items
    unique = module.unique

    assert len(unique) == len(set(unique))
    seen = set()
    for x in items:
        if x not in seen:
            seen.add(x)
    expected = [x for x in items if (x in seen and not (seen.remove(x) is None))]  # preserve first occurrences

    assert unique == expected


def test_unique_uses_first_occurrences_only(monkeypatch):
    module, _ = _load_module_and_capture_stdout(monkeypatch)
    items = module.items
    unique = module.unique

    idx_map = {}
    for i, v in enumerate(items):
        idx_map.setdefault(v, i)

    for i in range(1, len(unique)):
        prev = unique[i - 1]
        curr = unique[i]
        assert idx_map[prev] < idx_map[curr]


def test_print_output_matches_unique(monkeypatch):
    module, out = _load_module_and_capture_stdout(monkeypatch)

    m = re.search(r"unique=(\[[^\n]*\])", out)
    assert m is not None

    printed_list = eval(m.group(1), {})
    assert printed_list == module.unique


def test_printed_unique_is_expected_for_given_items(monkeypatch):
    module, out = _load_module_and_capture_stdout(monkeypatch)

    items = module.items
    expected = []
    for x in items:
        if x not in expected:
            expected.append(x)

    m = re.search(r"unique=(\[[^\n]*\])", out)
    assert m is not None
    printed_list = eval(m.group(1), {})

    assert module.unique == expected
    assert printed_list == expected