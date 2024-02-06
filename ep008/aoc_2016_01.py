input = open("input.txt").readline()
instructions_txt = input.strip().split(", ")

def parse_instruction(instruction_txt):
    turn = instruction_txt[0]
    distance = int(instruction_txt[1:])
    return (turn, distance)

instructions = [parse_instruction(i) for i in instructions_txt]

NORTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)
SOUTH = (-1, 0)

TURNS = {
    NORTH: {
        'R': EAST,
    },
    EAST: {
        'R' : SOUTH,
    },
    SOUTH: {
        'R': WEST,
    },
    WEST: {
        'R': NORTH,
    }
}
for bearing in TURNS:
    right = TURNS[bearing]['R']
    TURNS[right]['L'] = bearing


def jump(position, bearing, instruction):
    turn, distance = instruction
    new_bearing = TURNS[bearing][turn]
    x, y = position
    dx, dy = new_bearing
    new_position = x + dx * distance, y + dy * distance
    return new_position, new_bearing


# part 1

def solve_1():
    bearing = (1, 0)
    position = (0, 0)

    for instruction in instructions:
        position, bearing = jump(position, bearing, instruction)

    return abs(position[0]) + abs(position[1])

print(solve_1())

# part 2

def walk(position, bearing, instruction):
    turn, distance = instruction
    new_bearing = TURNS[bearing][turn]
    x, y = position
    dx, dy = new_bearing
    for _ in range(distance):
        x, y = x + dx, y + dy
        yield (x, y), new_bearing

def solve_2():
    bearing = (1, 0)
    position = (0, 0)
    visited = set()

    for instruction in instructions:
        for position, bearing in walk(position, bearing, instruction):
            if position in visited:
                return abs(position[0]) + abs(position[1])
            visited.add(position)

print(solve_2())