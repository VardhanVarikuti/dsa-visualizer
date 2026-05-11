"""
Graph menu for DSA Visualizer
Only graph-specific algorithms and visualizers.
"""
def graph_menu():
    while True:
        print("\n--- Graph Algorithms ---")
        print("[1] Undirected Graph")
        print("[2] Directed Graph")
        print("[3] Weighted Graph")
        print("[0] Back")
        choice = input("Select an option: ").strip()
        if choice == '1':
            undirected_graph_menu()
        elif choice == '2':
            directed_graph_menu()
        elif choice == '3':
            weighted_graph_menu()
        elif choice == '0':
            break
        else:
            print("Invalid input. Please enter 1-3 or 0.")

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
