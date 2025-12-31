from aueb_pathfinding.menu import (
    menu
)
from aueb_pathfinding.classes import Classroom, University

from aueb_pathfinding.ultils import (
    clean_values, # is used inside load_map function
    load_map, distance
)

# Load txt file
aueb_map = load_map()

# Initialize University Class
Aueb = University()

# add classes from txt file (aueb_map) inside the University class
for name, x, y, floor in zip(aueb_map["classroom"],aueb_map["x"],aueb_map["y"],aueb_map["floor"]):
    Aueb.add_node(Classroom(name=name, x=x, y=y, floor=floor))

for src in Aueb.nodes:
    for dest in Aueb.nodes:
        Aueb.add_edge(src, dest)


import networkx as nx
Aueb_Graph = nx.Graph()
for node in Aueb.nodes:
    Aueb_Graph.add_node(node.name, pos = [node.x, node.y])
print(Aueb_Graph)

Aueb.edges["A21"]
Aueb.edges["A22"]