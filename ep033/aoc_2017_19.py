import sys

ADJACENCY = [
    (-1, 0), (1, 0), (0, -1), (0, 1)
]

def turning_directions(direction):
    vi, vj = direction
    for di, dj in ADJACENCY:
        if vi * di + vj * dj == 0:
            yield di, dj

def next_position(diagram, i, j, direction):
    if diagram[i][j] == '+':
        for di, dj in turning_directions(direction):
            if diagram[i+di][j+dj] != ' ':
                return (i + di, j + dj), (di, dj)
    else:
        di, dj = direction
        return (i + di, j + dj), direction

def part_1_and_2(diagram):
    letters = []
    i, j = 0, diagram[0].index('|')
    direction = (1, 0)
    steps = 0
    while diagram[i][j] != ' ':
        # print(i, j, diagram[i][j])
        if diagram[i][j].isalpha():
            letters.append(diagram[i][j])
        (i, j), direction = next_position(diagram, i, j, direction)
        steps += 1
    return ''.join(letters), steps


if __name__ == '__main__':
    diagram = open(sys.argv[1]).readlines()
    for result in part_1_and_2(diagram):
        print(result)
