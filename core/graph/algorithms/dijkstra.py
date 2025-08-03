"""
Dijkstra's Algorithm for shortest path (step-by-step visualization)
"""
def dijkstra(graph, source, visualize=False):
    import heapq
    dist = {v: float('inf') for v in graph.get_vertices()}
    prev = {v: None for v in graph.get_vertices()}
    dist[source] = 0
    heap = [(0, source)]
    visited = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if visualize:
            yield ("visit", u, d)
        for v, w in graph.get_neighbors(u):
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
                if visualize:
                    yield ("update", v, dist[v])
    # Reconstruct paths for all nodes
    paths = {}
    for target in dist:
        path = []
        cur = target
        while cur is not None:
            path.append(cur)
            cur = prev.get(cur, None)
        path.reverse()
        if len(path) > 1 or (len(path) == 1 and path[0] == source):
            paths[target] = path
        else:
            paths[target] = []
    if visualize:
        yield ("done", dist, prev, paths)
    return dist, prev, paths 