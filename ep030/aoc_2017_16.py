
def step(dancers, movement):
    '''
    >>> step(list('abcde'), 's3')
    ['c', 'd', 'e', 'a', 'b']

    >>> step(list('abcde'), 'x3/4')
    ['a', 'b', 'c', 'e', 'd']

    >>> step(list('abcde'), 'pd/e')
    ['a', 'b', 'c', 'e', 'd']
    '''
    m, args = movement[0], movement[1:]
    match m, args:
        case 's', n:
            n = int(n)
            return dancers[-n:] + dancers[:len(dancers)-n]
        case 'x', params:
            i, j = map(int, params.split('/'))
            dancers = dancers[:]
            dancers[i], dancers[j] = dancers[j], dancers[i]
            return dancers
        case 'p', params:
            elements = params.split('/')
            i, j = map(dancers.index, elements)
            dancers = dancers[:]
            dancers[i], dancers[j] = dancers[j], dancers[i]
            return dancers

def parse_input(line):
    dance_moves = line.split(',')
    return dance_moves

def dance(dancers, dance_moves):
    for dance_move in dance_moves:
        dancers = step(dancers, dance_move)
    return ''.join(dancers)

DANCE_REPETITIONS = 10**9
def part_2(dancers, dance_moves):
    previous_arrangements = {}
    dancers = ''.join(dancers)
    for i in range(DANCE_REPETITIONS):
        if dancers in previous_arrangements:
            break
        previous_arrangements[dancers] = i
        dancers = dance(list(dancers), dance_moves)
    loop_start = previous_arrangements[dancers]
    loop_size = i - loop_start
    final_dance_index = DANCE_REPETITIONS % loop_size
    for dancers, index in previous_arrangements.items():
        if index == final_dance_index:
            return dancers

if __name__ == '__main__':
    dance_moves = parse_input(open('input.txt').readline())
    dancers = [chr(i) for i in range(ord('a'), ord('p')+1)]
    print(dance(dancers, dance_moves))
    print(part_2(dancers, dance_moves))
