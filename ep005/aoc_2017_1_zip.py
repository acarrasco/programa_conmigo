numbers = [int(c) for c in open("input.txt").readline().strip()]

# part 1
repeated_numbers = (a for a, b in zip(numbers, numbers[1:] + [numbers[0]]) if a == b)
result = sum(repeated_numbers)
print(result)

# part 2
l = len(numbers)
result = sum(a for a, b in zip(numbers, numbers[l // 2:] + numbers[:l // 2]) if a == b)

print(result)