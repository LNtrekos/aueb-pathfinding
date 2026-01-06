"""
Helper functions for the indoor navigation system.

This file contains utility functions used across the project,
including data cleaning, distance calculation, and shortest
path computation.
"""

import re
import math


# ==============================================================
#                   Data Cleaning Functions
# ==============================================================

def clean_values(value, special_symbols=r"[@#!$\*]"):
    """
    Clean input values by removing special symbols.

    This function attempts to convert the cleaned value to an integer.
    If conversion fails, the value is returned as a string (e.g. classroom name).

    :param value: str
        Raw value read from the input file.
    :param special_symbols: str
        Regular expression of symbols to be removed.

    :Returns: int or str
        Cleaned integer value or original string.
    """

    # Remove special symbols
    clean_value = re.sub(special_symbols, "", value)

    try:
        return int(clean_value)
    # If conversion fails, return the cleaned string
    except ValueError:
        return clean_value


# ==============================================================
#                   Distance Calculation
# ==============================================================

def distance(node1, node2, floor_weight=1.5):
    """
    Compute the weighted distance between two classrooms.

    The distance consists of:
    - Euclidean distance on the same floor
    - A penalty term when classrooms are on different floors

    :param node1: Classroom
        Starting classroom.
    :param node2: Classroom
        Target classroom.
    :param floor_weight: float
        Weight factor applied to floor differences.

    :Returns: float
        Weighted distance between the two classrooms.
    """

    # Euclidean distance components
    dx = node2.x - node1.x
    dy = node2.y - node1.y

    # Calculate Euclidean distance
    euclidean_distance = math.hypot(dx, dy)

    # Initialize floor penalty
    floor_penalty = 0.0

    # Apply penalty if floors differ
    if node1.floor != node2.floor:
        # Similar to MSE logic: larger floor difference -> larger penalty
        floor_diff = (node1.floor - node2.floor) ** 2
        floor_penalty = floor_weight * floor_diff

    return euclidean_distance + floor_penalty


# ==============================================================
#                   Shortest Path Algorithm
# ==============================================================

def dijkstra(graph, start, target):
    """
    Compute the shortest path between two classrooms using
    Dijkstra's algorithm.

    :param graph: University
        University graph containing nodes and weighted edges.
    :param start: Classroom
        Starting classroom.
    :param target: Classroom
        Target classroom.

    :Returns: tuple
        - path: list[Classroom]
            Shortest path from start to target.
        - distance: float
            Total cost of the path.
    """

    # Initialization of helper dictionaries
    dist = {}
    previous = {}
    visited = {}

    for node in graph.nodes:
        dist[node] = math.inf
        previous[node] = None
        visited[node] = False

    dist[start] = 0

    # Main Dijkstra loop
    while True:

        # Select unvisited node with minimum distance
        u = min(
            (node for node in graph.nodes if not visited[node]),
            key=lambda node: dist[node],
            default=None
        )

        # Stop if no reachable node remains
        if u is None or dist[u] == math.inf:
            break

        # Stop if target is reached
        if u == target:
            break

        visited[u] = True

        # Update shortest path
        for v in graph.get_neighbors(u):
            if not visited[v]:
                alt = dist[u] + graph.edges[u][v]
                if alt < dist[v]:
                    dist[v] = alt
                    previous[v] = u

    # Path reconstruction
    if dist[target] == math.inf:
        print(f"{target.name} is unreachable from {start.name} !")
        return [], math.inf

    path = []
    current = target
    while current is not None:
        path.insert(0, current)
        current = previous[current]

    return path, dist[target]
