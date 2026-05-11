"""
Main menu for DSA Visualizer
"""
def main_menu():
    while True:
        print("\n=== DSA Visualizer ===")
        print("[1] Trees")
        print("[2] Graphs")
        print("[3] Miscellaneous")
        print("[0] Exit")
        choice = input("Select an option: ").strip()
        if choice == '1':
            from menus.tree_menu import tree_menu
            tree_menu()
        elif choice == '2':
            from menus.graph_menu import graph_menu
            graph_menu()
        elif choice == '3':
            from menus.misc_menu import misc_menu
            misc_menu()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please enter 1, 2, 3, or 0.")
