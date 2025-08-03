"""
AVL Tree operations
"""
class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

def get_height(node):
    return node.height if node else 0

def update_height(node):
    node.height = 1 + max(get_height(node.left), get_height(node.right))

def get_balance(node):
    return get_height(node.left) - get_height(node.right) if node else 0

def rotate_right(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    update_height(y)
    update_height(x)
    return x

def rotate_left(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    update_height(x)
    update_height(y)
    return y

def avl_insert(root, value):
    print(f"[AVL] Inserting {value}...")
    if not root:
        return AVLNode(value)
    if value < root.value:
        root.left = avl_insert(root.left, value)
    elif value > root.value:
        root.right = avl_insert(root.right, value)
    else:
        return root
    update_height(root)
    balance = get_balance(root)
    # Left Left
    if balance > 1 and value < root.left.value:
        return rotate_right(root)
    # Right Right
    if balance < -1 and value > root.right.value:
        return rotate_left(root)
    # Left Right
    if balance > 1 and value > root.left.value:
        root.left = rotate_left(root.left)
        return rotate_right(root)
    # Right Left
    if balance < -1 and value < root.right.value:
        root.right = rotate_right(root.right)
        return rotate_left(root)
    return root

def avl_delete(root, value):
    print(f"[AVL] Deleting {value}...")
    if not root:
        return root
    if value < root.value:
        root.left = avl_delete(root.left, value)
    elif value > root.value:
        root.right = avl_delete(root.right, value)
    else:
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
        temp = root.right
        while temp.left:
            temp = temp.left
        root.value = temp.value
        root.right = avl_delete(root.right, temp.value)
    update_height(root)
    balance = get_balance(root)
    # Left Left
    if balance > 1 and get_balance(root.left) >= 0:
        return rotate_right(root)
    # Left Right
    if balance > 1 and get_balance(root.left) < 0:
        root.left = rotate_left(root.left)
        return rotate_right(root)
    # Right Right
    if balance < -1 and get_balance(root.right) <= 0:
        return rotate_left(root)
    # Right Left
    if balance < -1 and get_balance(root.right) > 0:
        root.right = rotate_right(root.right)
        return rotate_left(root)
    return root

def avl_balance(root):
    print("[AVL] Balancing tree...")
    update_height(root)
    balance = get_balance(root)
    if balance > 1:
        if get_balance(root.left) < 0:
            root.left = rotate_left(root.left)
        return rotate_right(root)
    if balance < -1:
        if get_balance(root.right) > 0:
            root.right = rotate_right(root.right)
        return rotate_left(root)
    return root
