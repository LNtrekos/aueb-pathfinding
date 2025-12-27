


def clean_values():
    return


def load_map():
    return



import re

special_symbols = r"[@#!$\*]"


with open("aueb_map.txt", "r") as file:
    for row in file:
        found = re.findall(special_symbols, row)
        if found:
            print(row, "->", found)


with open("aueb_map.txt", "r") as file:
    aueb_map = file.read()

print(aueb_map)
grid = aueb_map.splitlines()



# I have to search what kind of object is the aueb_map 
# and explore the re library
