import re
import math 

#special_symbols = r"[@#!$\*]"
def clean_values(value, special_symbols = r"[@#!$\*]"):
    
    clean_value = re.sub(special_symbols, "", value)

    try:
        return int(clean_value)
    except ValueError:
        return clean_value

#txt_file = "aueb_map.txt"
def load_map(txt_file = "aueb_map.txt"):

    aueb_map = {
        "classroom": [],
        "x": [], "y": [],
        "floor": []
    }

    with open(txt_file, "r") as file:
        for row in file:
            parts = [clean_values(v) for v in row.strip().split(";")]

            aueb_map["classroom"].append(parts[0])
            aueb_map["x"].append(parts[1])
            aueb_map["y"].append(parts[2])
            aueb_map["floor"].append(parts[3])
    

    return aueb_map

aueb_map = load_map()

from aueb_pathfinding.classes import Classroom, University

Aueb = University()

for name, x, y, floor in zip(aueb_map["classroom"],aueb_map["x"],aueb_map["y"],aueb_map["floor"]):
    Aueb.add_node(Classroom(name=name, x=x, y=y, floor=floor))

i = 0
name = aueb_map["classroom"][i]; x = aueb_map["x"][i]; y = aueb_map["y"][i]; floor = aueb_map["floor"][i]
node1 = Classroom(name=name, x=x, y=y, floor=floor)
print(node1)

i = 1
name = aueb_map["classroom"][i]; x = aueb_map["x"][i]; y = aueb_map["y"][i]; floor = aueb_map["floor"][i]
node2 = Classroom(name=name, x=x, y=y, floor=floor)
print(node2)

def distance(node1, node2, floor_weight=2.0):
    
    dx = node2.x - node1.x
    dy = node2.y - node1.y

    euclidean_distance = math.hypot(dx, dy)

    if node1.floor == node2.floor:
        floor_penalty = 0.0
    else:
        angle = abs(math.atan2(dy, dx))   # [0, π]

        # y-axis distance
        floor_penalty = floor_weight * (1 + angle)

    return euclidean_distance + floor_penalty
