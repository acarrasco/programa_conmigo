import heapq
import math

def dijkstra(start, goal, neighbors):
    distances = {}
    distances[start] = 0
    open_set = [(0, start)]

    while True:
        current_distance, node = heapq.heappop(open_set)
        if node == goal:
            return current_distance
        for cost, neighbor in neighbors(node):
            if distances.get(neighbor, math.inf) > current_distance + cost:
                distances[neighbor] = current_distance + cost
                heapq.heappush(open_set, (current_distance + cost, neighbor))
