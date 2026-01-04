"""
Helper functions for the indoor navigation system.
"""

import re
import math
import networkx as nx
import matplotlib.pyplot as plt


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


def visualize_graph(classrooms, max_distance = 21.0):

    # Initialise nx object
    uniGraph = nx.Graph()

    # Add each node
    for node in classrooms:
        uniGraph.add_node(node.name, pos=(node.x, node.y))

    # Add the edges without duplicates 
    for i in range(len(classrooms)):
        for j in range(i + 1, len(classrooms)):

            u, v = classrooms[i], classrooms[j]
            dist = distance(u, v)
            if dist <= max_distance:
                uniGraph.add_edge(u.name, v.name, weight=round(dist))

    pos = nx.get_node_attributes(uniGraph, 'pos')

    # Find the min and max x and y values to set the axis limits
    x_vals = [coord[0] for coord in pos.values()]
    y_vals = [coord[1] for coord in pos.values()]

    # Set the axis limits based on the min and max values of the coordinates
    x_min, x_max = min(x_vals) - 10, max(x_vals) + 10  # Add some padding
    y_min, y_max = min(y_vals) - 10, max(y_vals) + 10  # Add some padding

    # Create a plot to visualize the graph
    fig = plt.figure(figsize=(10, 10))

    # Draw the graph with the adjusted position layout
    nx.draw(uniGraph, pos, with_labels=True, node_size=1500, node_color='lightblue', font_size=12, font_weight='bold', edge_color='gray')

    # Optionally, display edge weights (Euclidean distances) on the graph
    edge_labels = nx.get_edge_attributes(uniGraph, 'weight')
    nx.draw_networkx_edge_labels(uniGraph, pos=pos, edge_labels=edge_labels)

    # Adjust the axis to fit the nodes nicely
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    # Add title and show the plot
    plt.title("Aueb Classrooms Graph")

    return fig


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


def print_shortest_path(shortest_path, distance):

    path = " -> ".join(str(node) for node in shortest_path)
    return f"Shortest Path: {path} with overall cost {distance}"
    





