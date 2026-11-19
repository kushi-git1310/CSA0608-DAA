"""
Unit tests for the three search algorithms.
Name   : S KUSHA LAKSHMI | Reg No : 192571074 | CSA0608 DAA
Run:  python Task_8_Implementation_Testing/Source_Code/test_cases.py
"""
from search_experiments import linear_search, recursive_binary_search

TESTS = []


def case(name, func):
    TESTS.append((name, func))


def hash_search(h, key):
    return h.get(key)


DATA = [1001, 1005, 1010, 1020, 1033, 1047, 1050, 1099]   # sorted, unique
HASH = {k: k for k in DATA}

# (id, description, target, expected index or -1)
CASES = [
    ("TC1", "Target is first element", 1001, 0),
    ("TC2", "Target is last element", 1099, 7),
    ("TC3", "Target is a middle element", 1020, 3),
    ("TC4", "Target present (other)", 1047, 5),
    ("TC5", "Target absent - smaller than all", 500, -1),
    ("TC6", "Target absent - larger than all", 9999, -1),
    ("TC7", "Target absent - between values", 1030, -1),
]


def run():
    passed = failed = 0
    print(f"{'ID':<5}{'Description':<36}{'Target':>7}{'Expected':>9}{'Linear':>8}{'Binary':>8}{'Hash':>6}  Result")
    print("-" * 92)
    for tid, desc, target, exp in CASES:
        lin, _ = linear_search(DATA, target)
        bin_, _ = recursive_binary_search(DATA, target)
        hs = hash_search(HASH, target)
        hs_ok = (hs == target) if exp != -1 else (hs is None)
        ok = lin == exp and bin_ == exp and hs_ok
        passed += ok
        failed += (not ok)
        print(f"{tid:<5}{desc:<36}{target:>7}{exp:>9}{lin:>8}{bin_:>8}{('found' if hs is not None else 'none'):>6}  {'PASS' if ok else 'FAIL'}")

    # Edge cases
    edge = [
        ("TC8", "Empty list", [], 5, -1),
        ("TC9", "Single element - found", [5], 5, 0),
        ("TC10", "Single element - not found", [5], 7, -1),
    ]
    for tid, desc, arr, target, exp in edge:
        lin, _ = linear_search(arr, target)
        bin_, _ = recursive_binary_search(arr, target)
        hs = {k: k for k in arr}.get(target)
        hs_ok = (hs == target) if exp != -1 else (hs is None)
        ok = lin == exp and bin_ == exp and hs_ok
        passed += ok
        failed += (not ok)
        print(f"{tid:<5}{desc:<36}{target:>7}{exp:>9}{lin:>8}{bin_:>8}{('found' if hs is not None else 'none'):>6}  {'PASS' if ok else 'FAIL'}")

    print("-" * 92)
    print(f"Total: {passed + failed}   Passed: {passed}   Failed: {failed}")
    return failed == 0


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
