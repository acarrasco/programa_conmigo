from collections import Counter

input = [line.strip() for line in open('input.txt')]


def most_repeated(characters):
    (character, _), = Counter(characters).most_common(1)
    return character

def least_repeated(characters):
    (_, character) = min((n, c) for (c, n) in Counter(characters).items())
    return character


def part_1(input):
    by_columns = zip(*input)
    most_repeated_character = map(most_repeated, by_columns)
    return ''.join(most_repeated_character)

def part_2(input):
    by_columns = zip(*input)
    least_repeated_character = map(least_repeated, by_columns)
    return ''.join(least_repeated_character)

print(part_1(input))
print(part_2(input))