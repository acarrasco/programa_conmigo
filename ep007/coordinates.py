import math

SPIRAL_ORDER = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
]

# generative method

def generate_indices():
    direction_index = 0

    i = 0
    j = 0
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
            i, j = next_i, next_j
            yield i, j

# analytical method

def get_layer(n):
    return math.ceil((n ** 0.5 - 1) / 2)

def get_spiral_coordinates(n):
    layer = get_layer(n) 
    if layer == 0:
        return 0, 0

    layer_side = (2 * layer + 1)
    bottom_right_corner = layer_side * layer_side
    distance_to_corner = bottom_right_corner - n
    side = distance_to_corner // (layer_side - 1)
    side_offset = distance_to_corner % (layer_side - 1)

    if side == 0: # bottom
        return layer, layer - side_offset
    elif side == 1: # left
        return layer - side_offset, -layer
    elif side == 2: # top
        return -layer, -layer + side_offset
    elif side == 3: # right
        return -layer + side_offset, layer
    else:
        raise "oops"

def test_get_layer():
    for layer in range(1, 5):
        a = 2 * (layer-1) + 1
        b = 2 * layer + 1
        for i in range(a*a+1, b*b+1):
            result = get_layer(i)
            if result != layer:
                print(i, layer, result)

def test_calculate_coordinates():
    it = iter(generate_indices())
    for n in range(1, 100):
        expected = next(it)
        result = get_spiral_coordinates(n)
        if result != expected:
            print(n, expected, result)

def print_points(points, missing='.'):
    max_h, _ = max(points)
    _, max_w = max(points, key=lambda p: p[1])
    min_h, _ = min(points)
    _, min_w = min(points, key=lambda p: p[1])

    for i in range(min_h, max_h+1):
        row = (points.get((i, j), missing) for j in range(min_w, max_w+1))
        yield ','.join(str(v) for v in row) + '\n'

test_get_layer()
test_calculate_coordinates()

SPIRAL_LAYER = 12
SPIRAL_SIZE = SPIRAL_LAYER ** 2

with open("spiral_one_based.csv", "w") as file:
    one_based_spiral = {p: n + 1 for n, p in zip(range(SPIRAL_SIZE), generate_indices())}
    file.writelines(print_points(one_based_spiral))

with open("sqn_one_based_floating.csv", "w") as file:
    layers = {p: "{:.2f}".format(n ** 0.5) for p, n in one_based_spiral.items()}
    file.writelines(print_points(layers))

with open("sqn_one_based_int.csv", "w") as file:
    layers = {p: "{}".format(int(n ** 0.5)) for p, n in one_based_spiral.items()}
    file.writelines(print_points(layers))

