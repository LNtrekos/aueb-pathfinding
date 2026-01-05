from aueb_pathfinding.menu import (
    menu, load_map, create_graph, visualize_graph, print_shortest_path,
    get_user_node, map_init_check, uni_init_check
)
from aueb_pathfinding.ultils import dijkstra

# Initialation step
uni_map = None; uni = None

print("\nRecommandation:\n- Maximum Distance: 21\n- Floor Weight = 1\nNeeded in option 2) Create Graph")
while True:
    
    choice = menu()

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
        print("\nUniversity Map loaded succesfully")

        print("\nReturning to main menu:")
    
    elif choice == 2:

        if not map_init_check(uni_map):
            continue

        uni = create_graph(uni_map)

        if uni is not None:
            print(uni)

        print("\nReturning to main menu:")

    elif choice == 3:

        if not map_init_check(uni_map):
            continue

        if not uni_init_check(uni):
            continue

        while True:

            snode = get_user_node(uni, "starting")
            if snode is None:
                break
            print(f"\nStarting classroom: {snode}\n")

            tnode = get_user_node(uni, "target")
            if tnode is None:
                break
            print(f"\nTarget classroom: {tnode}\n")
            
            shortest_path, distance = dijkstra(uni, snode, tnode)

            if not shortest_path:
                pass
            else:
                str_shorthest_path = print_shortest_path(shortest_path, distance)
                print(str_shorthest_path)
            
    
    elif choice == 4:

        if not map_init_check(uni_map):
            continue

        if not uni_init_check(uni):
            continue
        
        graph = visualize_graph(uni.nodes, uni.max_distance, uni.floor_weight)
        graph.show()

        print("\nReturning to main menu:")
            
    elif choice == 5:
        print("Exiting...")
        break

