import re
import math 

#special_symbols = r"[@#!$\*]"
def clean_values(value, special_symbols = r"[@#!$\*]"):
    
    clean_value = re.sub(special_symbols, "", value)

    # Try converting to integer
    try:
        return int(clean_value)
    # if fails means the column is Classroom Name:
    except ValueError:
        # so it is character
        return clean_value

#txt_file = "aueb_map.txt"
def load_map(txt_file = "aueb_map.txt"):

    aueb_map = {
        "classroom": [], "x": [], "y": [], "floor": []
    }

    with open(txt_file, "r") as file:
        for row in file:
            parts = [clean_values(value) for value in row.strip().split(";")]

            aueb_map["classroom"].append(parts[0]) # Classroom Name
            aueb_map["x"].append(parts[1])         # X
            aueb_map["y"].append(parts[2])         # Y 
            aueb_map["floor"].append(parts[3])     # Floor
    
    return aueb_map

def distance(node1, node2, floor_weight=1.0):

    dx = node2.x - node1.x
    dy = node2.y - node1.y

    euclidean_distance = math.hypot(dx, dy)
    floor_penalty = 0.0

    if node1.floor != node2.floor:

        floor_diff = (node1.floor - node2.floor)**2
        floor_penalty = floor_weight  * floor_diff

        if node2.floor > node1.floor: # Going Up
            print(f"Going Up ({node1.name} -> {node2.name})")
        else:                         # Going Down
            print(f"Going Down ({node1.name} -> {node2.name})")
    else:
        print(f"Same floor ({node1.name} -> {node2.name})")   # Same Floor   

    return euclidean_distance + floor_penalty


