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


def load_map(txt_file="aueb_map.txt"):
    # Load classroom coordinates and floor info from text file
    aueb_map = {"classroom": [], "x": [], "y": [], "floor": []}

    # Open the txt file
    with open(txt_file, "r") as file:
        for row in file:
            # Seprate each value by ; and clean and turn to int/str
            parts = [clean_values(v) for v in row.strip().split(";")]

            # Assign each value to the corresponding category 
            aueb_map["classroom"].append(parts[0])
            aueb_map["x"].append(parts[1])
            aueb_map["y"].append(parts[2])
            aueb_map["floor"].append(parts[3])

    return aueb_map


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





