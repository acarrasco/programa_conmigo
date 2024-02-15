DIRECTIONS = {
    'n': (1, 0),
    'ne': (0, 1),
    'se': (-1, 1),
    's': (-1, 0),
    'sw': (0, -1),
    'nw': (1, -1),
}

def hex_distance(point):
    '''
    >>> hex_distance(walk('ne,ne,ne'.split(',')))
    3
    >>> hex_distance(walk('ne,ne,sw,sw'.split(',')))
    0
    >>> hex_distance(walk('ne,ne,s,s'.split(',')))
    2
    >>> hex_distance(walk('se,sw,se,sw,sw'.split(',')))
    3
    '''
    di, dj = point

    if di * dj > 0:
        return abs(di) + abs(dj)
    else:
        return max(abs(di), abs(dj))
    
def walk(steps):
    i = 0
    j = 0
    for step in steps:
        di, dj = DIRECTIONS[step]
        i += di
        j += dj
        yield i, j

def part_1(input):
    for destination in walk(input):
        pass
    return hex_distance(destination)

def part_2(input):
    return max(map(hex_distance, walk(input)))

if __name__ == '__main__':
    input = open('input.txt').readline().strip().split(',')
    print(part_1(input))
    print(part_2(input))