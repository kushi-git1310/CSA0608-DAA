def selection_sort(values):
    a = values[:]
    comparisons = swaps = 0
    for i in range(len(a) - 1):
        min_index = i
        for j in range(i + 1, len(a)):
            comparisons += 1
            if a[j] < a[min_index]:
                min_index = j
        if min_index != i:
            a[i], a[min_index] = a[min_index], a[i]
            swaps += 1
    return a, comparisons, swaps


def bubble_sort(values):
    a = values[:]
    comparisons = swaps = 0
    for end in range(len(a) - 1, 0, -1):
        swapped = False
        for j in range(end):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return a, comparisons, swaps


def insertion_sort(values):
    a = values[:]
    comparisons = shifts = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                shifts += 1
                j -= 1
            else:
                break
        a[j + 1] = key
    return a, comparisons, shifts


if __name__ == "__main__":
    tests = {
        "nearly sorted": [10, 20, 30, 35, 34, 40],
        "reverse order": [60, 50, 40, 30, 20, 10],
        "edge case (empty)": [],
        "duplicates": [4, 2, 4, 1, 2],
    }
    algorithms = [
        ("Selection Sort", selection_sort),
        ("Bubble Sort", bubble_sort),
        ("Insertion Sort", insertion_sort),
    ]
    for test_name, data in tests.items():
        print(f"\n{test_name}: {data}")
        for name, algorithm in algorithms:
            sorted_data, comparisons, movements = algorithm(data)
            print(f"{name}: {sorted_data}; comparisons={comparisons}; swaps/shifts={movements}")
