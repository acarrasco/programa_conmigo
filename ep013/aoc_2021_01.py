from itertools import tee

# def sliding_by_n(seq, n):
#     '''
#     >>> list(sliding_by_n([1, 2, 3, 4], 1))
#     [(1,), (2,), (3,), (4,)]
#     >>> list(sliding_by_n([1, 2, 3, 4], 2))
#     [(1, 2), (2, 3), (3, 4)]
#     >>> list(sliding_by_n([1, 2, 3, 4], 3))
#     [(1, 2, 3), (2, 3, 4)]
#     >>> list(sliding_by_n([1, 2, 3, 4], 4))
#     [(1, 2, 3, 4)]
#     '''
#     window = []
#     for v in seq:
#         if len(window) >= n:
#             del window[0]
#         window.append(v)
#         if len(window) == n:
#             yield tuple(window)

def sliding_by_n(seq, n):
    '''
    >>> list(sliding_by_n([1, 2, 3, 4], 1))
    [(1,), (2,), (3,), (4,)]
    >>> list(sliding_by_n([1, 2, 3, 4], 2))
    [(1, 2), (2, 3), (3, 4)]
    >>> list(sliding_by_n([1, 2, 3, 4], 3))
    [(1, 2, 3), (2, 3, 4)]
    >>> list(sliding_by_n([1, 2, 3, 4], 4))
    [(1, 2, 3, 4)]
    '''
    iterators = tee(seq, n)
    for i, it in enumerate(iterators):
        for _ in range(i):
            next(it)
    return zip(*iterators)

if __name__ == '__main__':
    depths = list(map(int, open('input.txt')))

    # part 1
    increasing_single = sum(b > a for a, b in zip(depths, depths[1:]))
    print(increasing_single)

    # part 2
    # sliding_window = [a + b + c for a, b, c in zip(depths, depths[1:], depths[2:])]
    sliding_window = [sum(w) for w in sliding_by_n(depths, 3)]
    increasing_window = sum(b > a for a, b in zip(sliding_window, sliding_window[1:]))
    print(increasing_window)
