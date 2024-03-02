import sys
from collections import defaultdict
import itertools
from functools import cache

STARTING_GRID = '.#./..#/###'

def rotate_90(pattern):
    '''
    >>> rotate_90('12/34')
    '31/42'
    >>> rotate_90('123/456/789')
    '741/852/963'
    '''
    by_columns = zip(*pattern.split('/'))
    each_column_reversed = map(reversed, by_columns)
    return '/'.join(map(''.join, each_column_reversed))

def rotate_180(pattern):
    return rotate_90(rotate_90(pattern))

def rotate_270(pattern):
    return rotate_90(rotate_180(pattern))

def flip_h(pattern):
    '''
    >>> flip_h('12/34')
    '34/12'
    >>> flip_h('123/456/789')
    '789/456/123'
    '''
    return '/'.join(reversed(pattern.split('/')))

def flip_v(pattern):
    '''
    >>> flip_v('12/34')
    '21/43'
    >>> flip_v('123/456/789')
    '321/654/987'
    '''
    each_row_reversed = map(reversed, pattern.split('/'))
    return '/'.join(map(''.join, each_row_reversed))

def apply_transformations(transformations, pattern):
    for f in transformations:
        pattern = f(pattern)
    return pattern

def get_equivalent_transformations():
    rotations = [rotate_90, rotate_180, rotate_270]
    flips = [flip_h, flip_v]
    all_transformations = rotations + flips
    test_pattern = '123/456/789'
    equivalent_transformations = defaultdict(list)
    for t in all_transformations:
        result = t(test_pattern)
        equivalent_transformations[result].append([t])
    for tts in itertools.product(rotations, flips):
        result = apply_transformations(tts, test_pattern)
        equivalent_transformations[result].append(tts)
    for tts in itertools.product(flips, rotations):
        result = apply_transformations(tts, test_pattern)
        equivalent_transformations[result].append(tts)
    return equivalent_transformations

def get_unique_transformations():
    equivalent_transformations = get_equivalent_transformations()
    def shortest_transformation(list_of_transformations):
        return min(list_of_transformations, key=len)
    return [shortest_transformation(ltts) for ltts in equivalent_transformations.values()]

def digest_rules(raw_rules):
    transformations = get_unique_transformations() + [[lambda x: x]]
    expanded_rules = {}
    for rule in raw_rules:
        src_pattern, dst_pattern = rule.split(' => ')
        for tts in transformations:
            transformed_src = apply_transformations(tts, src_pattern)
            expanded_rules[transformed_src] = dst_pattern
    return expanded_rules

def extract_chunk(grid, chunk_size, ci, cj):
    '''
    >>> extract_chunk(['0123', '4567', '89ab', 'cdef'], 2, 0, 0)
    '01/45'
    >>> extract_chunk(['0123', '4567', '89ab', 'cdef'], 2, 1, 1)
    'ab/ef'
    '''
    return '/'.join(''.join(grid[i][j]
                for j in range(cj*chunk_size, (cj+1)*chunk_size))
                for i in range(ci*chunk_size, (ci+1)*chunk_size))

def chunk_grid(grid):
    '''
    >>> chunk_grid('12/34')
    [['12/34']]
    >>> chunk_grid('0123/4567/89ab/cdef')
    [['01/45', '23/67'], ['89/cd', 'ab/ef']]
    >>> chunk_grid('012345/6789ab/cdefgh/ijklmn/opqrst/uvwxyz')
    [['01/67', '23/89', '45/ab'], ['cd/ij', 'ef/kl', 'gh/mn'], ['op/uv', 'qr/wx', 'st/yz']]
    >>> chunk_grid('012/345/678')
    [['012/345/678']]
    >>> chunk_grid('012345678/9abcdefgh/ijklmnopq/rstuvwxyz/ABCDEFGHI/JKLMNOPQR/STUVWXYZ./!@#$%^&*(/)_+<>?:[]')
    [['012/9ab/ijk', '345/cde/lmn', '678/fgh/opq'], ['rst/ABC/JKL', 'uvw/DEF/MNO', 'xyz/GHI/PQR'], ['STU/!@#/)_+', 'VWX/$%^/<>?', 'YZ./&*(/:[]']]
    '''
    grid_by_lines = grid.split('/')
    grid_size = len(grid_by_lines)
    chunk_size = grid_size % 2 and 3 or 2
    chunks_per_side = grid_size // chunk_size
    return [[extract_chunk(grid_by_lines, chunk_size, ci, cj)
             for cj in range(chunks_per_side)]
             for ci in range(chunks_per_side)]

def from_grid_coordinates(chunks, chunk_size, i, j):
    '''
    >>> from_grid_coordinates([['012/345/678']], 3, 0, 0)
    '0'
    >>> from_grid_coordinates([['012/345/678']], 3, 1, 1)
    '4'
    >>> from_grid_coordinates([['01/67', '23/89', '45/ab'], ['cd/ij', 'ef/kl', 'gh/mn'], ['op/uv', 'qr/wx', 'st/yz']], 2, 2, 2)
    'e'
    '''
    ci, cj = i // chunk_size, j // chunk_size
    chunk = chunks[ci][cj]
    cij_i = i % chunk_size
    cij_j = j % chunk_size
    offset = cij_i * (chunk_size + 1) + cij_j
    return chunk[offset]

def reassemble_grid(chunks):
    chunk_size = chunks[0][0].count('/') + 1
    grid_size = chunk_size * len(chunks)
    return '/'.join(''.join(from_grid_coordinates(chunks, chunk_size, i, j)
                            for j in range(grid_size))
                            for i in range(grid_size))

def expand_grid(rules, grid):
    chunks = chunk_grid(grid)
    transformed_chunks = [[rules[c] for c in row] for row in chunks]
    return reassemble_grid(transformed_chunks)

def solve(rules, grid, total_repetitions):
    @cache
    def recurse(grid, repetitions):
        if repetitions == 0:
            return grid.count('#')
        chunks = chunk_grid(grid)
        expanded_chunks = (expand_grid(rules, chunk) for row in chunks for chunk in row)
        return sum(
            recurse(ec, repetitions -1)
            for ec in expanded_chunks
        )
    return recurse(grid, total_repetitions)

if __name__ == '__main__':
    raw_rules = list(map(str.strip, open(sys.argv[1]).readlines()))
    digested_rules = digest_rules(raw_rules)
    print(solve(digested_rules, STARTING_GRID, 5))
    print(solve(digested_rules, STARTING_GRID, 18))
