"""
This file contains the menu part of the navigation system
"""

from aueb_pathfinding.classes import Classroom, University
from aueb_pathfinding.ultils import clean_values


# ==============================================================
#                  User Input Functions
# ==============================================================

def user_choice(input_prompt, check_prompt, error_prompt,
    lower_limit=-float('inf'), upper_limit=float('inf')):
    '''
    Handles integer input from the user with:
    - Type validation
    - Lower/upper bound checks
    - Custom prompts for incorrect entries

    Parameters:
        input_prompt : Main message shown to the user.
        check_prompt : Message shown when the value is outside limits.
        error_prompt : Message shown when the input is not an integer.
        lower_limit  : Minimum acceptable value (default: -inf).
        upper_limit  : Maximum acceptable value (default: +inf).

    Returns:
        Validated integer input from the user.
    '''
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
            # Triggered when int conversion fails
            print(error_prompt)


def user_input_float(input_prompt, check_prompt, error_prompt,
                     lower_limit=-float('inf'), upper_limit=float('inf')):
    '''
    Handles floating-point input with:
    - Type validation
    - Lower/upper bound checks
    - Custom prompts for invalid numerical entries

    Parameters mirror those of user_input_int() but for float inputs.
    '''
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
            # For invalid float entries
            print(error_prompt)


def user_input_character(input_prompt):
    '''
    Handles string input where:
    - Blank inputs are rejected
    - User must confirm the entered value
    - Ensures non-empty, user-approved text input

    Returns:
        A validated, confirmed string.
    '''
    while True:
        # Remove surrounding spaces; ensure non-blank
        user_input = input(input_prompt).strip()

        if user_input == "":
            print("Wrong Input. Blank space is not allowed.")
            continue

        # Confirmation loop
        while True:
            confirm = input(f"You entered '{user_input}'. Proceed? [Y]/n: ").strip().lower()

            # Accept input on Enter or 'y'
            if confirm == "" or confirm == "y":
                print("\n")
                return user_input

            # Restart input if 'n'
            elif confirm == "n":
                print("Okay, let's try again.\n")
                break

            # Handle invalid confirmation inputs
            else:
                print("Invalid choice. Please type 'Y' or 'n'.")

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
    # Load classroom coordinates and floor info from text file
    aueb_map = {"classroom": [], "x": [], "y": [], "floor": []}

    # Open the txt file
    with open(txt_file, "r") as file:
        for row in file:
            # Seprate each value by ; and clean and turn to int/str
            parts = [clean_values(v) for v in row.strip().split(";")]

            # Assign each value to the corresponding category 
            aueb_map["classroom"].append(parts[0])
            aueb_map["x"].append(parts[1])
            aueb_map["y"].append(parts[2])
            aueb_map["floor"].append(parts[3])

    return aueb_map



# ==============================================================
#                     CREATE Graph
# ==============================================================

def create_graph(txt_map = None):
    """
    Prompt the user for max_distance,
    create a suitable graph, and return it.
    """
    if txt_map is None:
        print("Map is not yet loaded, please load map first.\n")
        return
    
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
    for name, x, y, floor in zip(txt_map["classroom"],txt_map["x"],txt_map["y"],txt_map["floor"]):
        uni.add_node(Classroom(name=name, x=x, y=y, floor=floor))

    for i in range(len(uni.nodes)):
        for j in range(i + 1, len(uni.nodes)):
            uni.add_edge(uni.nodes[i], uni.nodes[j])

    print("       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                 AUEB Graph          ")
    print("       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"\nAueb Graph with maximum distance {uni.max_distance} and {uni.floor_weight} floor weight created!\n")
    return uni


