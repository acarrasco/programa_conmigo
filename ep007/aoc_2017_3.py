import sys

input = int(sys.argv[1])

SPIRAL_ORDER = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
]

ADJACENCY = [(i, j) for i in (-1,0,1) for j in (-1, 0, 1) if i or j]

def generate_indices():
    direction_index = 0

    i = 0
    j = 0
    n = 1

    layer = 0

    yield i, j
    while True:
        di, dj = SPIRAL_ORDER[direction_index]
        
        next_i, next_j = i + di, j + dj
        if abs(next_i) > layer or abs(next_j) > layer:
            direction_index = (direction_index + 1) % 4
            if direction_index == 0:
                layer += 1
        else:
            n += 1
            i, j = next_i, next_j
            yield i, j

# part 1
it = iter(generate_indices())
for _ in range(input):
    i, j = next(it)

print(abs(i) + abs(j))

# part 2

memory = {
    (0, 0): 1,
}
n = 1
it = iter(generate_indices())
next(it)
while n < input:
    i, j = next(it)
    n = sum(memory.get((i + di, j + dj), 0) for di, dj in ADJACENCY)
    memory[i, j] = n

print(n)