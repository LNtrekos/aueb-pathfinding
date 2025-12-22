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
        
    def __str__(self):
        return (
            f"{self.name} is located on floor {self.floor}, "
            f"with coordinates [x: {self.x}, y: {self.y}]"
        )
    

A21 = Classroom(name="A21", x=0, y=0, floor=2)
print(A21)


class University: 

    # node list 
    # edge dict
    # int/float number max_distances 
    def __init__(self, ):
        return
    
    def __str__(self):
        pass

    def add_node(self, node):
        pass

    def add_edge(self, node1, node2):
        pass

    def get_neighbors(self, node):
        pass

    



