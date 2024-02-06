import sys

numbers = [int(c) for c in sys.stdin.readline().strip()]

# part 1
result = 0
for i in range(len(numbers)):
    if numbers[i] == numbers[i - 1]:
        result += numbers[i]
print(result)

# part 2
result = 0
for i in range(len(numbers)):
    if numbers[i] == numbers[(i + len(numbers) // 2) % len(numbers)]:
        result += numbers[i]
print(result)