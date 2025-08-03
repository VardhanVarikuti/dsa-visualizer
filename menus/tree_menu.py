"""
Tree menu for DSA Visualizer
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
        if choice == '2':
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
        elif choice == '1':
            from ui.generic_tree_visualizer import run_generic_tree_visualizer
            run_generic_tree_visualizer()
        elif choice == '0':
            break
        else:
            print("Invalid input. Please enter 1-5 or 0.")

def bst_menu():
    print("\n[1] Insert\n[2] Delete\n[3] Traversals\n[4] LCA\n[0] Back")
    choice = input("Select an operation: ").strip()
    ops = {'1': 'Insert', '2': 'Delete', '3': 'Traversals', '4': 'LCA'}
    if choice in ops:
        print(f"Launching {ops[choice]} on BST...")  # TODO: Implement {ops[choice]}
    elif choice == '0':
        return
    else:
        print("Invalid input.")

def avl_menu():
    print("\n[1] Insert\n[2] Delete\n[3] Balancing\n[0] Back")
    choice = input("Select an operation: ").strip()
    ops = {'1': 'Insert', '2': 'Delete', '3': 'Balancing'}
    if choice in ops:
        print(f"Launching {ops[choice]} on AVL Tree...")  # TODO: Implement {ops[choice]}
    elif choice == '0':
        return
    else:
        print("Invalid input.")

def trie_menu():
    print("\n[1] Insert\n[2] Search\n[3] Prefix Matching\n[0] Back")
    choice = input("Select an operation: ").strip()
    ops = {'1': 'Insert', '2': 'Search', '3': 'Prefix Matching'}
    if choice in ops:
        print(f"Launching {ops[choice]} on Trie...")  # TODO: Implement {ops[choice]}
    elif choice == '0':
        return
    else:
        print("Invalid input.")

def nary_tree_menu():
    print("\n[1] BFS Traversal\n[2] DFS Traversal\n[0] Back")
    choice = input("Select an operation: ").strip()
    ops = {'1': 'BFS Traversal', '2': 'DFS Traversal'}
    if choice in ops:
        print(f"Launching {ops[choice]} on N-ary Tree...")  # TODO: Implement {ops[choice]}
    elif choice == '0':
        return
    else:
        print("Invalid input.")
