
jumps = [int(line) for line in open("input.txt")]

def solve_generic(jumps, next_jump_offest):
    jumps = jumps[:]
    pc = 0
    steps = 0
    while 0 <= pc < len(jumps):
        jumps[pc], pc = next_jump_offest(jumps[pc]), pc + jumps[pc]
        steps += 1
    return steps

def part_1(jumps):
    return solve_generic(jumps, lambda j: j + 1)

def part_2(jumps):
    return solve_generic(jumps, lambda j: j -1 if j >= 3 else j + 1)

def part_2_opt(jumps):
    pc = 0
    steps = 0
    size = len(jumps);
    while pc >= 0 and pc < size:
        j = jumps[pc]
        if j >= 3:
            jumps[pc] -= 1
        else:
            jumps[pc] += 1
        pc += j;
        steps += 1
    return steps

print(part_1(jumps))
print(part_2(jumps))
# print(part_2_opt(jumps))