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


i = 0
name = aueb_map["classroom"][i]; x = aueb_map["x"][i]; y = aueb_map["y"][i]; floor = aueb_map["floor"][i]
node1 = Classroom(name=name, x=x, y=y, floor=floor)
print(node1)

i = 5
name = aueb_map["classroom"][i]; x = aueb_map["x"][i]; y = aueb_map["y"][i]; floor = aueb_map["floor"][i]
node2 = Classroom(name=name, x=x, y=y, floor=floor)
print(node2)

distance(node1=node1, node2=node2)

Aueb.add_edge(node1, node2)

print(Aueb)

