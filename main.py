"""
Main execution file for the indoor navigation system.

This file controls the overall program flow by:
- Displaying the main menu
- Managing user choices
- Coordinating map loading, graph creation, visualization
- Executing shortest path computations
"""

from aueb_pathfinding.menu import (
    menu, load_map, create_graph, visualize_graph,
    print_shortest_path, get_user_node,
    map_init_check, uni_init_check
)
from aueb_pathfinding.ultils import dijkstra


# ==============================================================
#                  Program Initialization
# ==============================================================

# Initial state: no map and no graph loaded
uni_map = None
uni = None

print(
    "\nRecommendation:\n"
    "- Maximum Distance: 21\n"
    "- Floor Weight: 1\n"
    "These values are suggested when selecting option 2) Create Graph\n"
)


# ==============================================================
#                  Main Program Loop
# ==============================================================
1

while True:

    # Display menu and get user choice
    choice = menu()

    # ----------------------------------------------------------
    # Option 1: Load Map
    # ----------------------------------------------------------
    if choice == 1:

        uni_map = load_map()

        if uni_map is None:
            print("Failed to load map.")
            continue

        if not uni_map:
            print("Map data provided are empty.")
            continue

        print("\nPrinting map data:")
        print(f"\n{uni_map}")
        print("\nUniversity map loaded successfully.")
        print("\nReturning to main menu:")

    # ----------------------------------------------------------
    # Option 2: Create Graph
    # ----------------------------------------------------------
    elif choice == 2:

        # Ensure map is loaded before creating graph
        if not map_init_check(uni_map):
            continue

        uni = create_graph(uni_map)

        # Display graph information if creation succeeded
        if uni is not None:
            print(uni)

        print("\nReturning to main menu:")

    # ----------------------------------------------------------
    # Option 3: Find Shortest Path
    # ----------------------------------------------------------
    elif choice == 3:

        # Ensure map and graph are initialized
        if not map_init_check(uni_map):
            continue

        if not uni_init_check(uni):
            continue

        # Allow multiple shortest path queries
        while True:

            # Select starting node
            snode = get_user_node(uni, "starting")
            if snode is None:
                break
            print(f"\nStarting classroom: {snode}\n")

            # Select target node
            tnode = get_user_node(uni, "target")
            if tnode is None:
                break
            print(f"\nTarget classroom: {tnode}\n")

            # Compute shortest path using Dijkstra's algorithm
            shortest_path, distance = dijkstra(uni, snode, tnode)

            if not shortest_path:
                # No path found (already handled inside dijkstra)
                pass
            else:
                result_str = print_shortest_path(shortest_path, distance)
                print(result_str)

    # ----------------------------------------------------------
    # Option 4: Visualize Graph
    # ----------------------------------------------------------
    elif choice == 4:

        # Ensure map and graph are initialized
        if not map_init_check(uni_map):
            continue

        if not uni_init_check(uni):
            continue

        # Generate and display visualization
        graph_fig = visualize_graph(
            uni.nodes, uni.max_distance, uni.floor_weight
        )
        graph_fig.show()

        print("\nReturning to main menu:")

    # ----------------------------------------------------------
    # Option 5: Exit Program
    # ----------------------------------------------------------
    elif choice == 5:
        print("Exiting program...")
        break
