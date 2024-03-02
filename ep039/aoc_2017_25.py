def parse_rules(lines):
    for line in lines:
        if line.startswith('In state'):
            state = line[-2]
        elif 'If the current value is' in line:
            read_value = int(line[-2])
        elif 'Write the value' in line:
            write_value = int(line[-2])
        elif 'Move one slot to the right' in line:
            direction = 1
        elif 'Move one slot to the left' in line:
            direction = -1
        elif 'Continue with state' in line:
            next_state = line[-2]
            yield state, read_value, write_value, direction, next_state

def group_rules(parsed_rules):
    return {(state, read_value): (write_value, direction, next_state) for 
            state, read_value, write_value, direction, next_state in parsed_rules }

def parse_blueprints(lines):
    rules_lines = lines[3:]
    grouped_rules = group_rules(parse_rules(rules_lines))
    initial_state = lines[0][-2]
    checksum_steps = int(lines[1].split()[-2])
    return initial_state, grouped_rules, checksum_steps

class TuringMachine:
    def __init__(self, initial_state, rules):
        self.state = initial_state
        self.rules = rules
        self.tape = set()
        self.head = 0
    
    def read(self):
        return int(self.head in self.tape)

    def write(self, value):
        if value:
            self.tape.add(self.head)
        else:
            self.tape.discard(self.head)

    def move_head(self, direction):
        self.head += direction

    def step(self):
        rule = self.rules[self.state, self.read()]
        write_value, direction, next_state = rule
        self.write(write_value)
        self.move_head(direction)
        self.state = next_state

def part_1():
    input = list(map(str.strip, open('input.txt')))
    initial_state, rules, steps = parse_blueprints(input)
    machine = TuringMachine(initial_state, rules)
    for _ in range(steps):
        machine.step()
    return len(machine.tape)

print(part_1())
