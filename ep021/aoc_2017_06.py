banks = list(map(int, open('input.txt').readline().split()))

def find_max_bank_index(banks):
    current_max_index = 0
    for index, value in enumerate(banks):
        if value > banks[current_max_index]:
            current_max_index = index
    return current_max_index

def rebalance(banks):
    bank_index = find_max_bank_index(banks)
    banks = list(banks)
    amount_to_redistribute = banks[bank_index]
    banks[bank_index] = 0
    while amount_to_redistribute > 0:
        bank_index += 1
        banks[bank_index % len(banks)] += 1
        amount_to_redistribute -= 1
    return tuple(banks)

def part_1_and_2(banks):
    seen_configurations = {}
    banks = tuple(banks)
    iteration = 0
    while banks not in seen_configurations:
        seen_configurations[banks] = iteration
        iteration += 1
        banks = rebalance(banks)
    return len(seen_configurations), iteration - seen_configurations[banks]

print(part_1_and_2(banks))