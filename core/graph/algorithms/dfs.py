"""
Depth-First Search (DFS) for directed/unweighted graphs
"""
def dfs(graph, start):
    print("[DFS] Running DFS on directed/unweighted graph...")
    visited = set()
    stack = [start]
    while stack:
        u = stack.pop()
        if u not in visited:
            yield u
            visited.add(u)
            for v, _ in reversed(graph.get_neighbors(u)):
                if v not in visited:
                    stack.append(v) 