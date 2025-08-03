"""
Johnson's Algorithm for all-pairs shortest paths (step-by-step visualization)
"""
from core.graph.graph import Graph
def johnson(graph, visualize=False):
    from core.graph.algorithms.bellman_ford import bellman_ford
    from core.graph.algorithms.dijkstra import dijkstra
    vertices = list(graph.get_vertices())
    new_graph = Graph(directed=True)
    for u in vertices:
        for v, w in graph.get_neighbors(u):
            new_graph.add_edge(u, v, w)
    s = '__new__'
    for v in vertices:
        new_graph.add_edge(s, v, 0)
    # Use generator to get both animation steps and the return value
    if visualize:
        gen = bellman_ford(new_graph, s, visualize=True)
        steps = []
        try:
            while True:
                steps.append(next(gen))
        except StopIteration as e:
            h_prev = e.value
        if h_prev is None or h_prev[0] is None:
            yield ("negative_cycle",)
            return None
        h, _ = h_prev
        for step in steps:
            yield step
    else:
        h, _ = bellman_ford(new_graph, s)
        if h is None:
            if visualize:
                yield ("negative_cycle",)
            return None
    # Ensure h contains all vertices (including those with no outgoing edges)
    for v in vertices + [s]:
        if v not in h:
            h[v] = float('inf')
    dist = {u: {v: float('inf') for v in vertices} for u in vertices}
    for u in vertices:
        def reweight(v, w):
            return w + h[u] - h[v]
        # Build reweighted graph for Dijkstra
        reweighted_graph = Graph(directed=True)
        for x in vertices:
            for y, w in graph.get_neighbors(x):
                reweighted_graph.add_edge(x, y, reweight(y, w))
        try:
            d, _, _ = dijkstra(reweighted_graph, u)
        except Exception as e:
            if visualize:
                yield ("error", f"Dijkstra failed for node {u}: {e}")
            continue
        for v in vertices:
            if d[v] < float('inf'):
                dist[u][v] = d[v] - h[u] + h[v]
                if visualize:
                    yield ("update", u, v, dist[u][v])
    if visualize:
        yield ("done", dist)
    return dist 