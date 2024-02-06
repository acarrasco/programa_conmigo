import heapq

current_elf_calories = 0
elves_total_calories = []
for line in open("input.txt"):
    if line.strip() == "":
        elves_total_calories.append(current_elf_calories)
        current_elf_calories = 0
    else:
        current_elf_calories += int(line.strip())
elves_total_calories.append(current_elf_calories)

# part 1
print(max(elves_total_calories))

# part 2
top_three = heapq.nlargest(3, elves_total_calories)
print(sum(top_three))