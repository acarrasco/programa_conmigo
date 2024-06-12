import sys

def solve(urinals):
    '''
    n = len(urinals)
    complexity = O(n*n*n*log(n))
    '''
    def key(i):
        occupied_urinals = ((j, v) for (j, v) in enumerate(urinals) if v == '1')
        distances_to_occupied = sorted(abs(i-j) for j, v in occupied_urinals)
        return distances_to_occupied, i
    empty_urinal_indices = (i for i, u in enumerate(urinals) if u=='0')
    return max(empty_urinal_indices, default='N/A', key=key)

if __name__ == '__main__':
    for line in sys.stdin:
        print(solve(line.strip()))
