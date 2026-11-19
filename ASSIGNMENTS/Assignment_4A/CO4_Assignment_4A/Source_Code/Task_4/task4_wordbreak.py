"""Task 4 - WordBreak: original (faulty) algorithm vs repaired algorithm.
Author: S KUSHA LAKSHMI | Reg No: 192571074 | Course: CSA0608
substring(Text, j, i) = characters at positions j .. i-1 (0-based), i.e. Text[j:i]."""

def wordbreak_faulty(text, dictionary, verbose=False):
    n = len(text)
    DP = [False] * (n + 1)
    DP[0] = True
    for i in range(1, n + 1):
        DP[i] = False
        for j in range(0, i):
            if text[j:i] in dictionary:               # DEFECT: DP[j] is never checked
                DP[i] = True
                if verbose:
                    print(f"  i={i}: j={j} substring '{text[j:i]}' in dictionary -> DP[{i}]=TRUE")
                break
        else:
            if verbose:
                print(f"  i={i}: no substring ending here in dictionary -> DP[{i}]=FALSE")
    return DP[n], DP


def wordbreak_fixed(text, dictionary, verbose=False):
    n = len(text)
    DP = [False] * (n + 1)
    DP[0] = True
    for i in range(1, n + 1):
        DP[i] = False
        for j in range(0, i):
            if DP[j] and text[j:i] in dictionary:     # FIX: prefix text[0:j] must be breakable
                DP[i] = True
                if verbose:
                    print(f"  i={i}: j={j} DP[{j}]=TRUE and '{text[j:i]}' in dictionary -> DP[{i}]=TRUE")
                break
        else:
            if verbose:
                print(f"  i={i}: no j with DP[j]=TRUE and word text[j:i] -> DP[{i}]=FALSE")
    return DP[n], DP


if __name__ == "__main__":
    print("=== FAILING INPUT: Text='catdog', Dictionary={'dog'} ===")
    print("Correct answer should be FALSE ('cat' is not a dictionary word)")
    print("-- Faulty algorithm trace --")
    r1, d1 = wordbreak_faulty("catdog", {"dog"}, True)
    print("Faulty  result:", r1, "DP =", d1)
    print("-- Fixed algorithm trace --")
    r2, d2 = wordbreak_fixed("catdog", {"dog"}, True)
    print("Fixed   result:", r2, "DP =", d2)

    print("\n=== REGRESSION INPUT: Text='applepen', Dictionary={'apple','pen'} ===")
    print("-- Faulty algorithm trace --")
    r1, d1 = wordbreak_faulty("applepen", {"apple", "pen"}, True)
    print("Faulty  result:", r1)
    print("-- Fixed algorithm trace --")
    r2, d2 = wordbreak_fixed("applepen", {"apple", "pen"}, True)
    print("Fixed   result:", r2)

    print("\n=== EXTRA TEST CASES (expected vs fixed vs faulty) ===")
    cases = [("leetcode", {"leet", "code"}, True), ("catsandog", {"cats", "dog", "sand", "and", "cat"}, False),
             ("abcd", {"b", "cd"}, False), ("", {"a"}, True), ("aaaa", {"a", "aa"}, True),
             ("xyz", set(), False), ("abab", {"ab"}, True), ("abc", {"c"}, False)]
    for t, d, exp in cases:
        print(f"Text={t!r:12} Dict={sorted(d)!s:28} expected={exp!s:5} "
              f"fixed={wordbreak_fixed(t, d)[0]!s:5} faulty={wordbreak_faulty(t, d)[0]}")
