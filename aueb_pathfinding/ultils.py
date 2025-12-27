import re
special_symbols = r"[@#!$\*]"

def clean_values(value, special_symbols = r"[@#!$\*]"):
    
    clean_value = re.sub(special_symbols, "", value)

    try:
        return int(clean_value)
    except ValueError:
        return clean_value

txt_file = "aueb_map.txt"
def load_map(txt_file = "aueb_map.txt"):

    aueb_map = []

    with open(txt_file, "r") as file:
        for row in file:
            parts = row.strip().split(";")
            clean_row = [clean_values(value) for value in parts]
            aueb_map.append(clean_row)

    return aueb_map

