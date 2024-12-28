import sys
import functools

def get_empty_candidates(occupied_indices, size):
    '''
    Yields tuples that contain the midpoints in contiguous empty blocks and
    the index in the occupied_indices that delimits the block on the right.
    '''
    # if the first urinal is not occupied, it is empty
    if 0 != next(iter(occupied_indices), None):
        yield 0, 0
    for p, (i, j) in enumerate(zip(occupied_indices, occupied_indices[1:])):
        gap_size = j - i
        if gap_size > 1:
            midpoint = i + gap_size // 2
            yield midpoint, p + 1
            if gap_size % 2 == 1:
                yield midpoint + 1, p + 1
    # if the last urinal is not occupied, it is empty
    if size - 1 != next(iter(reversed(occupied_indices)), None):
        yield size - 1, len(occupied_indices)

def compare_sequences(a, b):
    '''
    >>> compare_sequences((i for i in range(1, 4)), [2, 3, 4])
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

def get_distances(occupied_urinal_indices, empty_position_and_right_occupied_idx):
    '''
    >>> list(get_distances([0], (2, 1))) # 100
    [2]
    >>> list(get_distances([2], (0, 0))) # 001
    [2]
    >>> list(get_distances([0, 3], (1, 1))) # 1001
    [1, 2]
    >>> list(get_distances([0, 3], (2, 1))) # 1001
    [1, 2]
    >>> list(get_distances([0, 2, 5], (1, 1))) # 101001
    [1, 1, 4]
    >>> list(get_distances([0, 2, 5], (4, 2))) # 101001
    [1, 2, 4]
    >>> list(get_distances([0, 2, 5], (7, 3))) # 101001
    [2, 5, 7]
    '''
    empty_position, right = empty_position_and_right_occupied_idx
    left = right - 1
    while left >= 0 and right < len(occupied_urinal_indices):
        d_left = empty_position - occupied_urinal_indices[left]
        d_right = occupied_urinal_indices[right] - empty_position
        if d_left < d_right:
            yield d_left
            left -= 1
        else:
            yield d_right
            right += 1
    while left >= 0:
        d_left = empty_position - occupied_urinal_indices[left]
        yield d_left
        left -= 1
    while right < len(occupied_urinal_indices):
        d_right = occupied_urinal_indices[right] - empty_position
        yield d_right
        right += 1

def solve(urinals):
    occupied_urinal_indices = [j for (j, v) in enumerate(urinals) if v == '1']
    def cmp(i, j):
        distances_to_i = get_distances(occupied_urinal_indices, i)
        distances_to_j = get_distances(occupied_urinal_indices, j)
        result = compare_sequences(distances_to_i, distances_to_j)
        if result != 0:
            return result
        return i[0] - j[0]

    candidates = get_empty_candidates(occupied_urinal_indices, len(urinals))
    return max(candidates, default=('N/A', ), key=functools.cmp_to_key(cmp))[0]

if __name__ == '__main__':
    for line in sys.stdin:
        print(solve(line.strip()))
