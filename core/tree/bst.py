"""
Binary Search Tree (BST) operations
"""
class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def bst_insert(root, value):
    print(f"[BST] Inserting {value}...")
    if root is None:
        return BSTNode(value)
    if value < root.value:
        root.left = bst_insert(root.left, value)
    elif value > root.value:
        root.right = bst_insert(root.right, value)
    return root

def bst_delete(root, value):
    print(f"[BST] Deleting {value}...")
    if root is None:
        return None
    if value < root.value:
        root.left = bst_delete(root.left, value)
    elif value > root.value:
        root.right = bst_delete(root.right, value)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        # Find inorder successor
        succ = root.right
        while succ.left:
            succ = succ.left
        root.value = succ.value
        root.right = bst_delete(root.right, succ.value)
    return root

def bst_traversals(root):
    print("[BST] Traversing tree (inorder, preorder, postorder)...")
    def inorder(node):
        return inorder(node.left) + [node.value] + inorder(node.right) if node else []
    def preorder(node):
        return [node.value] + preorder(node.left) + preorder(node.right) if node else []
    def postorder(node):
        return postorder(node.left) + postorder(node.right) + [node.value] if node else []
    return {
        'inorder': inorder(root),
        'preorder': preorder(root),
        'postorder': postorder(root)
    }

def bst_lca(root, n1, n2):
    print(f"[BST] Finding LCA of {n1} and {n2}...")
    while root:
        if n1 < root.value and n2 < root.value:
            root = root.left
        elif n1 > root.value and n2 > root.value:
            root = root.right
        else:
            return root.value if root else None
    return None
