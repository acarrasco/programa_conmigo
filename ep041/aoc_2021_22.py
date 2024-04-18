import sys
from collections import namedtuple
from itertools import product
from functools import cache

Step = namedtuple('Step', ['status', 'x', 'y', 'z'])

def parse_region(region):
    axis, boundaries = region.split('=')
    start, end = boundaries.split('..')
    return axis, (int(start), int(end))

def parse_line(line):
    '''
    >>> parse_line('on x=-20..26,y=-36..17,z=-47..7')
    Step(status='on', x=(-20, 26), y=(-36, 17), z=(-47, 7))
    '''
    status, cuboid = line.split()
    return Step(status=status, **dict(map(parse_region, cuboid.split(','))))

def constrained_range(start, end):
    constrained_start = max(-50, start)
    constrained_end = min(50, end)
    return range(constrained_start, constrained_end + 1)

def part_1(steps):
    on_cubes = set()
    for step in steps:
        for xyz in product(
            constrained_range(*step.x),
            constrained_range(*step.y),
            constrained_range(*step.z)
        ):
            if step.status == 'on':
                on_cubes.add(xyz)
            else:
                on_cubes.discard(xyz)
    return len(on_cubes)


class EmptySet:
    def __len__(self):
        return 0
    def __and__(self, other):
        return self
    def __or__(self, other):
        return other
    def __sub__(self, other):
        return self
    def __str__(self):
        return f'∅'
EMPTY = EmptySet()

cardinality_cache = {}

@cache
def union(a, b):
    return Union(a, b)

@cache
def difference(a, b):
    return Difference(a, b)

@cache
def intersection(a, b):
    return a & b

class BaseSet:
    def __init__(self):
        self._len = None
    def __or__(self, other):
        if other is EMPTY:
            return self
        return union(self, other)
    def __sub__(self, other):
        if other is EMPTY:
            return self
        return difference(self, other)
    def __len__(self):
        k = self
        if k not in cardinality_cache:
            cardinality_cache[k] = self.cardinality()
        return cardinality_cache[k]

class Union(BaseSet):
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b
    def cardinality(self):
        return len(self.a) + len(self.b) - len(intersection(self.a, self.b))
    def __and__(self, other):
        if other is EMPTY:
            return EMPTY
        a_and_o = intersection(self.a, other)
        b_and_o = intersection(self.b, other)
        if a_and_o is EMPTY:
            return b_and_o
        elif b_and_o is EMPTY:
            return a_and_o
        return union(a_and_o, b_and_o)
    def __str__(self):
        return f'({self.a}|{self.b})'

class Difference(BaseSet):
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b
    def cardinality(self):
        return len(self.a) - len(intersection(self.a, self.b))
    def __and__(self, other):
        if other is EMPTY:
            return EMPTY
        return difference(intersection(self.a, other), self.b)
    def __str__(self):
        return f'({self.a}-{self.b})'

def size(region):
    start, end = region
    return (end + 1 - start)

def range_intersection(a, b):
    '''
    >>> intersection((0, 10), (20, 30))
    >>> intersection((20, 30), (0, 10))
    >>> intersection((0, 10), (10, 20))
    (10, 10)
    >>> intersection((0, 10), (5, 20))
    (5, 10)
    >>> intersection((5, 20), (0, 10))
    (5, 10)
    >>> intersection((0, 20), (5, 15))
    (5, 15)
    >>> intersection((5, 15), (0, 20))
    (5, 15)
    '''
    if a > b:
        a, b = b, a
    a0, a1 = a
    b0, b1 = b
    if a1 < b0:
        return None
    return max(a0, b0), min(a1, b1)

class Cuboid(BaseSet):
    def __init__(self, x, y, z):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
    def cardinality(self):
        return size(self.x) * size(self.y) * size(self.z)
    def __and__(self, other):
        if other is EMPTY:
            return EMPTY
        ix = range_intersection(self.x, other.x)
        iy = range_intersection(self.y, other.y)
        iz = range_intersection(self.z, other.z)
        if ix and iy and iz:
            return Cuboid(ix, iy, iz)
        else:
            return EMPTY
    def __str__(self):
        return f'<x={self.x},y={self.y},z={self.z}>'

def part_2(steps):
    cubes = EMPTY
    for step in steps:
        c = Cuboid(step.x, step.y, step.z)
        if step.status == 'on':
            cubes = union(cubes, c)
        else:
            cubes = difference(cubes, c)
    return len(cubes)

if __name__ == '__main__':
    steps = list(map(parse_line, sys.stdin))
    print(part_1(steps))
    print(part_2(steps))