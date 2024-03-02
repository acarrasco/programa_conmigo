import sys
from itertools import count
from collections import defaultdict, deque

def try_parse_int(text):
    try:
        return int(text)
    except:
        return text

def parse_instruction(line):
    tokens = line.split()
    return tuple(map(try_parse_int, tokens))

BLOCKED = 'blocked'
FINISHED = 'finished'

class Program1:
    def __init__(self, instructions):
        self.instructions = instructions
        self.pc = 0
        self.registers = defaultdict(int)
        self.last_frequency = None

    def evaluate(self, x):
        if isinstance(x, int):
            return x
        return self.registers[x]
    
    def step(self):
        if not(0 <= self.pc < len(self.instructions)):
            return
        instruction = self.instructions[self.pc]
        j = 1
        match instruction:
            case 'snd', x:
                self.last_frequency = self.evaluate(x)
            case 'set', x, y:
                self.registers[x] = self.evaluate(y)
            case 'add', x, y:
                self.registers[x] += self.evaluate(y)
            case 'mul', x, y:
                self.registers[x] *= self.evaluate(y)
            case 'mod', x, y:
                self.registers[x] %= self.evaluate(y)
            case 'rcv', x:
                return self.last_frequency
            case 'jgz', x, y:
                if self.evaluate(x) > 0:
                    j = self.evaluate(y)
        self.pc += j

class Program2:
    def __init__(self, instructions, pid, queues):
        self.instructions = instructions
        self.pid = pid
        self.queues = queues
        self.pc = 0
        self.registers = defaultdict(int)
        self.registers['p'] = pid
        self.times_sent = 0

    def evaluate(self, x):
        if isinstance(x, int):
            return x
        return self.registers[x]
    
    def inbox(self):
        return self.queues[self.pid]
    
    def outbox(self):
        return self.queues[self.pid ^ 1]

    def step(self):
        if not(0 <= self.pc < len(self.instructions)):
            return FINISHED
        instruction = self.instructions[self.pc]
        j = 1

        match instruction:
            case 'snd', x:
                self.outbox().append(self.evaluate(x))
                self.times_sent += 1
            case 'set', x, y:
                self.registers[x] = self.evaluate(y)
            case 'add', x, y:
                self.registers[x] += self.evaluate(y)
            case 'mul', x, y:
                self.registers[x] *= self.evaluate(y)
            case 'mod', x, y:
                self.registers[x] %= self.evaluate(y)
            case 'rcv', x:
                if self.inbox():
                    self.registers[x] = self.inbox().popleft()
                else:
                    return BLOCKED
            case 'jgz', x, y:
                if self.evaluate(x) > 0:
                    j = self.evaluate(y)
        self.pc += j


def part_1(instructions):
    program = Program1(instructions)
    steps_sequence = (program.step() for _ in count())
    non_null_steps = filter(None, steps_sequence)
    return next(non_null_steps)

def part_2(instructions):
    queues = [deque(), deque()]
    p0 = Program2(instructions, 0, queues)
    p1 = Program2(instructions, 1, queues)

    while True:
        r0 = p0.step()
        r1 = p1.step()
        if r0 and r1:
            return p1.times_sent

if __name__ == '__main__':
    instructions = list(map(parse_instruction, open(sys.argv[1])))
    print(part_1(instructions))
    print(part_2(instructions))
