import argparse
import copy

CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3

def parse_input(lines):
    '''
    >>> {(-1, -1): '#', (0, 1): '#'} == parse_input(['#..', '..#', '...'])
    True
    '''
    infected = []
    for i, row in enumerate(lines):
        for j, node in enumerate(row):
            if node == '#':
                infected.append((i, j))
    mi, mj = i // 2, j // 2
    return {(i - mi, j - mj): INFECTED for i, j in infected}

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

DIRECTION = [UP, RIGHT, DOWN, LEFT]

RIGHT_TURN = 1
LEFT_TURN = -1

class NodesState:
    def __init__(self, input):
        self.state = parse_input(input)

    def set_state(self, position, state):
        if state == CLEAN:
            del self.state[position]
        else:
            self.state[position] = state

    def get_state(self, position):
        return self.state.get(position, CLEAN)


class VirusCarrier:
    REVERSE = 2
    DO_NOT_TURN = 0

    STATE_TO_DIRECTION_OFFSET = {
        CLEAN: LEFT_TURN,
        INFECTED: RIGHT_TURN,
        WEAKENED: DO_NOT_TURN,
        FLAGGED: REVERSE,
    }

    def next_direction_offset(self, node_state):
        return self.STATE_TO_DIRECTION_OFFSET[node_state]

    def __init__(self):
        self.i = 0
        self.j = 0
        self.direction_idx = DIRECTION.index(UP)

    def advance(self):
        di, dj = DIRECTION[self.direction_idx]
        self.i += di
        self.j += dj

    def burst(self, nodes):
        current_coordinates = self.i, self.j
        current_state = nodes.get_state(current_coordinates)
        self.direction_idx = self.next_direction(current_state)
        next_state = self.next_state(current_state)
        nodes.set_state(current_coordinates, next_state)
        self.advance()
        return next_state == INFECTED

    def next_direction(self, node_state):
        offset = self.next_direction_offset(node_state)
        return (self.direction_idx + offset) % 4

    def next_direction_offset(self, node_state):
        return self.STATE_TO_DIRECTION_OFFSET[node_state]
    
    def next_state(self, node_state):
        raise 'Not implemented'


class PartOneCarrier(VirusCarrier):
    def next_state(self, node_state):
        return (node_state + 2) % 4


class PartTwoCarrier(VirusCarrier):
    def next_state(self, node_state):
        return (node_state + 1) % 4


def solve(nodes, carrier, iterations):
    nodes = copy.deepcopy(nodes)    
    return sum(carrier.burst(nodes) for _ in range(iterations))

if __name__ == '__main__':
    parser = argparse.ArgumentParser('aoc 2017 22')
    parser.add_argument('-inputfile', default='input.txt', type=argparse.FileType())
    parser.add_argument('-partonebursts', default=10000, type=int)
    parser.add_argument('-parttwobursts', default=10000000, type=int)
    args = parser.parse_args()

    nodes_state = NodesState(args.inputfile)

    print(solve(nodes_state, PartOneCarrier(), args.partonebursts))
    print(solve(nodes_state, PartTwoCarrier(), args.parttwobursts))
