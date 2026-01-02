"""
Helper functions for the indoor navigation system.
"""

import re
import math
import networkx as nx

def clean_values(value, special_symbols=r"[@#!$\*]"):
    # Remove special symbols and try to convert to int
    clean_value = re.sub(special_symbols, "", value)

    try:
        return int(clean_value)
    except ValueError:
        return clean_value


def load_map(txt_file="aueb_map.txt"):
    # Load classroom coordinates and floor info from text file
    aueb_map = {"classroom": [], "x": [], "y": [], "floor": []}

    with open(txt_file, "r") as file:
        for row in file:
            parts = [clean_values(v) for v in row.strip().split(";")]

            aueb_map["classroom"].append(parts[0])
            aueb_map["x"].append(parts[1])
            aueb_map["y"].append(parts[2])
            aueb_map["floor"].append(parts[3])

    return aueb_map


def distance(node1, node2, floor_weight=1.0):
    # Euclidean distance + symmetric floor-change penalty (undirected)
    dx = node2.x - node1.x
    dy = node2.y - node1.y

    euclidean_distance = math.hypot(dx, dy)
    floor_penalty = 0.0

    if node1.floor != node2.floor:
        floor_diff = (node1.floor - node2.floor) ** 2
        floor_penalty = floor_weight * floor_diff

    return euclidean_distance + floor_penalty


def create_Graph_instance():
    return nx.Graph()


def add_nx_nodes(uni, uni_nx):
    
    for node in uni.nodes:
        uni_nx.add_node(node.name, pos = [node.x, node.y])

def visualize_graph(classrooms, max_distance = 21.0):

    uniGraph = nx.Graph()

    for node in classrooms:
        uniGraph.add_node(node.name, pos = [node.x, node.y])

    for i in range(len(classrooms)):
        for j in range(i + 1, len(classrooms)):

            u, v = classrooms[i], classrooms[j]
            dist = distance(u, v)
            if dist <= max_distance:
                uniGraph.add_edge(u.name, v.name, weight=dist)

    
    return uniGraph




