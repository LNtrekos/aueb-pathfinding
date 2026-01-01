"""
This file contains the classes we used: 
Classroom, University
"""

from aueb_pathfinding.ultils import distance, clean_values # inside distance 


class Classroom:

    def __init__(self, name, x, y, floor):

        # Basic validation
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Classroom name must be a non-empty string.")
        
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Coordinates must be integers.")
        
        if not isinstance(floor, int):
            raise ValueError("Floor must be an integer.")

        # Assign attributes
        self.name = name
        self.x = x
        self.y = y
        self.floor = floor

    def __eq__(self, other):
        """ eq and hash a bit extra for this project
        But It was something disccussed in class and 
        thought of incorporating """

        if not isinstance(other, Classroom):
            print("Argument is not a Classroom object")
        return (
            self.name == other.name
            and self.floor == other.floor
        )

    def __hash__(self):
        return hash((self.name, self.floor))
        
    def __str__(self):
        return self.name


class University: 

    def __init__(self, nodes=None, edges=None, max_distance=21.0):

        if nodes is None:
            nodes = []
        if edges is None:
            edges = {}

        if not isinstance(nodes, list):
            raise TypeError("nodes must be a list.")

        if not isinstance(edges, dict):
            raise TypeError("edges must be a dict.")
        
        if not isinstance(max_distance, (int, float)):
            raise TypeError("max_distance must be a number")

        for n in nodes:
            if not isinstance(n, Classroom):
                raise TypeError("All nodes must be Classroom objects")

        self.nodes = list(nodes)
        self.edges = dict(edges)
        self.max_distance = float(max_distance)
        
    def __str__(self):
        # Classrooms
        classrooms = ", ".join(node.name for node in self.nodes)

        # Links / roads
        links = []
        for src, targets in self.edges.items():
            for dst, dist in targets.items():
                links.append(f"{src} -> {dst} (dist={dist})")

        links_str = "\n".join(links) if links else "No links available"

        return (
            "\nAUEB Classrooms:\n"
            f"{classrooms}\n\n"
            "Available links:\n"
            f"{links_str}"
        )

        
    def add_node(self, node):

        if isinstance(node, Classroom):
            self.nodes.append(node)
        else:
            print("Invalid classroom. Please provide a Classroom object.")

    def add_edge(self, node1, node2):

        if node1 == node2:
            print("Node 1 and Node 2 are the same")
            return

        dist = distance(node1, node2)

        if dist > self.max_distance:
            print(f"{node1.name} is too far from {node2.name}")
            return

        if node1.name not in self.edges:
            self.edges[node1.name] = {}

        self.edges[node1.name][node2.name] = round(dist, 2)


    def get_neighbors(self, node):
        
        neighbors = []
        for node_name in self.edges[node.name]:
            neighbors.append(node_name)

        return neighbors


