import sys

def get_empty_candidates(occupied_indices, size):
    '''
    >>> list(get_empty_candidates([0, 1], 2)) # 11
    []
    >>> list(get_empty_candidates([], 3)) # 000
    [0, 2]
    >>> list(get_empty_candidates([0, 2], 3)) # 101
    [1]
    >>> list(get_empty_candidates([0, 3], 4)) # 1001
    [1, 2]
    >>> list(get_empty_candidates([0, 7], 8)) # 10000001
    [3, 4]
    >>> list(get_empty_candidates([1], 5)) # 01000
    [0, 4]
    '''
    if 0 != next(iter(occupied_indices), None):
        yield 0
    for i, j in zip(occupied_indices, occupied_indices[1:]):
        d = j - i
        if d > 1:
            yield i + d // 2
            if d % 2 == 1:
                yield i + d // 2 + 1
    if size -1 != next(iter(reversed(occupied_indices)), None):
        yield size - 1

def solve(urinals):
    occupied_urinal_indices = [j for (j, v) in enumerate(urinals) if v == '1']
    def key(i):
        distances_to_occupied = sorted(abs(i-j) for j in occupied_urinal_indices)
        return distances_to_occupied, i
    candidates = get_empty_candidates(occupied_urinal_indices, len(urinals))
    return max(candidates, default='N/A', key=key)


if __name__ == '__main__':
    for line in sys.stdin:
        print(solve(line.strip()))
