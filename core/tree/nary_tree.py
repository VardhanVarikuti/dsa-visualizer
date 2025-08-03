"""
N-ary Tree operations
"""
from collections import deque

class NaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

def nary_bfs(root):
    print("[N-ary Tree] BFS Traversal...")
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.value)
        for child in node.children:
            queue.append(child)
    return result

def nary_dfs(root):
    print("[N-ary Tree] DFS Traversal...")
    result = []
    def dfs(node):
        if not node:
            return
        result.append(node.value)
        for child in node.children:
            dfs(child)
    dfs(root)
    return result
