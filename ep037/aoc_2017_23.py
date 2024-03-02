import sys
from itertools import count

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

class Program:
    def __init__(self, instructions, initial_values={}, trace=False):
        self.trace = trace
        self.instructions = instructions
        self.pc = 0
        self.registers = {chr(i): 0 for i in range(ord('a'), ord('i'))}
        self.registers.update(initial_values)
        self.times_mul = 0

    def evaluate(self, x):
        if isinstance(x, int):
            return x
        return self.registers[x]
    
    def step(self):
        if not(0 <= self.pc < len(self.instructions)):
            return self.times_mul, self.registers
        instruction = self.instructions[self.pc]
        j = 1
        match instruction:
            case 'snd', x:
                self.last_frequency = self.evaluate(x)
            case 'set', x, y:
                self.registers[x] = self.evaluate(y)
            case 'add', x, y:
                self.registers[x] += self.evaluate(y)
            case 'sub', x, y:
                self.registers[x] -= self.evaluate(y)
            case 'mul', x, y:
                self.registers[x] *= self.evaluate(y)
                self.times_mul += 1
            case 'mod', x, y:
                self.registers[x] %= self.evaluate(y)
            case 'jnz', x, y:
                if self.trace:
                    print(f'trace pc={self.pc}, {" ".join(f"{r}={v}" for r, v in self.registers.items())}')
                if self.evaluate(x) != 0:
                    j = self.evaluate(y)
        self.pc += j

def execute(instructions, initial_values={}, trace=False):
    program = Program(instructions, initial_values, trace)
    steps_sequence = (program.step() for _ in count())
    non_null_steps = filter(None, steps_sequence)
    return next(non_null_steps)


def is_prime(n):
    sqn = int(n**0.5)
    for i in range(2, sqn):
        if n % i == 0:
            return False
    return True

if __name__ == '__main__':
    instructions = list(map(parse_instruction, open(sys.argv[1])))
    part_1_times_mul, _ = execute(instructions)
    print(part_1_times_mul)

    _, registers = execute(instructions[:10], {'a': 1})
    first = registers['b']
    last = registers['c']

    _, registers = execute(instructions[-2:-1])
    step = registers['b']
    
    part_2 = sum(not is_prime(i) for i in range(first, last + 1, step))
    print(part_2)
