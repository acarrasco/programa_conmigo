MOD_RESULT = 10**9 + 7

def permutations(elements):
    if not elements:
        yield []
        return
    for head_index, head in enumerate(elements):
        rest = list(elements)
        del rest[head_index]
        for rest_permutation in permutations(rest):
            yield [head] + rest_permutation

def lehmer_code(permutation):
    """
    >>> lehmer_code([1, 2, 3])
    [0, 0, 0]

    >>> lehmer_code([2, 1, 3])
    [1, 0, 0]

    >>> lehmer_code([3, 2, 1])
    [2, 1, 0]
    """
    result = []
    for i, x in enumerate(permutation):
        inversions = 0
        for j in range(i+1, len(permutation)):
            if permutation[j] < x:
                inversions += 1
        result.append(inversions)
    return result

def lehmer_to_factorial(code):
    """
    >>> lehmer_to_factorial([0, 0, 0])
    0

    >>> lehmer_to_factorial([1, 0, 0])
    2

    >>> lehmer_to_factorial([2, 1, 0])
    5
    """
    base = 1
    result = 0
    for pos in range(1, len(code)):
        base *= pos
        i = len(code) - 1 - pos
        result += base * code[i]
    return result

def permutation_to_index(permutation):
    """
    >>> all(i == permutation_to_index(p) for i, p in enumerate(permutations([1, 2, 3])))
    True
    """
    code = lehmer_code(permutation)
    return lehmer_to_factorial(code)


def replace_missing(pattern, missing):
    """
    >>> replace_missing([0, 1, 2], [3])
    [3, 1, 2]

    >>> replace_missing([1, 2, 3], [])
    [1, 2, 3]
    """
    missing_iter = iter(missing)
    return list(x or next(missing_iter) for x in pattern)

def solve(pattern):
    """
    >>> solve([0, 2, 3, 0])
    23

    >>> solve([4, 3, 2, 1])
    24
    """
    n = len(pattern)
    missing_numbers = set(range(1, n+1)) - set(pattern)
    acc = 0
    for missing_permutation in permutations(missing_numbers):
        replaced = replace_missing(pattern, missing_permutation)
        i = permutation_to_index(replaced)
        acc += i + 1
    return acc % MOD_RESULT

if __name__ == '__main__':
    n = int(input().strip())

    a = list(map(int, input().rstrip().split()))

    print(solve(a))
