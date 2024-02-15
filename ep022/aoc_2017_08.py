from collections import namedtuple, defaultdict
import operator


Instruction = namedtuple('Instruction', ['register', 'operation', 'immediate', 'condition_register', 'comparator', 'condition_value'])

COMPARATORS = {
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
}

OPERATORS = {
    'inc': operator.add,
    'dec': operator.sub,
}

def parse_instruction(line):
    change, condition = line.split(' if ')
    register, operation, immediate = change.split()
    condition_register, comparator, condition_value = condition.split()
    return Instruction(register, operation, int(immediate), condition_register, comparator, int(condition_value))

def execute_instruction(registers, instruction):
    register, operation, immediate, condition_register, comparator, condition_value = instruction
    condition_register_value = registers[condition_register]
    if COMPARATORS[comparator](condition_register_value, condition_value):
        result = OPERATORS[operation](registers[register], immediate)
        registers[register] = result
        return result
    
def part_1(instructions):
    registers = defaultdict(int)
    for instruction in instructions:
        execute_instruction(registers, instruction)
    return max(registers.values())

def part_2(instructions):
    registers = defaultdict(int)
    instruction_results = (execute_instruction(registers, instruction) for instruction in instructions)
    return max(filter(lambda x: x is not None, instruction_results))

if __name__ == '__main__':
    input = open('input.txt')
    instructions = list(map(parse_instruction, input))
    print(part_1(instructions))
    print(part_2(instructions))
