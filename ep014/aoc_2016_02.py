MOVEMENTS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}

KEYPAD_PART_1 = [
    '123',
    '456',
    '789',
]

# def clamp(v, minimum, maximum):
#     '''
#     >>> clamp(10, 0, 5)
#     5
#     >>> clamp(3, -1, 4)
#     3
#     >>> clamp(-10, -5, 5)
#     -5
#     '''
#     if v < minimum:
#         return minimum
#     elif v > maximum:
#         return maximum
#     else:
#         return v

def solve_generic(keypad, start, can_move, instructions):
    i, j = start
    code = []
    for instruction in instructions:
        for movement in instruction:
            di, dj = MOVEMENTS[movement]
            if can_move(i + di, j + dj):
                i = i + di
                j = j + dj
        code.append(keypad[i][j])
    return ''.join(code)


def solve_1(instructions):
    '''
    >>> solve_1(['ULL','RRDDD','LURDL','UUUUD',])
    '1985'
    '''
    def can_move(i, j):
        return 0 <= i <= 2 and 0 <= j <= 2
    return solve_generic(KEYPAD_PART_1, (1, 1), can_move, instructions)

KEYPAD_PART_2 = [
    '       ',
    '   1   ',
    '  234  ',
    ' 56789 ',
    '  ABC  ',
    '   D   ',
    '       ',
]


def solve_2(instructions):
    '''
    >>> solve_2(['ULL','RRDDD','LURDL','UUUUD',])
    '5DB3'
    '''
    def can_move(i, j):
        return KEYPAD_PART_2[i][j] != ' '
    return solve_generic(KEYPAD_PART_2, (3, 1), can_move, instructions)

if __name__ == '__main__':
    instructions = [line.strip() for line in open('input.txt')]

    print(solve_1(instructions))
    print(solve_2(instructions))
