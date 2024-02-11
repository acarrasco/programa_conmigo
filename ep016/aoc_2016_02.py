from itertools import chain, batched

input = [list(map(int, line.split())) for line in open('input.txt')]

def is_triangle(sides):
    a, b, c = sorted(sides)
    return a + b > c

print(sum(map(is_triangle, input)))

by_columns = zip(*input)
all_sides = chain(*by_columns)

print(sum(is_triangle(sides) for sides in batched(all_sides, 3)))
