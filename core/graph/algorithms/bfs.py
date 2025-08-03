"""
Breadth-First Search (BFS) for directed/unweighted graphs
"""
def bfs(graph, start):
    print("[BFS] Running BFS on directed/unweighted graph...")
    from collections import deque
    visited = set()
    queue = deque([start])
    while queue:
        u = queue.popleft()
        if u not in visited:
            yield u
            visited.add(u)
            for v, _ in graph.get_neighbors(u):
                if v not in visited:
                    queue.append(v) 