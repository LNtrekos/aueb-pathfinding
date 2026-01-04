from aueb_pathfinding.menu import menu, load_map, create_graph
from aueb_pathfinding.ultils import dijkstra, visualize_graph

aueb_map = None
while True:
    choice = menu()

    if choice == 1:
        aueb_map = load_map()
        print("\nAUEB map loaded succesfully,\nreturning to main menu: ")
    
    elif choice == 2:
        uni = create_graph(aueb_map)
        if uni is not None:
            print(uni)
        print("\nReturning to main menu:")

    elif choice == 3:
        #shortest_path, distance = dijkstra()
        print("Find shortest path")
    
    elif choice == 4:
        #fig = visualize_graph(uni.nodes, max_distance=uni.max_distance)
        #print(fig)
        print("VIz")
            
    elif choice == 5:
        print("Exiting...")
        break

