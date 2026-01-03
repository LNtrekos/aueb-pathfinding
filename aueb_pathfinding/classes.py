"""
This file contains the classes we used: 
Classroom, University
"""

from aueb_pathfinding.ultils import distance # inside University (for edges) 

class Classroom:

    # Initialization
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

    # Print method
    def __str__(self):
        return self.name
    
    # Represent method (for developers)
    def __repr__(self):
        return f"Classroom(name={self.name!r}, floor={self.floor})"

    # Equallity 
    def __eq__(self, other):
        """ eq and hash a bit extra for this project
        But It was something disccussed in class and 
        thought of incorporating """

        if not isinstance(other, Classroom):
            return False
        return self.name == other.name

    # Hash items
    def __hash__(self):
        return hash((self.name, self.floor))
        

class University: 

    # Initialization
    def __init__(self, nodes=None, edges=None, max_distance=21.0):

        # Basic validation
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

        # Assign attributes
        self.nodes = list(nodes)
        self.edges = dict(edges)
        self.max_distance = float(max_distance)
        
    # Nodes
    def add_node(self, node):

        # Basic validation
        if isinstance(node, Classroom):
            self.nodes.append(node)
        else:
            print("Invalid classroom. Please provide a Classroom object.")

    # Edges
    def add_edge(self, node1, node2):
        
        # Check if nodes are the same (eq from classroom object)
        if node1 == node2:
            print("Node 1 and Node 2 are the same")
            return

        # calsulate the distance between the nodes 
        dist = distance(node1, node2)

        # Distance has to be valid 
        if dist > self.max_distance:
            print(f"{node1.name} is too far from {node2.name}")
            return

        # Initialise place in dictionary to store each node
        if node1 not in self.edges:
            self.edges[node1] = {}
        
        if node2 not in self.edges:
            self.edges[node2] = {}

        # Add both "directions" (A21 -> A22, A22 -> A21), though the graph is undirected
        self.edges[node1][node2] = round(dist, 2)
        self.edges[node2][node1] = round(dist, 2)

    # Neighbors
    def get_neighbors(self, node):
        
        if node not in self.edges:
            return []
        
        neighbors = list(self.edges[node].keys())
        return neighbors
    
    # String represent
    def __str__(self):
        # Nice way to display Classrooms
        classrooms = ", ".join(node.name for node in self.nodes)

        # Nice way to display all links / roads (both ways)
        links = []
        for src, targets in self.edges.items():
            for dest, dist in targets.items():
                links.append(f"{src} -> {dest} (dist={dist})")

        links_str = "\n".join(links) if links else "No links available"

        return (
            "\nAUEB Classrooms:\n"
            f"{classrooms}\n\n"
            "Available links:\n"
            f"{links_str}"
        )

        


