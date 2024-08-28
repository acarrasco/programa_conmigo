from collections import defaultdict
from itertools import permutations
from math import factorial, comb

MOD_RESULT = 10**9 + 7

def aggregate_inversions(inversions):
    """
    >>> aggregate_inversions([(1, 0), (1, 1), (2, 1)])
    [(1, 0), (3, 1)]
    """
    result = defaultdict(int)
    for amount, inversion_number in inversions:
        result[inversion_number] += amount
    return sorted((amount, inversion_number) for (inversion_number, amount) in result.items())

def calculate_inversions_brute_force(current, seen_values, seen_wildcards, missing_values):
    if current == 0:
        for current in missing_values:
            missing_minus_current = set(missing_values) - {current}
            yield from calculate_inversions_brute_force(current, seen_values, seen_wildcards, missing_minus_current)
        return
    fixed = sum(current > i for i in seen_values)
    for missing_perm in permutations(missing_values, seen_wildcards):
        inversions = fixed + sum(current > i for i in missing_perm)
        yield (1, inversions)

def ways_to_draw_from_two_sets(n_draws, set_a_size, set_b_size):
    """
    >>> list(ways_to_draw_from_two_sets(2, 1, 3))
    [(6, 0, 2), (6, 1, 1)]

    >>> list(ways_to_draw_from_two_sets(2, 2, 2))
    [(2, 0, 2), (8, 1, 1), (2, 2, 0)]
    """
    min_from_a = max(0, n_draws - set_b_size)
    max_from_a = min(n_draws, set_a_size)
    for draw_from_a in range(min_from_a, max_from_a+1):
        draw_from_b = n_draws - draw_from_a
        ways_to_draw_from_a = comb(set_a_size, draw_from_a)
        ways_to_draw_from_b = comb(set_b_size, draw_from_b)
        ways_to_reorder = factorial(n_draws)
        ways = ways_to_draw_from_a * ways_to_draw_from_b * ways_to_reorder
        yield ways, draw_from_a, draw_from_b

def calculate_inversions(current, seen_values, seen_wildcards, missing_values):
    """
    >>> aggregate_inversions(calculate_inversions(3, [4], 0, [1, 2]))
    [(1, 0)]

    >>> aggregate_inversions(calculate_inversions(3, [], 1, [1, 2, 4]))
    [(1, 0), (2, 1)]

    >>> aggregate_inversions(calculate_inversions(2, [], 2, [1, 3, 4]))
    [(2, 0), (4, 1)]

    >>> aggregate_inversions(calculate_inversions(3, [], 3, [1, 2, 4, 5]))
    [(12, 1), (12, 2)]

    >>> aggregate_inversions(calculate_inversions(2, [3], 2, [1, 4]))
    [(2, 1)]

    >>> aggregate_inversions(calculate_inversions(0, [2], 2, [1, 3, 4]))
    [(2, 0), (2, 2), (2, 3)]
    """
    if current == 0:
        for current in missing_values:
            missing_minus_current = set(missing_values) - {current}
            yield from calculate_inversions(current, seen_values, seen_wildcards, missing_minus_current)
        return
    missing_lesser_than_current = sum(current > i for i in missing_values)
    missing_larger_than_current = len(missing_values) - missing_lesser_than_current
    fixed = sum(current > i for i in seen_values)

    unused = len(missing_values) - seen_wildcards
    for ways, inversions, _ in ways_to_draw_from_two_sets(seen_wildcards, missing_lesser_than_current, missing_larger_than_current):
        yield factorial(unused) * ways, fixed + inversions

def solve(pattern):
    """
    >>> solve([0, 2, 3, 0])
    23

    >>> solve([4, 3, 2, 1])
    24
    """
    n = len(pattern)
    missing_digits = set(range(1, n+1)) - set(pattern)
    acc = 0
    pos = 1
    base = 1
    seen_wildcards = 0
    seen_values = []
    if pattern[-1] == 0:
        seen_wildcards += 1
    else:
        seen_values.append(pattern[-1])
    for i in range(len(pattern)-2, -1, -1):
        current = pattern[i]
        base = (base * pos) % MOD_RESULT
        pos += 1
        for amount, inversions in calculate_inversions(current, seen_values, seen_wildcards, missing_digits):
            acc += base * inversions * amount
            acc %= MOD_RESULT
        if current == 0:
            seen_wildcards += 1
        else:
            seen_values.append(current)

    return (acc + factorial(len(missing_digits))) % MOD_RESULT # account for the 1 base offset

if __name__ == '__main__':
    n = int(input().strip())

    a = list(map(int, input().rstrip().split()))

    print(solve(a))
