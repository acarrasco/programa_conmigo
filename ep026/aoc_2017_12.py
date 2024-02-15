def parse_line(line):
    left, right =  line.split('<->')
    right = tuple(int(x) for x in right.split(','))
    return int(left), right

def update_sets(old_sets, new_set):
    for s in old_sets:
        if s & new_set:
            new_set.update(s)
        else:
            yield s
    yield new_set

def solve(input):
    sets = []
    for left, right in input:
        current = set(right)
        current.add(left)
        sets = list(update_sets(sets, current))

    part_2 = len(sets)
    for s in sets:
        if 0 in s:
            return len(s), part_2

if __name__ == '__main__':
    input = list(map(parse_line, open('input.txt')))
    part_1, part_2 = solve(input)
    print(part_1)
    print(part_2)
