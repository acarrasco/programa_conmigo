import sys
from itertools import batched
from operator import xor
from functools import reduce

def knot_hash(string, lengths, rounds=1):
    '''
    >>> knot_hash(range(5),(3, 4, 1, 5))
    [3, 4, 2, 1, 0]
    '''
    string = list(string)
    current_position = 0
    skip_size = 0

    for _round in range(rounds):
        for length in lengths:
            for n in range(length // 2):
                i = (current_position + n) % len(string)
                j = (current_position + length - n - 1) % len(string)
                string[i], string[j] = string[j], string[i]
            current_position += length + skip_size
            skip_size += 1

    return string

LENGTHS_PADDING = [17, 31, 73, 47, 23]

def sparse_to_dense_hash(sparse_hash):
    for group in batched(sparse_hash, 16):
        yield reduce(xor, group)

def full_hash(input):
    '''
    >>> full_hash('')
    'a2582a3a0e66e6e86e3812dcb672a272'

    >>> full_hash('AoC 2017')
    '33efeb34ea91902bb2f59c9920caa6cd'
    '''
    lengths = list(map(ord, input)) + LENGTHS_PADDING
    sparse_hash = knot_hash(range(256), lengths, rounds=64)
    dense_hash = sparse_to_dense_hash(sparse_hash)
    return bytearray(dense_hash).hex()

def count_bits(a):
    '''
    >>> count_bits(0b10101)
    3
    >>> count_bits(0xFF00)
    8
    >>> count_bits(0)
    0
    >>> count_bits(7)
    3
    '''
    mask = 0o11111111111
    a = (a - ((a&~mask)>>1)) - ((a>>2)&mask)
    a += a >> 3
    a = (a & 0o70707) + ((a>>18) & 0o70707)
    a *= 0o10101
    return ((a>>12) & 0x3f)

def count_ones(b):
    return sum(map(count_bits, b))

def generate_grid(key):
    return [bytearray.fromhex(full_hash(f'{key}-{row}'))
            for row in range(128)]

def part_1(grid):
    total_ones = 0
    for row in grid:
        total_ones += count_ones(row)
    return total_ones

ADJACENCY = [(1, 0), (-1, 0), (0, -1), (0, 1)]

def flood_fill(grid, i, j, visited):
    for di, dj in ADJACENCY:
        ni, nj = i + di, j + dj
        if (
                0 <= ni < len(grid)
            and 0 <= nj < len(grid)
            and grid[ni][nj] == '1'
            and (ni, nj) not in visited
        ):
            visited.add((ni, nj))
            flood_fill(grid, ni, nj, visited)

def part_2(grid):
    string_grid = [
        ''.join(f'{i:08b}' for i in row) for row in grid
    ]
    region_count = 0
    visited = set()
    for i, row in enumerate(string_grid):
        for j, c in enumerate(row):
            if c == '1' and (i, j) not in visited:
                flood_fill(string_grid, i, j, visited)
                region_count += 1
    return region_count

if __name__ == '__main__':
    input = sys.argv[1]
    grid = generate_grid(input)
    print(part_1(grid))
    print(part_2(grid))