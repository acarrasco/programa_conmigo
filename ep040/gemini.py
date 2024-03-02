def find_farthest_urinal(urinal_state):
  """
  This function finds the farthest urinal from occupied ones with tie-breakers.

  Args:
      urinal_state: A string representing the state of the urinals, where 0 is unoccupied and 1 is occupied.

  Returns:
      The index of the optimal urinal or "N/A" if none are available.
  """
  occupied_indices = [i for i, state in enumerate(urinal_state) if state == "1"]  # Find occupied urinal indices

  if not occupied_indices:  # No occupied urinals, any is good
    return 0

  # Find distances to closest occupied urinal for each index
  distances = [0] * len(urinal_state)  # Initialize distances to 0 for empty urinals
  for occupied in occupied_indices:
    for i in range(len(urinal_state)):
      if urinal_state[i] == "0" and abs(i - occupied) > distances[i]:  # Only update if further
        distances[i] = abs(i - occupied)

  # Find index with farthest distance (considering tie-breakers)
  farthest_index = -1
  farthest_distance = -float("inf")
  for i, distance in enumerate(distances):
    if distance > farthest_distance:
      farthest_index = i
      farthest_distance = distance
    elif distance == farthest_distance:  # Tie case - prefer furthest from left
      farthest_index = max(farthest_index, i)

  return farthest_index if farthest_index != -1 else "N/A"



# Example usage with test cases
test_cases = [
  "10000",
  "101",
  "000100",
  "0000000",
  "1100111",
  "110011",
  "1010001000111",
  "1111"
]

for case in test_cases:
  result = find_farthest_urinal(case)
  print(f"{result}")
