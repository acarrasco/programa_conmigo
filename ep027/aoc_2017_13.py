import sys

def parse_line(line):
    layer_depth, layer_range = map(int, line.split(':'))
    return int(layer_depth), int(layer_range)

def parse_firewall(lines):
    return dict(map(parse_line, lines))

class Scanner:
    def __init__(self, layer_range):
        self.layer_range = layer_range
        self.position = 0
        self.direction = 1
        
    def step(self):
        if not (0 <= self.position + self.direction < self.layer_range):
            self.direction *= -1
        self.position += self.direction

    def is_in_zero_position(self, turn):
        return turn % (2 * (self.layer_range -1)) == 0

def part_1(firewall_configuration):
    scanners = {d: Scanner(r) for d, r in firewall_configuration.items()}
    severity = 0

    max_depth = max(firewall_configuration)
    for depth in range(max_depth + 1):        
        scanner = scanners.get(depth)
        if scanner and scanner.position == 0:
            severity += depth * scanner.layer_range

        for scanner in scanners.values():
            scanner.step()
    return severity

def is_caught(scanners, delay):
    return any(scanner.is_in_zero_position(delay + depth)
                for depth, scanner in scanners.items())

def part_2(firewall_configuration):
    delay = 0
    scanners = {d: Scanner(r) for d, r in firewall_configuration.items()}
    while is_caught(scanners, delay):
        delay += 1
    return delay

if __name__ == '__main__':
    input = open(sys.argv[1]).readlines()
    firewall_configuration = parse_firewall(input)
    print(part_1(firewall_configuration))
    print(part_2(firewall_configuration))
