import sys
import itertools
import collections

class V:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f'V({self.x},{self.y},{self.z})'
    
    def __iter__(self):
        return iter((self.x, self.y, self.z))
    
    def __add__(self, other):
        ox, oy, oz = other
        return V(self.x + ox, self.y + oy, self.z + oz)
    
    def __sub__(self, other):
        ox, oy, oz = other
        return V(self.x - ox, self.y - oy, self.z - oz)
    
    def __eq__(self, other):
        return all(a == b for a, b in zip(self, other))
    
    def __hash__(self) -> int:
        return self.x + (self.y ** 5) % 52365 + self.z * 643763

def parse_line(line):
    clean_line = ''.join(c for c in line if c.isdigit() or c == '-' or c == ',')
    numbers = map(int, clean_line.split(','))
    p, v, a = itertools.starmap(V, itertools.batched(numbers, 3))
    return V(p, v, a)

def parse_input(lines):
    return [parse_line(line) for line in lines]

def part_1(particles):
    def abs_acceleration(index_and_particle):
        _idx, (_p, _v, a) = index_and_particle
        return sum(map(abs, a))

    idx, _ = min(enumerate(particles), key=abs_acceleration)
    return idx

def update(particle):
    '''
    >>> update(V(V(-6,0,0), V(3,0,0),V(0,0,0)))
    V(V(-3,0,0),V(3,0,0),V(0,0,0))

    >>> update(V(V(1,2,3), V(4,5,6),V(8,9,10)))
    V(V(13,16,19),V(12,14,16),V(8,9,10))
    '''
    p, v, a = particle
    nv = v + a
    np = nv + p
    return V(np, nv, a)

def anihilate_particles(particles):
    '''
    >>> anihilate_particles([
    ...     V(V(0,0,0),V(1,2,3),V(0,0,3)),
    ...     V(V(0,1,0),V(1,2,3),V(0,2,0)),
    ...     V(V(0,0,0),V(1,4,3),V(1,0,0)),
    ...    ])
    [V(V(0,1,0),V(1,2,3),V(0,2,0))]
    '''
    positions = collections.defaultdict(list)
    for idx, particle in enumerate(particles):
        p, _, _ = particle
        positions[p].append(idx)

    particles_to_remove = set()
    for colliding_particles in positions.values():
        if len(colliding_particles) > 1:
            particles_to_remove.update(colliding_particles)
    
    return [p for idx, p in enumerate(particles) if idx not in particles_to_remove]

def update_all(particles):
    return [update(particle) for particle in particles]

def tick(particles):
    updated_particles = update_all(particles)
    return anihilate_particles(updated_particles)

def expanding(particles):
    for i, p1 in enumerate(particles):
        for p2 in particles[i+1:]:
            diff = p1 - p2
            p, v, a = diff
            for p_j, v_j, a_j in zip(p, v, a): # j = x, y, z
                if p_j * v_j < 0 or v_j * a_j < 0:
                    return False
    return True

def part_2(particles):
    i = 0
    while True:
        particles = tick(particles)
        i += 1
        if i %100 == 0 and expanding(particles):
            return len(particles)

if __name__ == '__main__':
    particles = parse_input(sys.stdin)
    print(part_1(particles))
    print(part_2(particles))