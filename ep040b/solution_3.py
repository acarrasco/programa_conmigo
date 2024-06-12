import sys

def get_empty_candidates(occupied_indices, size, filter_distance):
    if 0 != next(iter(occupied_indices), None):
        yield 0
    for i, j in zip(occupied_indices, occupied_indices[1:]):
        d = j - i
        if d >= filter_distance:
            yield i + d // 2
            if d % 2 == 1:
                yield i + d // 2 + 1
    if size - 1 != next(iter(reversed(occupied_indices)), None):
        yield size - 1

def get_largest_empty_size(occupied_indices, size):
    '''
    >>> get_largest_empty_size([], 3) # 000
    6
    >>> get_largest_empty_size([0, 2], 3) # 101
    2
    >>> get_largest_empty_size([0, 2, 5], 6) # 101001
    3
    >>> get_largest_empty_size([0, 2, 5], 8) # 10100100
    6
    '''
    largest = 0
    if 0 != next(iter(occupied_indices), None):
        largest = 2 * next(iter(occupied_indices), 0)
    for i, j in zip(occupied_indices, occupied_indices[1:]):
        d = j - i
        largest = max(largest, d)
    last = next(iter(reversed(occupied_indices)), 0)
    if size -1 != last:
        largest = max(largest, 2 * (size - last))
    return largest


def solve(urinals):
    occupied_urinal_indices = [j for (j, v) in enumerate(urinals) if v == '1']
    def key(i):
        occupied_urinals = ((j, v) for (j, v) in enumerate(urinals) if v == '1')
        distances_to_occupied = sorted(abs(i-j) for j, v in occupied_urinals)
        return distances_to_occupied, i
    filter_distance = get_largest_empty_size(occupied_urinal_indices, len(urinals))
    if filter_distance == 1:
        return 'N/A'
    candidates = get_empty_candidates(occupied_urinal_indices, len(urinals), filter_distance)
    return max(candidates, key=key)


if __name__ == '__main__':
    for line in sys.stdin:
        print(solve(line.strip()))
