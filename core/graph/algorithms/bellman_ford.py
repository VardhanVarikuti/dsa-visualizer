"""
Bellman-Ford Algorithm for shortest paths in directed graphs (step-by-step visualization)
"""
def bellman_ford(graph, source, visualize=False):
    dist = {v: float('inf') for v in graph.get_vertices()}
    prev = {v: None for v in graph.get_vertices()}
    dist[source] = 0
    # Ensure all vertices are present in dist, even if not in graph.adj
    for u in graph.get_vertices():
        for v, w in graph.get_neighbors(u):
            if v not in dist:
                dist[v] = float('inf')
                prev[v] = None
    for _ in range(len(graph.get_vertices()) - 1):
        for u in graph.get_vertices():
            for v, w in graph.get_neighbors(u):
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    if visualize:
                        yield ("update", v, dist[v])
    # Check for negative-weight cycles
    for u in graph.get_vertices():
        for v, w in graph.get_neighbors(u):
            if dist[u] + w < dist[v]:
                if visualize:
                    yield ("negative_cycle",)
                return None, None
    if visualize:
        yield ("done", dist, prev)
    # Always return a tuple, even if visualize=True, for generator use in Johnson's algorithm
    return dist, prev
