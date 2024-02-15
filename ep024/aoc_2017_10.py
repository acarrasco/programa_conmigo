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

def part_1(input):
    lengths = list(map(int, input.strip().split(',')))
    a, b, *_ = knot_hash(range(256), lengths)
    return a * b
    

if __name__ == '__main__':
    input = open('input.txt').readline().strip()
    print(part_1(input))
    print(full_hash(input))