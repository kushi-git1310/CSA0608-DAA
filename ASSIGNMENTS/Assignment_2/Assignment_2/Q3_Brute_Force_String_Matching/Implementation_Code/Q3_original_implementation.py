def brute_force_match(text, pattern):
    comparisons = 0
    n, m = len(text), len(pattern)
    if m == 0:
        return 0, comparisons
    for shift in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[shift + j] != pattern[j]:
                break
            j += 1
        if j == m:
            return shift, comparisons
    return -1, comparisons


if __name__ == "__main__":
    tests = [
        ("early mismatch", "abcdefghijk", "z"),
        ("repeated prefix", "aaaaaaaaab", "aaaab"),
        ("match near end", "the quick brown fox jumps", "jumps"),
    ]
    for label, text, pattern in tests:
        index, comparisons = brute_force_match(text, pattern)
        print(f"{label}: index={index}, character comparisons={comparisons}")
