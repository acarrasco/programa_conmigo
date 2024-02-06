from functools import reduce

SYMBOL_TO_DIRECTION = {
    '(': 1,
    ')': -1,
}

instructions = open("input.txt").readline().strip()
directions = list(map(SYMBOL_TO_DIRECTION.get, instructions))

# part 1
def add(a, b):
    return a + b

floor = reduce(add, directions)
print(floor)

# part 2

def accumulate_floors(floors, direction):
    last_floor = floors[-1]
    return floors + [last_floor + direction]

floors = reduce(accumulate_floors, directions, [0])
basement_index = floors.index(-1)

print(basement_index)