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

    def clean_values(value, special_symbols = r"[@#!$\*]"):
    
        clean_value = re.sub(special_symbols, "", value)

        try:
            return int(clean_value)
        except ValueError:
            return clean_value

    aueb_map = {
        "classroom": [], "x": [], "y": [], "floor": []
    }

    with open(txt_file, "r") as file:
        for row in file:
            parts = [clean_values(v) for v in row.strip().split(";")]

            aueb_map["classroom"].append(parts[0])
            aueb_map["x"].append(parts[1])
            aueb_map["y"].append(parts[2])
            aueb_map["floor"].append(parts[3])
    
    return aueb_map

def distance(node1, node2, floor_weight=1.0):

    dx = node2.x - node1.x
    dy = node2.y - node1.y

    euclidean_distance = math.hypot(dx, dy)
    floor_penalty = 0.0

    if node1.floor != node2.floor:
        angle = math.atan2(dy, dx)    # tilt
        floor_penalty = floor_weight  * angle

        if node2.floor > node1.floor: # Going Up
            print("Going Up")
        else:                         # Going Down
            print("Going Down")
    else:
        print("Same floor")           # Same Floor   

    return euclidean_distance + floor_penalty


