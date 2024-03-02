import sys
from collections import deque

def simulate(skip, steps):
    '''
    >>> simulate(1, 1)
    deque([0])

    >>> simulate(3, 2)
    deque([1, 0])

    >>> simulate(3, 3)
    deque([2, 1, 0])

    >>> simulate(3, 10)
    deque([9, 5, 7, 2, 4, 3, 8, 6, 1, 0])
    '''
    buffer = deque()
    for i in range(steps):
        buffer.rotate(-skip-1)
        buffer.appendleft(i)
        # bc = deque(buffer)
        # zi = bc.index(0)
        # bc.rotate(-zi)
        # print(bc)
    return buffer

def part_1(skip):
    buffer = simulate(skip, 2018)
    return buffer[1]

def part_2(skip, steps):
    current_position = 0
    last_value_after_zero = 0
    for i in range(1, steps):
        current_position = (current_position + skip) % (i)
        if current_position == 0:
            last_value_after_zero = i
        current_position += 1
    return last_value_after_zero

def test_part_2(skip, steps):
    brute_force_buffer = simulate(skip, steps)
    zero_index = brute_force_buffer.index(0)
    expected = brute_force_buffer[(zero_index + 1) % (steps)]
    result = part_2(skip, steps)
    print(expected, result)

if __name__ == '__main__':
    input = int(sys.argv[1])
    print(part_1(input))
    # test_part_2(377, 1)
    # test_part_2(377, 2)
    # test_part_2(377, 3)
    # test_part_2(377, 100)
    # test_part_2(377, 1000)
    # test_part_2(377, 2000)
    # test_part_2(377, 40000)
    print(part_2(input, 50000000))