import sys
import functools
import bisect

def get_empty_candidates(occupied_indices, size):
    if 0 != next(iter(occupied_indices), None):
        yield 0
    for i, j in zip(occupied_indices, occupied_indices[1:]):
        d = j - i
        if d > 1:
            yield i + d // 2
            if d % 2 == 1:
                yield i + d // 2 + 1
    if size - 1 != next(iter(reversed(occupied_indices)), None):
        yield size - 1

def compare_sequences(a, b):
    '''
    >>> compare_sequences([1, 2, 3], [2, 3, 4])
    -1
    >>> compare_sequences([1, 2, 3], [1, 2, 3])
    0
    >>> compare_sequences([3, 2, 3], [2, 3, 4])
    1
    >>> compare_sequences([], [2, 3, 4])
    1
    >>> compare_sequences([1, 2, 3, 4], [1, 2, 3])
    -1
    '''
    end = object()
    iter_a = iter(a)
    iter_b = iter(b)
    va = next(iter_a, end)
    vb = next(iter_b, end)
    while va != end and vb != end:
        if va > vb:
            return 1
        elif va < vb:
            return -1
        va = next(iter_a, end)
        vb = next(iter_b, end)
    if va == end and vb == end:
        return 0
    elif va == end:
        return 1
    else:
        return -1

def get_distances(occupied_urinal_indices, empty_position):
    '''
    >>> list(get_distances([0], 2)) # 100
    [2]
    >>> list(get_distances([2], 0)) # 001
    [2]
    >>> list(get_distances([0, 3], 1)) # 1001
    [1, 2]
    >>> list(get_distances([0, 3], 2)) # 1001
    [1, 2]
    >>> list(get_distances([0, 2, 5], 1)) # 101001
    [1, 1, 4]
    >>> list(get_distances([0, 2, 5], 4)) # 101001
    [1, 2, 4]
    '''
    j = bisect.bisect_right(occupied_urinal_indices, empty_position)
    i = j - 1
    while i >= 0 and j < len(occupied_urinal_indices):
        di = empty_position - occupied_urinal_indices[i]
        dj = occupied_urinal_indices[j] - empty_position
        if di < dj:
            yield di
            i -= 1
        else:
            yield dj
            j += 1
    while i >= 0:
        di = empty_position - occupied_urinal_indices[i]
        yield di
        i -= 1
    while j < len(occupied_urinal_indices):
        dj = occupied_urinal_indices[j] - empty_position
        yield dj
        j += 1

def solve(urinals):
    occupied_urinal_indices = [j for (j, v) in enumerate(urinals) if v == '1']
    def cmp(i, j):
        distances_to_i = get_distances(occupied_urinal_indices, i)
        distances_to_j = get_distances(occupied_urinal_indices, j)
        result = compare_sequences(distances_to_i, distances_to_j)
        if result != 0:
            return result
        return i - j

    candidates = get_empty_candidates(occupied_urinal_indices, len(urinals))
    return max(candidates, default='N/A', key=functools.cmp_to_key(cmp))

if __name__ == '__main__':
    for line in sys.stdin:
        print(solve(line.strip()))
