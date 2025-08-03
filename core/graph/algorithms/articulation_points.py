"""
Articulation Points and Bridges for undirected graphs (Tarjan's Algorithm, step-by-step visualization)
"""
def articulation_points_and_bridges(graph, visualize=False):
    time = [0]
    disc = {}
    low = {}
    parent = {}
    ap = set()
    bridges = []
    def dfs(u):
        children = 0
        disc[u] = low[u] = time[0]
        time[0] += 1
        if visualize:
            yield ("visit", u, disc[u], low[u])
        for v, _ in graph.get_neighbors(u):
            if v not in disc:
                parent[v] = u
                children += 1
                for step in dfs(v):
                    yield step
                low[u] = min(low[u], low[v])
                # Articulation point
                if parent.get(u) is None and children > 1:
                    ap.add(u)
                    if visualize:
                        yield ("ap", u)
                if parent.get(u) is not None and low[v] >= disc[u]:
                    ap.add(u)
                    if visualize:
                        yield ("ap", u)
                # Bridge
                if low[v] > disc[u]:
                    bridges.append((u, v))
                    if visualize:
                        yield ("bridge", (u, v))
            elif v != parent.get(u):
                low[u] = min(low[u], disc[v])
    for u in graph.get_vertices():
        if u not in disc:
            parent[u] = None
            gen = dfs(u)
            for step in gen:
                yield step
    if visualize:
        yield ("done", list(ap), bridges)
    return ap, bridges 