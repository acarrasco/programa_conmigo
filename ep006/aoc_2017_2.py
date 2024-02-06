import sys

data = []
for line in sys.stdin:
    line_numbers = [int(n) for n in line.strip().split()]
    data.append(line_numbers)

# part 1
checksum = sum(max(row) - min(row) for row in data)
print(checksum)

# part 2
evenly_divisible_sum = 0
for row in data:
    for i, a in enumerate(row):
        for j, b in enumerate(row):
            if i != j and a % b == 0:
                evenly_divisible_sum += a // b
print(evenly_divisible_sum)
