import sys
from dijkstra import dijkstra

HALLWAY_ROW = 1
AMPHIPODS = 'ABCD'
HALLWAY_SIDE = 2
COLUMN_WIDTH = 1
ROOMS_FIRST_ROW = HALLWAY_ROW + 1

PART_1_GOAL = (
'#############',
'#...........#',
'###A#B#C#D###',
'  #A#B#C#D#',
'  #########',
)

PART_2_GOAL = (
'#############',
'#...........#',
'###A#B#C#D###',
'  #A#B#C#D#',
'  #A#B#C#D#',
'  #A#B#C#D#',
'  #########',
)

def amphipod_index(amphipod):
    return ord(amphipod) - ord('A')

def parse(input):
    return tuple(map(str.rstrip, input))

def distance(state, start, end):
    '''
    >>> distance([
    ... '#############',
    ... '#...........#',
    ... '###A#B#C#D###',
    ... '  #A#B#C#D#',
    ... '  #########',
    ... ], (2, 3), (1, 11))
    9
    >>> distance([
    ... '#############',
    ... '#.B.......C..#',
    ... '###A#.#.#D###',
    ... '  #A#.#B#D#',
    ... '  #########',
    ... ], (3, 7), (3, 5))
    6
    >>> distance([
    ... '#############',
    ... '#.....C.....#',
    ... '###A#B#.#D###',
    ... '  #A#B#C#D#',
    ... '  #########',
    ... ], (2, 3), (1, 11))
    >>> distance([
    ... '#############',
    ... '#.....C.....#',
    ... '###A#B#.#D###',
    ... '  #A#B#C#D#',
    ... '  #########',
    ... ], (3, 3), (1, 1))
    >>> distance([
    ... '#############',
    ... '#.....C.....#',
    ... '###A#C#B#D###',
    ... '  #A#B#.#D#',
    ... '  #########',
    ... ], (3, 3), (3, 7))
    '''
    start_i, start_j = start
    end_i, end_j = end

    for j in range(min(start_j, end_j)+1, max(start_j, end_j)):
        if state[HALLWAY_ROW][j] != '.':
            return None
    
    for i in range(HALLWAY_ROW, start_i):
        if state[i][start_j] != '.':
            return None

    for i in range(HALLWAY_ROW, end_i):
        if state[i][end_j] != '.':
            return None

    return (start_i - HALLWAY_ROW) + abs(end_j - start_j) + (end_i - HALLWAY_ROW)

def update_state(state, start, end):
    '''
    >>> update_state((
    ... '#############',
    ... '#.B.......C.#',
    ... '###A#.#.#D###',
    ... '  #A#.#B#D#',
    ... '  #########',
    ... ), (3, 7), (3, 5))
    ['#############', '#.B.......C.#', '###A#.#.#D###', '  #A#B#.#D#', '  #########']
    '''
    si, sj = start
    ei, ej = end
    mutable = [list(row) for row in state]
    mutable[si][sj], mutable[ei][ej] = '.', mutable[si][sj]
    return tuple(
        ''.join(row) for row in mutable
    )

def get_burrow_column(amphipod_index):
    return COLUMN_WIDTH + HALLWAY_SIDE + amphipod_index * 2

def try_burrow(state, amphipod, start):
    '''
    >>> try_burrow([
    ... '#############',
    ... '#.B.......C.#',
    ... '###A#.#.#D###',
    ... '  #A#.#B#D#',
    ... '  #########',
    ... ], 'B', (3, 7))
    (60, ['#############', '#.B.......C.#', '###A#.#.#D###', '  #A#B#.#D#', '  #########'])
    >>> try_burrow([
    ... '#############',
    ... '#.B.........#',
    ... '###A#.#.#D###',
    ... '  #A#C#B#D#',
    ... '  #########',
    ... ], 'B', (3, 7))
    '''
    start_i, start_j = start
    index = amphipod_index(amphipod)
    end_j = get_burrow_column(index)
    if start_j == end_j:
        return
    for end_i in reversed(range(ROOMS_FIRST_ROW, len(state) - 1)):
        if state[end_i][end_j] == '.':
            end = (end_i, end_j)
            d = distance(state, start, end)
            if d:
                unit_cost = 10 ** index
                return d * unit_cost, update_state(state, start, end)
        elif state[end_i][end_j] != amphipod:
            return

def to_hallway_states(state, amphipod, start):
    _start_i, start_j = start
    index = amphipod_index(amphipod)
    burrow_column = get_burrow_column(index)

    # already in its final position
    if burrow_column == start_j and all(row[burrow_column] in '.#'+amphipod for row in state):
        return

    unit_cost = 10 ** index
    for j, h in enumerate(state[HALLWAY_ROW]):
        if h == '.' and state[HALLWAY_ROW+1][j] == '#':
            end = HALLWAY_ROW, j
            d = distance(state, start, end)
            if d:
                yield d * unit_cost, update_state(state, start, end)

def next_states(state):
    # if an amphipod can go to its burrow, no need to explore more states
    for i in range(HALLWAY_ROW, len(state)):
        row = state[i]
        for j, amphipod in enumerate(row):
            if amphipod in AMPHIPODS:
                s = try_burrow(state, amphipod, (i, j))
                if s:
                    yield s
                    return
    # we need to explore all possibilities that can go to hallway
    for i in range(HALLWAY_ROW+1, len(state)):
        row = state[i]
        for j, amphipod in enumerate(row):
            if amphipod in AMPHIPODS:
                yield from to_hallway_states(state, amphipod, (i, j))

def exhaustive_search(state, goal, neighbors, total_cost=0):
    if state == goal:
        yield total_cost, state
        return
    for cost, neighbor in neighbors(state):
        yield from exhaustive_search(neighbor, goal, neighbors, total_cost + cost)

def part_1(input):
    # return min(exhaustive_search(input, PART_1_GOAL, next_states), default=None)
    return dijkstra(input, PART_1_GOAL, next_states)

def part_2(input):
    EXTRA_ROOMS = (
        '  #D#C#B#A#',
        '  #D#B#A#C#',
    )
    start = input[0:ROOMS_FIRST_ROW+1] + EXTRA_ROOMS + input[ROOMS_FIRST_ROW + len(EXTRA_ROOMS) - 1:]
    return dijkstra(start, PART_2_GOAL, next_states)

if __name__ == '__main__':
    problem_input = parse(sys.stdin)
    print(part_1(problem_input))
    print(part_2(problem_input))
