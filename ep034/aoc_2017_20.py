import sys
import math
from functools import reduce
from itertools import batched
from collections import defaultdict

CLEAN_PARTICLE_INPUT_TABLE = {ord(c): None for c in 'pva=<>'}
def parse_particle(line):
    tokens = line.translate(CLEAN_PARTICLE_INPUT_TABLE).split(',')
    return list(batched(map(int, tokens),3))

def absolute_acceleration(index_and_particle):
    _, (_, _, a) = index_and_particle
    return sum(map(abs, a))

def part_1(particles):
    return min(particles, key=absolute_acceleration)[0]

POSITION, VELOCITY, ACCELERATION = range(3)

def tick(particles):
    '''
    >>> tick(tick([((0,0,0), (1, 2, 3), (1, 2, 3))]))
    [((5, 10, 15), (3, 6, 9), (1, 2, 3))]
    '''
    result = []
    for i, ((px, py, pz), (vx, vy, vz), (ax, ay, az)) in particles:
        vx += ax
        vy += ay
        vz += az
        px += vx
        py += vy
        pz += vz
        updated_particle = i, ((px, py, pz), (vx, vy, vz), (ax, ay, az))
        result.append(updated_particle)
    return result

def calculate_distances(particles):
    distances = [
        abs(x) + abs(y) + abs(z) for _,((x,y,z),_,_) in particles
    ]
    return distances

def velocity_towards_acceleration(particle):
    _, (_, (vx, vy, vz), (ax, ay, az)) = particle
    return vx * ax >= 0 and vy * ay >= 0 and vz * az >= 0

def expanding(particles, distances_0, distances_1):
    velocities_towards_accelerations = map(velocity_towards_acceleration, particles)
    increasing_distances = (d0 < d1 for d0, d1 in zip(distances_0, distances_1))
    return all(velocities_towards_accelerations) and all(increasing_distances)

def anhiliate(particles):
    particles_by_position = defaultdict(list)
    for i, (position, _, _) in particles:
        particles_by_position[position].append(i)

    particles_to_remove = set(pi for v in particles_by_position.values()
                                 for pi in v  
                                 if len(v) > 1)
    if not particles_to_remove:
        return particles
    # print('anhiliating', [v for v in particles_by_position.values() if len(v) > 1])
    return [(i, p) for (i, p) in particles if i not in particles_to_remove]

def part_2_brute_force(particles):
    distances = calculate_distances(particles)
    # pprint.pprint(particles)
    while True:
        particles = tick(particles)
        #pprint.pprint(particles)
        new_distances = calculate_distances(particles)
        particles = anhiliate(particles)
        if expanding(particles, distances, new_distances):
            return len(particles)
        distances = new_distances


def position_at_t(particle, t):
    '''
    >>> position_at_t(((0,0,0), (1, 2, 3), (0, 0, 0)), 0)
    (0, 0, 0)
    >>> position_at_t(((0,0,0), (1, 2, 3), (0, 0, 0)), 1)
    (1, 2, 3)
    >>> position_at_t(((0,0,0), (1, 2, 3), (0, 0, 0)), 2)
    (2, 4, 6)
    >>> position_at_t(((1,1,1), (1, 2, 3), (0, 0, 0)), 2)
    (3, 5, 7)
    >>> position_at_t(((0,0,0), (1, 2, 3), (1, 2, 3)), 1)
    (2, 4, 6)
    >>> position_at_t(((0,0,0), (1, 2, 3), (1, 2, 3)), 2)
    (5, 10, 15)
    '''
    return tuple(
        d + v * t + a * t * (t + 1) // 2 for d, v, a in zip(*particle)
    )

def solve_equation(a, b, c):
    if a == 0 and b == 0 and c == 0:
        return (math.nan,)
    if a == 0 and b == 0:
        return ()
    if a == 0:
        return (-c / b,)
    return ((-b + (b*b - 4*a*c)**0.5) / (2*a),
            (-b - (b*b - 4*a*c)**0.5) / (2*a))

def time_at_origin(d, v, a):
    return solve_equation(a / 2, v + a / 2, d)

def is_real(x):
    return x.imag == 0

def round(x):
    if abs(x - int(x+0.5)) < 1E-3:
        return int(x+0.5)
    return x

def common_times(times):
    valid_times = (set(map(round, filter(is_real, tg))) for tg in times if tg != (math.nan,))
    return reduce(set.intersection, valid_times)

def collision_time(particle_i, particle_j):
    i, (pi, vi, ai) = particle_i
    j, (pj, vj, aj) = particle_j
    
    # collision time for each dimension indendently
    # d = d0 + v * t + a * t * (t + 1) = a * t**2 + (v + a) * t + d0
    times = [time_at_origin(pi[i]-pj[i], vi[i]-vj[i], ai[i]-aj[i])
             for i in range(3) # for each dimension x=0, y=1, z=2
             ]
    common = common_times(times)
    # print(i, j, times, common)
    return min(common, default=False)

def part_2_analytical(particles):
    particles = list(map(tuple, particles))
    collision_times = defaultdict(list)
    for i in range(len(particles)):
        pi = particles[i]
        for j in range(i+1, len(particles)):
            pj = particles[j]
            t = collision_time(pi, pj)
            if t:
                collision_times[int(t)].append(i)
                collision_times[int(t)].append(j)
    anihilated = set()
    for _, colliding_particles in sorted(collision_times.items()):
        remaining_colliding_particles = set(colliding_particles) - anihilated
        if len(remaining_colliding_particles) >= 2:
            anihilated.update(remaining_colliding_particles)
    # print(anihilated)
    return len(particles) - len(anihilated)

if __name__ == '__main__':
    input = open(sys.argv[1])
    particles = list(enumerate(map(parse_particle, input)))
    print(part_1(particles))
    print(part_2_brute_force(particles))
    # print(part_2_analytical(particles))