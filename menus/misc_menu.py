"""
Miscellaneous menu for DSA Visualizer
Contains algorithms that are not strictly tree or graph based.
"""
def misc_menu():
    while True:
        print("\n--- Miscellaneous ---")
        print("[1] Maze/Grid Pathfinding")
        print("[2] N-Queens (Backtracking)")
        print("[0] Back")
        choice = input("Select an option: ").strip()
        if choice == '1':
            from ui.grid_visualizer import run_grid_visualizer
            run_grid_visualizer()
        elif choice == '2':
            print("Launching Backtracking on N-Queens...")
            from ui.nqueens_visualizer import run_nqueens_visualizer
            run_nqueens_visualizer()
        elif choice == '0':
            break
        else:
            print("Invalid input. Please enter 1, 2, or 0.")
