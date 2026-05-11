"""
Tree menu for DSA Visualizer
Only tree-specific data structures and visualizers.
"""
def tree_menu():
    while True:
        print("\n--- Tree Algorithms ---")
        print("[1] Generic Binary Tree")
        print("[2] BST")
        print("[3] AVL")
        print("[4] Trie")
        print("[5] N-ary Tree")
        print("[0] Back")
        choice = input("Select an option: ").strip()
        if choice == '1':
            from ui.generic_tree_visualizer import run_generic_tree_visualizer
            run_generic_tree_visualizer()
        elif choice == '2':
            from ui.tree_visualizer import run_tree_visualizer
            run_tree_visualizer('BST')
        elif choice == '3':
            from ui.tree_visualizer import run_tree_visualizer
            run_tree_visualizer('AVL')
        elif choice == '4':
            from ui.trie_visualizer import run_trie_visualizer
            run_trie_visualizer()
        elif choice == '5':
            from ui.nary_tree_visualizer import run_nary_tree_visualizer
            run_nary_tree_visualizer()
        elif choice == '0':
            break
        else:
            print("Invalid input. Please enter 1-5 or 0.")
