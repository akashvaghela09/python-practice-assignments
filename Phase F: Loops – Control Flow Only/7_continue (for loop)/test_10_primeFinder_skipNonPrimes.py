import importlib.util
import os
import sys


def _load_module_capture_stdout(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)

    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module, buf.getvalue()


def test_primes_list_exact():
    file_path = os.path.join(os.path.dirname(__file__), "10_primeFinder_skipNonPrimes.py")
    module, _ = _load_module_capture_stdout("prime_finder_10", file_path)

    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert hasattr(module, "primes")
    actual = module.primes
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_output_exact():
    file_path = os.path.join(os.path.dirname(__file__), "10_primeFinder_skipNonPrimes.py")
    _, out = _load_module_capture_stdout("prime_finder_10_out", file_path)

    expected = "2 3 5 7 11 13 17 19 23 29\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_composites_and_in_range():
    file_path = os.path.join(os.path.dirname(__file__), "10_primeFinder_skipNonPrimes.py")
    module, _ = _load_module_capture_stdout("prime_finder_10_props", file_path)

    primes = module.primes
    assert isinstance(primes, list)

    in_range = all(isinstance(p, int) and 2 <= p <= 30 for p in primes)

    def is_prime(x):
        if x < 2:
            return False
        for d in range(2, x):
            if x % d == 0:
                return False
        return True

    all_prime = all(is_prime(p) for p in primes)

    assert in_range and all_prime, f"expected={(True, True)!r} actual={(in_range, all_prime)!r}"