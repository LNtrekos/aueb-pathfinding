"""
Helper functions for the indoor navigation system.
"""

import re
import math


def clean_values(value, special_symbols=r"[@#!$\*]"):
    # Remove special symbols and try to convert to int
    clean_value = re.sub(special_symbols, "", value)

    try:
        return int(clean_value)
    # if that fails it has to be integer (Classroom Name) given the columns we currently have
    except ValueError:
        return clean_value


def distance(node1, node2, floor_weight=1.5):
    
    # Euclidean distance 
    dx = node2.x - node1.x
    dy = node2.y - node1.y

    # Used the math method to calculate the distance
    euclidean_distance = math.hypot(dx, dy)
    # Initial floor penalty
    floor_penalty = 0.0

    # Apply penalty if floors differ
    if node1.floor != node2.floor:
        # Same to the logic of MSE, the greatest the difference the greatest the penalty
        floor_diff = (node1.floor - node2.floor) ** 2
        # with some floor weight for adjusting
        floor_penalty = floor_weight * floor_diff
    
    return euclidean_distance + floor_penalty


def dijkstra(graph, start, target):
    
    dist = dict(); previous = dict() ; visited = dict()
    
    # Initialization
    for node in graph.nodes:
        dist[node] = math.inf
        previous[node] = None
        visited[node] = False

    dist[start] = 0

    # Main loop
    while not all(visited.values()):
        
        # u ← unvisited vertex with minimum distance
        u = min(
            (node for node in graph.nodes if not visited[node]),
            key=lambda node: dist[node],
            default=None
        )

        if u is None:
            break

        if dist[u] == math.inf:
            break

        if u == target:
            break
        
        visited[u] = True


        for v in graph.get_neighbors(u):
            if not visited[v]:
                alt = dist[u] + graph.edges[u][v]
                if alt < dist[v]:
                    dist[v] = alt
                    previous[v] = u

    # Path reconstruction
    path = []
    current = target
    while current is not None:
        path.insert(0, current)
        current = previous[current]
    
    return path, dist[target]


    





