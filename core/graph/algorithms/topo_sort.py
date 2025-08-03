"""
Topological Sort for directed graphs (step-by-step visualization)
"""
def topo_sort(graph, visualize=False):
    from collections import deque
    in_degree = {u: 0 for u in graph.get_vertices()}
    for u in graph.get_vertices():
        for v, _ in graph.get_neighbors(u):
            in_degree[v] = in_degree.get(v, 0) + 1
    queue = deque([u for u in graph.get_vertices() if in_degree[u] == 0])
    topo_order = []
    if visualize:
        yield ("init_queue", list(queue))
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        if visualize:
            yield ("visit", u, list(topo_order), list(queue))
        for v, _ in graph.get_neighbors(u):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                if visualize:
                    yield ("enqueue", v, list(queue))
    if len(topo_order) != len(in_degree):
        if visualize:
            yield ("cycle", None)
        return []
    if visualize:
        yield ("done", list(topo_order))
    return topo_order
