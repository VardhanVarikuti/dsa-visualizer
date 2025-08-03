"""
SPFA (Shortest Path Faster Algorithm) for shortest path (step-by-step visualization)
"""
def spfa(graph, source, visualize=False):
    from collections import deque
    dist = {v: float('inf') for v in graph.get_vertices()}
    prev = {v: None for v in graph.get_vertices()}
    in_queue = {v: False for v in graph.get_vertices()}
    count = {v: 0 for v in graph.get_vertices()}
    dist[source] = 0
    queue = deque([source])
    in_queue[source] = True
    while queue:
        u = queue.popleft()
        in_queue[u] = False
        if visualize:
            yield ("visit", u, dist[u])
        for v, w in graph.get_neighbors(u):
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                prev[v] = u
                if not in_queue[v]:
                    queue.append(v)
                    in_queue[v] = True
                count[v] += 1
                if count[v] > len(graph.get_vertices()):
                    if visualize:
                        yield ("negative_cycle",)
                    return None, None
                if visualize:
                    yield ("update", v, dist[v])
    if visualize:
        yield ("done", dist, prev)
    return dist, prev 