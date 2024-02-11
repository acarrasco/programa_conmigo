from collections import defaultdict

DIRECTIONS = {
    '^': (1, 0),
    'v': (-1, 0),
    '>': (0, 1),
    '<': (0, -1),
}

input = open("input.txt").readline().strip()

def part_1(input):
    i = 0
    j = 0

    # we only needed a set, but I believed I was advancing work for part 2...
    gifts_per_house = defaultdict(lambda: 0)
    gifts_per_house[0, 0] = 1

    for direction in input:
        di, dj = DIRECTIONS[direction]
        i += di
        j += dj

        gifts_per_house[i, j] += 1

    return len(gifts_per_house)

def get_visited_houses(input):
    i = 0
    j = 0

    visited = set()
    visited.add((0, 0))

    for direction in input:
        di, dj = DIRECTIONS[direction]
        i += di
        j += dj
        visited.add((i, j))

    return visited

def part_2(input):
    santa_instructions = [d for i, d in enumerate(input) if i % 2 == 0]
    robot_instructions = [d for i, d in enumerate(input) if i % 2 == 1]
    visited = get_visited_houses(santa_instructions) | get_visited_houses(robot_instructions)
    return len(visited)

print(part_1(input))
print(part_2(input))