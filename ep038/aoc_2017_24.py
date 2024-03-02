import functools
import sys

def parse_component(line):
    a, b = sorted(map(int, line.split('/')))
    return a, b

components = sorted(map(parse_component, open(sys.argv[1])))

def best_bridge(components, metric):
    @functools.cache
    def substructure(right_port, remaining):
        candidates = []
        for i, (a, b) in enumerate(remaining):
            if a == right_port:
                next_remaining = remaining[:i] + remaining[i+1:]
                length, strength = substructure(b, next_remaining)
                candidates.append((length + 1, strength + a + b))
            if b == right_port:
                next_remaining = remaining[:i] + remaining[i+1:]
                length, strength = substructure(a, next_remaining)
                candidates.append((length + 1, strength + a + b))
        return max(candidates, default=(0, 0), key=metric)
    _length, strength = substructure(0, tuple(components))
    return strength

print(best_bridge(components, lambda length_and_strength: length_and_strength[1]))
print(best_bridge(components, lambda length_and_strength: length_and_strength))