def find_optimal_urinal(scenario):
    urinals = [int(char) for char in scenario.strip()]

    if sum(urinals) == 0:
        # All urinals are unoccupied
        return "N/A"

    if sum(urinals) == len(urinals):
        # All urinals are occupied, no empty urinal
        return "N/A"

    max_distance = 0
    optimal_urinal = 0
    current_distance = 0

    for i in range(len(urinals)):
        if urinals[i] == 0:
            # Calculate distance to the closest occupied urinal
            current_distance += 1

            if i == len(urinals) - 1 or urinals[i + 1] == 1:
                # If it's the last urinal or the next one is occupied
                if current_distance > max_distance:
                    # Update optimal urinal index
                    max_distance = current_distance
                    optimal_urinal = i - current_distance // 2
                current_distance = 0

    return str(optimal_urinal)


# Read input scenarios
input_data = """10000
101
000100
0000000
1100111
110011
1010001000111
1111"""

input_scenarios = input_data.split('\n')

# Process each scenario and print the result
for scenario in input_scenarios:
    result = find_optimal_urinal(scenario)
    print(result)
