import sys

def try_parse_int(operand):
    try:
        return int(operand)
    except:
        return operand

def parse_instruction(line):
    op, a, b = line.split()
    return op, try_parse_int(a), try_parse_int(b)

def chunk_program(text):
    r'''
    >>> chunk_program('inp w\nadd x y\nsub w 1\ninp w\nmod z 2')
    ['add x y\nsub w 1\n', 'mod z 2']
    '''
    segments = list(filter(None, text.split('inp w\n')))
    return segments

def parse(text):
    chunks = chunk_program(text)
    result = []
    for chunk in chunks:
        lines = chunk.splitlines()
        result.append(list(map(parse_instruction, lines)))
    return result

def get_constants(chunk):
    _, _, k = chunk[3]
    _, _, l = chunk[4]
    _, _, m = chunk[14]
    return k, l, m

def solve(program_chunks):
    constants = []
    digits_part_1 = {}
    digits_part_2 = {}
    for i, chunk in enumerate(program_chunks):
        k, l, m = get_constants(chunk)
        if k == 1:
            constants.append((i, k, l, m))
        else:
            pi, pk, pl, pm = constants.pop()
            # pw + pm + l = w
            d = pm + l
            if d > 0:
                pw_pt1 = 9 - d
                w_pt1 = 9

                pw_pt2 = 1
                w_pt2 = 1 + d
            else:
                pw_pt1 = 9
                w_pt1 = 9 + d

                pw_pt2 = 1 - d
                w_pt2 = 1
            digits_part_1[i] = w_pt1
            digits_part_1[pi] = pw_pt1

            digits_part_2[i] = w_pt2
            digits_part_2[pi] = pw_pt2

    part_1 = ''.join(str(v) for k, v in sorted(digits_part_1.items()))
    part_2 = ''.join(str(v) for k, v in sorted(digits_part_2.items()))
    return part_1, part_2


if __name__ == '__main__':
    input_text = sys.stdin.read()
    chunks = parse(input_text)
    part_1, part_2 = solve(chunks)
    print(part_1)
    print(part_2)