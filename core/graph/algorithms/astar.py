"""
A* Algorithm for shortest path (step-by-step visualization)
Assumes graph nodes have (x, y) positions in node_pos dict.
"""
from collections import deque

def astar(graph, source, target, node_pos, visualize=False):
    import heapq
    def heuristic(u, v):
        return 0
    dist = {v: float('inf') for v in graph.get_vertices()}
    prev = {v: None for v in graph.get_vertices()}
    dist[source] = 0
    heap = [(heuristic(source, target), 0, source)]
    visited = set()
    while heap:
        f, d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if visualize:
            yield ("visit", u, d)
        if u == target:
            break
        for v, w in graph.get_neighbors(u):
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(heap, (dist[v] + heuristic(v, target), dist[v], v))
                if visualize:
                    yield ("update", v, dist[v])
    # Reconstruct path
    path = []
    if target not in dist or dist[target] == float('inf'):
        if visualize:
            yield ("not_found", target)
        if visualize:
            yield ("done", dist, prev, path)
        return dist, prev, path
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    if visualize:
        yield ("done", dist, prev, path)
    return dist, prev, path 