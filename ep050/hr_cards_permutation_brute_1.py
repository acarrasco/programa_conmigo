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

def check_permutation(permutation, pattern):
    return all(b == 0 or a == b for (a, b) in zip (permutation, pattern))

def solve(pattern):
    n = len(pattern)
    acc = 0
    for i, permutation in enumerate(permutations(range(1, n+1))):
        if check_permutation(permutation, pattern):
            acc += i + 1
    return acc % MOD_RESULT

if __name__ == '__main__':
    n = int(input().strip())

    a = list(map(int, input().rstrip().split()))

    print(solve(a))
