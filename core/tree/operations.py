"""
Generic tree operations (true generic binary tree, not BST)
"""
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def find_node(root, value):
    if not root:
        return None
    if root.value == value:
        return root
    left = find_node(root.left, value)
    if left:
        return left
    right = find_node(root.right, value)
    if right:
        return right
    return None

def tree_insert(root, value, parent_value=None, side='left'):
    print(f"[Tree] Inserting {value} under {parent_value} as {side} child...")
    if not root:
        return TreeNode(value)
    if parent_value is None:
        # Insert as leftmost available spot (BFS)
        from collections import deque
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if not node.left:
                node.left = TreeNode(value)
                return root
            else:
                queue.append(node.left)
            if not node.right:
                node.right = TreeNode(value)
                return root
            else:
                queue.append(node.right)
        return root
    parent = find_node(root, parent_value)
    if not parent:
        raise ValueError(f"Parent {parent_value} not found.")
    if side == 'left':
        if parent.left:
            raise ValueError(f"Parent {parent_value} already has a left child.")
        parent.left = TreeNode(value)
    elif side == 'right':
        if parent.right:
            raise ValueError(f"Parent {parent_value} already has a right child.")
        parent.right = TreeNode(value)
    else:
        raise ValueError("Side must be 'left' or 'right'.")
    return root

def find_deepest_and_parent(root):
    from collections import deque
    queue = deque([(root, None)])
    last = (root, None)
    while queue:
        node, parent = queue.popleft()
        last = (node, parent)
        if node.left:
            queue.append((node.left, node))
        if node.right:
            queue.append((node.right, node))
    return last  # (deepest_node, its_parent)

def tree_delete(root, value):
    print(f"[Tree] Deleting {value}...")
    if not root:
        return None
    # Find node to delete and its parent
    from collections import deque
    queue = deque([(root, None)])
    node_to_delete = None
    parent_of_delete = None
    while queue:
        node, parent = queue.popleft()
        if node.value == value:
            node_to_delete = node
            parent_of_delete = parent
        if node.left:
            queue.append((node.left, node))
        if node.right:
            queue.append((node.right, node))
    if not node_to_delete:
        return root  # Not found
    # Find deepest, rightmost node and its parent
    deepest, parent_of_deepest = find_deepest_and_parent(root)
    if node_to_delete is deepest:
        # Just remove the deepest node
        if parent_of_deepest:
            if parent_of_deepest.left is deepest:
                parent_of_deepest.left = None
            else:
                parent_of_deepest.right = None
        else:
            # Deleting the only node (root)
            return None
        return root
    # Replace value
    node_to_delete.value = deepest.value
    # Remove deepest node
    if parent_of_deepest:
        if parent_of_deepest.left is deepest:
            parent_of_deepest.left = None
        else:
            parent_of_deepest.right = None
    return root

def tree_lca(root, n1, n2):
    print(f"[Tree] Finding LCA of {n1} and {n2}...")
    def helper(node):
        if not node:
            return None, 0
        left_lca, left_count = helper(node.left)
        if left_lca:
            return left_lca, 2  # propagate up the found LCA
        right_lca, right_count = helper(node.right)
        if right_lca:
            return right_lca, 2  # propagate up the found LCA
        mid = int(node.value == n1 or node.value == n2)
        total = left_count + right_count + mid
        if total == 2:
            return node, 2
        return None, total
    lca_node, count = helper(root)
    if count == 2:
        return lca_node.value
    return None
