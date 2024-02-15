import sys

A_FACTOR = 16807
B_FACTOR = 48271
MODULO = 2147483647
SAMPLE_SIZE_PT1 = 40000000
SAMPLE_SIZE_PT2 = 5000000
MASK = 0xFFFF

def generate(start, factor, size, multiple_condition=1):
    previous = start
    generated = 0
    while generated < size:
        previous = (previous * factor) % MODULO
        if previous % multiple_condition == 0:
            yield previous
            generated += 1

def part_1(a_start, b_start):
    generator_a = generate(a_start, A_FACTOR, SAMPLE_SIZE_PT1)
    generator_b = generate(b_start, B_FACTOR, SAMPLE_SIZE_PT1)
    return sum(a&MASK == b&MASK for a, b in zip(generator_a, generator_b))

def part_2(a_start, b_start):
    generator_a = generate(a_start, A_FACTOR, SAMPLE_SIZE_PT2, 4)
    generator_b = generate(b_start, B_FACTOR, SAMPLE_SIZE_PT2, 8)
    return sum(a&MASK == b&MASK for a, b in zip(generator_a, generator_b))

def parse_input():
    a, b = open(sys.argv[1])
    return int(a.split()[-1]), int(b.split()[-1])

if __name__ == '__main__':
    a, b = parse_input()
    print(part_1(a, b))
    print(part_2(a, b))