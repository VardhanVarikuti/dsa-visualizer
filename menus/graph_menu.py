"""
Graph menu for DSA Visualizer
"""
def graph_menu():
    while True:
        print("\n--- Graph Algorithms ---")
        print("[1] Maze/Grid")
        print("[2] N-Queens")
        print("[3] Directed Graph")
        print("[4] Weighted Graph")
        print("[5] Undirected Graph")
        print("[0] Back")
        choice = input("Select an option: ").strip()
        if choice == '1':
            from ui.grid_visualizer import run_grid_visualizer
            run_grid_visualizer()
        elif choice == '2':
            print("Launching Backtracking on N-Queens...")
            from ui.nqueens_visualizer import run_nqueens_visualizer
            run_nqueens_visualizer()
        elif choice == '3':
            directed_graph_menu()
        elif choice == '4':
            weighted_graph_menu()
        elif choice == '5':
            undirected_graph_menu()
        elif choice == '0':
            break
        else:
            print("Invalid input. Please enter 1-5 or 0.")

def maze_grid_menu():
    print("\n[1] BFS\n[2] DFS\n[3] A*\n[4] Dijkstra\n[5] Bidirectional BFS\n[0] Back")
    choice = input("Select an algorithm: ").strip()
    algos = {'1': 'BFS', '2': 'DFS', '3': 'A*', '4': 'Dijkstra', '5': 'Bidirectional BFS'}
    if choice in algos:
        print(f"Launching {algos[choice]} on Maze/Grid...")  # TODO: Implement {algos[choice]}
    elif choice == '0':
        return
    else:
        print("Invalid input.")

def directed_graph_menu():
    print("Launching Directed Graph Visualizer...")
    from ui.directed_graph_visualizer import run_directed_graph_visualizer
    run_directed_graph_visualizer()

def weighted_graph_menu():
    print("Launching Weighted Graph Visualizer...")
    from ui.weighted_graph_visualizer import run_weighted_graph_visualizer
    run_weighted_graph_visualizer()

def undirected_graph_menu():
    print("Launching Undirected Graph Visualizer...")
    from ui.undirected_graph_visualizer import run_undirected_graph_visualizer
    run_undirected_graph_visualizer()
