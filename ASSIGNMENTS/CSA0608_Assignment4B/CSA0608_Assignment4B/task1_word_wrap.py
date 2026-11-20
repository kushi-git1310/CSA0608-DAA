"""
CSA0608 - Design and Analysis of Algorithms | Assignment 4B
Student : S KUSHA LAKSHMI   Reg.No : 192571074

TASK 1 - Word Wrap as a Document-Layout Engine (Dynamic Programming)

Model
-----
* words[0..n-1]  : the words of the document, in order (order may not change)
* W              : maximum width of a line (characters)
* a line holding words i..j-1 has length  len = sum(len(w)) + (j-i-1)   (single spaces)
* unused spaces  : s = W - len          (a line is legal only if s >= 0)
* penalty        : s^2 for every non-final line, 0 for the final line

DP definition (suffix form)
---------------------------
best[i]   = minimum penalty for laying out words i..n-1 (words before i are already placed)
best[n]   = 0                                   (nothing left -> no cost)
best[i]   = min over j in (i+1..n) such that words i..j-1 fit on one line of
            cost(i, j) + best[j]
            cost(i, j) = 0            if j == n   (this line is the final line)
                         s^2          otherwise
choice[i] = the j that achieved the minimum (used to rebuild the layout)
Answer    = best[0]
"""
import sys
from itertools import combinations

INF = float("inf")


class WordTooLongError(ValueError):
    """Raised when a single word is wider than the line width (no legal layout exists)."""


# --------------------------------------------------------------------------- #
# ALGORITHM LOGIC (no printing here, except through the optional trace list)
# --------------------------------------------------------------------------- #
def validate_input(words, width):
    if width <= 0:
        raise ValueError("Line width must be a positive integer")
    for w in words:
        if len(w) > width:
            raise WordTooLongError(
                f"word '{w}' has length {len(w)} which exceeds the line width {width}")


def wrap_dp(words, width, trace=None, penalise_last_line=False, strict_fit=False):
    """Return (min_penalty, best_table, choice_table).

    trace              : optional list; every candidate considered is appended to it
    penalise_last_line : FAULT-INJECTION switch (a classic bug) - never use in production
    strict_fit         : FAULT-INJECTION switch (off-by-one bug: '<' instead of '<=')
    """
    validate_input(words, width)
    n = len(words)
    best = [INF] * (n + 1)
    choice = [None] * (n + 1)
    best[n] = 0
    for i in range(n - 1, -1, -1):
        line_len = -1                       # becomes len(words[i]) after the first add
        for j in range(i + 1, n + 1):       # candidate: put words i..j-1 on one line
            line_len += len(words[j - 1]) + 1
            fits = line_len < width if strict_fit else line_len <= width
            if not fits:
                break                       # adding more words only makes it longer
            unused = width - line_len
            is_final = (j == n)
            line_pen = 0 if (is_final and not penalise_last_line) else unused ** 2
            total = line_pen + best[j]
            if trace is not None:
                trace.append((i, j, unused, line_pen, best[j], total))
            if total < best[i]:
                best[i] = total
                choice[i] = j
    return best[0], best, choice


def rebuild_layout(words, width, choice, penalise_last_line=False):
    """Follow the choice[] pointers from word 0 and describe every line."""
    n = len(words)
    layout, i = [], 0
    while i < n:
        j = choice[i]
        text = " ".join(words[i:j])
        unused = width - len(text)
        penalty = 0 if (j == n and not penalise_last_line) else unused ** 2
        layout.append({"first": i, "last": j - 1, "text": text,
                       "unused": unused, "penalty": penalty})
        i = j
    return layout


def greedy_wrap_penalty(words, width):
    """Reference only: the 'fill each line as much as possible' strategy (word processors of old)."""
    validate_input(words, width)
    lines, cur = [], []
    for w in words:
        if sum(map(len, cur)) + len(cur) + len(w) <= width:   # len(cur) = spaces already needed
            cur.append(w)
        else:
            lines.append(cur)
            cur = [w]
    lines.append(cur)
    pen = sum((width - len(" ".join(l))) ** 2 for l in lines[:-1])
    return pen, lines


def brute_force_min_penalty(words, width):
    """Independent oracle: try every possible set of line breaks (2^(n-1) layouts)."""
    validate_input(words, width)
    n = len(words)
    best = INF
    for k in range(n):                                   # k = number of break points
        for cuts in combinations(range(1, n), k):
            bounds = (0,) + cuts + (n,)
            ok, pen = True, 0
            for a, b in zip(bounds, bounds[1:]):
                length = len(" ".join(words[a:b]))
                if length > width:
                    ok = False
                    break
                if b != n:
                    pen += (width - length) ** 2
            if ok:
                best = min(best, pen)
    return best


# --------------------------------------------------------------------------- #
# INPUT / OUTPUT
# --------------------------------------------------------------------------- #
def print_layout(layout, width, total):
    print(f"{'Ln':>3} | {'Words':>9} | {'Unused':>6} | {'Penalty':>7} | Text (ruler = width {width})")
    print("-" * (width + 40))
    for k, ln in enumerate(layout, 1):
        span = f"{ln['first']}-{ln['last']}"
        print(f"{k:>3} | {span:>9} | {ln['unused']:>6} | {ln['penalty']:>7} | |{ln['text']:<{width}}|")
    print("-" * (width + 40))
    print(f"MINIMUM TOTAL PENALTY = {total}   (lines used = {len(layout)})")


def print_trace(words, trace, best, choice):
    print(f"{'i':>2} {'word[i]':<12}{'cand j':>6} {'unused s':>9} {'s^2 / 0':>8} {'best[j]':>8} {'total':>6}  selected")
    cur_i = None
    for (i, j, s, pen, bj, tot) in trace:
        mark = "<== chosen" if choice[i] == j else ""
        label = words[i] if i != cur_i else ""
        print(f"{i:>2} {label:<12}{j:>6} {s:>9} {pen:>8} {bj:>8} {tot:>6}  {mark}")
        cur_i = i
    print("best[] table :", {i: best[i] for i in range(len(best))})
    print("choice[] tbl :", {i: choice[i] for i in range(len(choice) - 1)})


def run_case(words, width, title, show_trace=False):
    print(f"\n=== {title} (W = {width}, words = {len(words)}) ===")
    trace = [] if show_trace else None
    total, best, choice = wrap_dp(words, width, trace)
    layout = rebuild_layout(words, width, choice)
    if show_trace:
        print_trace(words, trace, best, choice)
    print_layout(layout, width, total)
    return total, layout, best, choice


# --------------------------------------------------------------------------- #
TEXT = ("Dynamic programming solves a problem by combining the answers to smaller "
        "overlapping subproblems and remembering each answer so that no work is "
        "repeated while a document engine breaks a long paragraph into neat lines")


def first_changed_line(old, new):
    for k in range(min(len(old), len(new))):
        if (old[k]["first"], old[k]["last"]) != (new[k]["first"], new[k]["last"]):
            return k + 1
    return min(len(old), len(new)) + 1 if len(old) != len(new) else None


def main():
    # ---- 1.1 + 1.2  small instance with a COMPLETE DP trace ------------------
    small = "aaa bb cc ddddd".split()
    print("#" * 78)
    print("TASK 1.2  FULL DP TRACE ON A SMALL INSTANCE")
    print("#" * 78)
    print("Meaning of the columns:")
    print("  i        : sub-problem 'lay out words i..n-1'")
    print("  cand j   : first word of the NEXT line (words i..j-1 form the current line)")
    print("  unused s : W - length of that candidate line")
    print("  s^2 / 0  : penalty of that line (0 if it is the final line)")
    print("  best[j]  : already-solved optimum of the smaller sub-problem j..n-1")
    print("  total    : s^2 + best[j]  -> the minimum over j becomes best[i]")
    run_case(small, 6, "Small instance", show_trace=True)

    # ---- 1.1  the real document ---------------------------------------------
    words = TEXT.split()
    print("\n" + "#" * 78)
    print("TASK 1.1  BASELINE RUN ON THE FULL PARAGRAPH")
    print("#" * 78)
    total40, lay40, best40, choice40 = run_case(words, 40, "Baseline W=40")
    print("\nbest[i] for the first 12 and last 6 sub-problems (state evidence):")
    print("  first :", {i: best40[i] for i in range(12)})
    print("  last  :", {i: best40[i] for i in range(len(words) - 5, len(words) + 1)})
    g_pen, g_lines = greedy_wrap_penalty(words, 40)
    print(f"Greedy first-fit penalty = {g_pen} with {len(g_lines)} lines  vs DP optimum = {total40}")

    # ---- 1.3  requirement change: three new widths, prediction first ----------
    print("\n" + "#" * 78)
    print("TASK 1.3  REQUIREMENT CHANGE - PREDICT, THEN RUN")
    print("#" * 78)
    predictions = {
        30: dict(changes=True, first_line=1, direction="increase"),
        50: dict(changes=True, first_line=1, direction="decrease"),
        60: dict(changes=True, first_line=1, direction="decrease"),
    }
    reasons = {
        30: "narrower page: line 1 can no longer hold the same words, more (penalised) lines are needed",
        50: "wider page: line 1 can absorb extra words, fewer penalised lines -> lower penalty",
        60: "even wider page: fewer lines again, more text moves into the free final line",
    }
    summary = []
    for w, pred in predictions.items():
        print(f"\nPREDICTION for W={w}: arrangement changes={pred['changes']}, "
              f"first change at line {pred['first_line']}, total penalty should {pred['direction']} "
              f"(baseline {total40}).")
        print(f"  reasoning: {reasons[w]}")
        total, lay, _, _ = run_case(words, w, f"Actual W={w}")
        fc = first_changed_line(lay40, lay)
        direction = "increase" if total > total40 else ("decrease" if total < total40 else "same")
        summary.append((w, pred, fc, total, direction, len(lay)))
    print("\nPREDICTION vs ACTUAL")
    print(f"{'W':>3} | {'lines':>5} | {'pred.first chg':>14} | {'actual first chg':>16} | "
          f"{'pred. dir':>9} | {'actual dir':>10} | {'penalty':>7} | verdict")
    for w, pred, fc, total, direction, nl in summary:
        ok = (fc == pred["first_line"]) and (direction == pred["direction"])
        print(f"{w:>3} | {nl:>5} | {pred['first_line']:>14} | {str(fc):>16} | "
              f"{pred['direction']:>9} | {direction:>10} | {total:>7} | {'MATCH' if ok else 'PARTIAL/MISMATCH'}")

    # ---- 1.4  boundary tests ---------------------------------------------------
    print("\n" + "#" * 78)
    print("TASK 1.4  BOUNDARY / FAILURE TESTS")
    print("#" * 78)
    bw, bW = ["aaaa", "bbbb", "cc"], 9
    print(f"Chosen boundary case: words={bw}, W={bW}")
    print("  'aaaa bbbb' is EXACTLY 9 characters (unused = 0) and 'cc' is the final line (free).")
    print("  Expected optimum = 0, layout = [aaaa bbbb] / [cc]")
    t, _, c = wrap_dp(bw, bW)
    print("  Correct DP        :", t, [l['text'] for l in rebuild_layout(bw, bW, c)])
    t2, _, c2 = wrap_dp(bw, bW, strict_fit=True)
    print("  Bug 1 (< not <=)  :", t2, [l['text'] for l in rebuild_layout(bw, bW, c2)], " <-- WRONG (exact fit rejected)")
    t3, _, c3 = wrap_dp(bw, bW, penalise_last_line=True)
    print("  Bug 2 (last line penalised):", t3, [l['text'] for l in rebuild_layout(bw, bW, c3, True)], " <-- WRONG")
    assert t == 0 and brute_force_min_penalty(bw, bW) == 0
    assert t2 != 0 and t3 != 0
    print("  => the single case detects BOTH classic defects; correct DP == brute force == 0 : PASS")

    print("\nOther exceptional inputs:")
    tests = [
        ("single word that fits", ["hello"], 10),
        ("single word == width", ["hello"], 5),
        ("text fits on one line", "to be or".split(), 20),
        ("empty document", [], 10),
    ]
    for name, ws, W in tests:
        t, _, c = wrap_dp(ws, W)
        print(f"  {name:<24}: penalty={t}, lines={[l['text'] for l in rebuild_layout(ws, W, c)] if ws else []}")
    for name, ws, W in [("word longer than width", ["extraordinary", "day"], 5),
                        ("zero width", ["a"], 0)]:
        try:
            wrap_dp(ws, W)
            print(f"  {name:<24}: NO ERROR  <-- defect")
        except ValueError as e:
            print(f"  {name:<24}: rejected -> {type(e).__name__}: {e}")

    # ---- independent validation of DP against brute force -----------------------
    print("\nValidation: DP vs exhaustive enumeration on 12-word prefix, widths 14..30")
    sample = words[:12]
    ok_all = True
    for W in range(14, 31, 4):
        d = wrap_dp(sample, W)[0]
        b = brute_force_min_penalty(sample, W)
        ok_all &= (d == b)
        print(f"  W={W:>2}: DP={d:>4}  brute-force={b:>4}  {'OK' if d == b else 'MISMATCH'}")
    print("ALL MATCH" if ok_all else "SOME MISMATCH")


if __name__ == "__main__":
    main()
