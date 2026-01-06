"""
This file implements the menu system and user interaction layer
of the indoor navigation application.

It handles:
- Displaying menu options
- Validating user input
- Loading the map data
- Creating the university graph
- Visualizing the graph
- Initiating shortest path computations
"""

from aueb_pathfinding.classes import Classroom, University
from aueb_pathfinding.ultils import clean_values, distance

import networkx as nx
import matplotlib.pyplot as plt

# ==============================================================
#                  Init Check Functions
# ==============================================================

"""
Funtions to ensure the smooth user journey, first has to:
load map -> create graph and then:
visualize or find shortest path
"""

def map_init_check(uni_map):
    
    """
    Docstring for map_init_check
    
    :param map: str or None
        Map loaded from the txt file.
    
    :Returns: bool
        True if map is loaded, False otherwise.
    """
    
    if uni_map is None:
        print(
            "\nMap is not loaded yet. Please load a map first.\n"
            "Hint: Go to option 1) Load Map ;)."
        )
        return False
    return True


def uni_init_check(uni):
    
    """
    Docstring for uni_init_check
    
    :param uni: str or None
        uni created from University class.
    
    :Returns: bool
        True if uni is created, False otherwise.
    """
    
    if uni is None:
        print(
            "\nMap is not loaded yet. Please load a map first.\n"
            "Hint: Go to option 2) Create Graph ;)."
        )
        return False
    
    return True



# ==============================================================
#                  User Input Functions
# ==============================================================
def user_choice(input_prompt, check_prompt, error_prompt, lower_limit, upper_limit):
    
    """
    Handle integer input from the user with validation.

    This function ensures that the user input:
    - Is an integer
    - Lies within the specified lower and upper limits

    :param input_prompt: str
        Main message shown to the user.
    :param check_prompt: str
        Message shown when the value is outside the allowed range.
    :param error_prompt: str
        Message shown when the input is not an integer.
    :param lower_limit: int
        Minimum acceptable value.
    :param upper_limit: int
        Maximum acceptable value.

    :Returns: int
        Validated integer input from the user.
    """

    while True:
        try:
            # Attempt to convert user input to integer
            user_input = int(input(input_prompt))

            # Check if value lies outside user-defined limits
            if user_input < lower_limit or user_input > upper_limit:
                print(check_prompt)
                continue

            return user_input

        except ValueError:
            # Triggered when integer conversion fails
            print(error_prompt)


def user_input_float(input_prompt, check_prompt, error_prompt, lower_limit=-float('inf'), upper_limit=float('inf')):
    
    """
    Handle floating-point input from the user with validation.

    This function ensures that the user input:
    - Is a valid floating-point number
    - Lies within the specified bounds

    :param input_prompt: str
        Main message shown to the user.
    :param check_prompt: str
        Message shown when the value is outside the allowed range.
    :param error_prompt: str
        Message shown when the input is not a valid float.
    :param lower_limit: float
        Minimum acceptable value.
    :param upper_limit: float
        Maximum acceptable value.

    :Returns: float
        Validated floating-point input from the user.
    """
    
    while True:
        try:
            # Attempt to convert user input to float
            user_input = float(input(input_prompt))

            # Range check
            if user_input < lower_limit or user_input > upper_limit:
                print(check_prompt)
                continue

            return user_input

        except ValueError:
            # Triggered when float conversion fails
            print(error_prompt)


def get_user_node(uni, type_node):

    """
    Allow the user to select a classroom from the university graph.

    This function is used to select either the starting or target
    classroom for the shortest path computation.

    :param uni: University
        University graph containing classroom nodes.
    :param type_node: str
        Description of the node type ("starting" or "target").

    :Returns: Classroom or None
        Selected classroom, or None if the user chooses to exit.
    """

    if uni is None:
        print("No University has been created yet! Load one first.")
        return None

    list_len = len(uni.nodes)

    while True:

        print("\n-----------------------------")
        print("       Classrooms List       ")
        print("-----------------------------\n")

        # Display available classrooms
        for idx, node in enumerate(uni.nodes, start=1):
            print(f"{idx}. {node.name}")
        print(f"{list_len + 1}. Exit\n")

        # User selects classroom
        user_input = user_choice(
            input_prompt=(
                f"Please enter the number (from 1 to {list_len}) of the "
                f"{type_node} node (or {list_len + 1} to exit): "
            ),
            check_prompt=f"Please choose an integer from 1 to {list_len + 1}.",
            error_prompt=f"Wrong input. Please choose an integer from 1 to {list_len + 1}.",
            lower_limit=1,
            upper_limit=list_len + 1
        )

        # Handle exit option
        if user_input == list_len + 1:
            print("\nReturning to main menu.")
            return None

        # Convert to Python list index and return selected node
        return uni.nodes[user_input - 1]


# ==============================================================
#                     MENU layout
# ==============================================================

def menu():

    """
    Display the main menu and return the user's selection.
    Valid options: 1–5
    """
    
    print("""
    =========================
            MENU
    =========================
    1) Load Map
    2) Create Graph
    3) Find the shortest path between two classrooms
    4) Visualize Map
    5) Exit
    """)
    
    user_input = user_choice(
                input_prompt="Please choose an option (1–5): ",
                check_prompt="Choice out of range. Please choose a number between 1 and 5.",
                error_prompt="Invalid input. Please enter a number between 1 and 5.",
                lower_limit=1, upper_limit=5    
            )
    
    return user_input
    


# ==============================================================
#                     LOAD Map
# ==============================================================

def load_map(txt_file="aueb_map.txt"):

    """
    Load classroom data from a text file.

    The file is expected to contain one classroom per line,
    with values separated by semicolons in the following order:
    classroom_name; x; y; floor

    :param txt_file: str
        Path to the map text file.

    :Returns: dict
        Dictionary containing classroom names, coordinates,
        and floor levels.
    """

    # Initialize storage for classroom information
    uni_map = {"classroom": [], "x": [], "y": [], "floor": []}

    # Open and read the text file
    with open(txt_file, "r") as file:
        for row in file:
            # Separate values by ';' and clean each entry
            parts = [clean_values(v) for v in row.strip().split(";")]

            # Assign values to the corresponding categories
            uni_map["classroom"].append(parts[0])
            uni_map["x"].append(parts[1])
            uni_map["y"].append(parts[2])
            uni_map["floor"].append(parts[3])

    return uni_map



# ==============================================================
#                     CREATE Graph
# ==============================================================

def create_graph(uni_map = None):

    """
    Create the university graph from the loaded map.

    This function:
    - Prompts the user for graph parameters
    - Creates a University object
    - Adds classroom nodes and weighted edges

    :param uni_map: dict or None
        Dictionary containing classroom data loaded from the map file.

    :Returns: University or None
        Constructed university graph, or None if the map is not loaded.
    """

    if uni_map is None:
        print("Map is not yet loaded, please load map first.\n")
        return
    
    print("\n--- Creating Graph ---\n")
    
    # Maximum Distance input
    user_input_max_distance = user_input_float(
            input_prompt=f"Please Enter Graph's maximum distance: ",
            check_prompt="Maximum distance must greater than 10!",
            error_prompt="Invalid input. Please enter a real number greater than 10.",
            lower_limit=10
        )
    
    # Floor Weight input
    user_input_floor_weight = user_input_float(
            input_prompt=f"Please Enter Graph's floor weight: ",
            check_prompt="Floor Weight must be at least 1!",
            error_prompt="Invalid input. Please enter a real number greater or equal to 1.",
            lower_limit=1
        )

    # Create ecosystem instance
    uni = University(max_distance=user_input_max_distance, floor_weight=user_input_floor_weight)

    # Add nodes and edges to the graph (University Object)
    for name, x, y, floor in zip(
        uni_map["classroom"],uni_map["x"],uni_map["y"],uni_map["floor"]
    ):
        uni.add_node(Classroom(name=name, x=x, y=y, floor=floor))

    for i in range(len(uni.nodes)):
        for j in range(i + 1, len(uni.nodes)):
            uni.add_edge(uni.nodes[i], uni.nodes[j])

    print("\n      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("               University Graph          ")
    print("        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"\nUniversity Graph with maximum distance {uni.max_distance} and floor weight equal to {uni.floor_weight} created!\n")
    return uni 



# ==============================================================
#                     Vizualize Graph
# ==============================================================

def visualize_graph(classrooms, max_distance=21.0, floor_weight=1.0):

    """
    Visualize the university graph using NetworkX and Matplotlib.

    This function creates a graphical representation of the classrooms
    and their connections based on the given distance constraints.

    :param classrooms: list[Classroom]
        List of classroom nodes to be visualized.
    :param max_distance: float
        Maximum allowed distance between two classrooms to draw an edge.
    :param floor_weight: float
        Weight applied to floor differences when computing distances.

    :Returns: matplotlib.figure.Figure
        Figure object containing the rendered graph.
    """

    # Initialise nx object
    uniGraph = nx.Graph()

    # Add each node
    for node in classrooms:
        uniGraph.add_node(node.name, pos=(node.x, node.y))

    # Add the edges without duplicates 
    for i in range(len(classrooms)):
        for j in range(i + 1, len(classrooms)):

            u, v = classrooms[i], classrooms[j]
            dist = distance(u, v, floor_weight)
            if dist <= max_distance:
                uniGraph.add_edge(u.name, v.name, weight=round(dist))

    pos = nx.get_node_attributes(uniGraph, 'pos')

    # Find the min and max x and y values to set the axis limits
    x_vals = [coord[0] for coord in pos.values()]
    y_vals = [coord[1] for coord in pos.values()]

    # Set the axis limits based on the min and max values of the coordinates
    x_min, x_max = min(x_vals) - 10, max(x_vals) + 10  # Add some padding
    y_min, y_max = min(y_vals) - 10, max(y_vals) + 10  # Add some padding

    # Create a plot to visualize the graph
    fig = plt.figure(figsize=(10, 10))

    # Draw the graph with the adjusted position layout
    nx.draw(uniGraph, pos, with_labels=True, node_size=1500, node_color='lightblue', font_size=12, font_weight='bold', edge_color='gray')

    # Optionally, display edge weights (Euclidean distances) on the graph
    edge_labels = nx.get_edge_attributes(uniGraph, 'weight')
    nx.draw_networkx_edge_labels(uniGraph, pos=pos, edge_labels=edge_labels)

    # Adjust the axis to fit the nodes nicely
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    # Add title and show the plot
    plt.title("Aueb Classrooms Graph")

    return fig



# ==============================================================
#                     Shortest Path
# ==============================================================

def print_shortest_path(shortest_path, distance):

    """
    Format the shortest path result as a readable string.

    :param shortest_path: list[Classroom]
        List of classrooms representing the shortest path.
    :param distance: float
        Total cost of the shortest path.

    :Returns: str
        Formatted string describing the path and its total cost.
    """

    path = " -> ".join(str(node) for node in shortest_path)

    return f"Shortest Path: {path} with overall cost {distance}"
