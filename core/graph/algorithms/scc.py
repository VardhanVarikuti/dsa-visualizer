"""
Strongly Connected Components (SCC) for directed graphs (Kosaraju's algorithm, step-by-step visualization)
"""
def strongly_connected_components(graph, visualize=False):
    visited = set()
    order = []
    def dfs(u):
        visited.add(u)
        if visualize:
            yield ("visit", u, "first")
        for v, _ in graph.get_neighbors(u):
            if v not in visited:
                yield from dfs(v)
        order.append(u)
        if visualize:
            yield ("finish", u, list(order))
    for u in graph.get_vertices():
        if u not in visited:
            yield from dfs(u)
    # Transpose graph
    transpose = {u: [] for u in graph.get_vertices()}
    for u in graph.get_vertices():
        for v, _ in graph.get_neighbors(u):
            transpose[v].append(u)
    if visualize:
        yield ("transpose", transpose)
    # Second pass
    visited.clear()
    sccs = []
    def dfs_transpose(u, component):
        visited.add(u)
        component.append(u)
        if visualize:
            yield ("visit", u, "second")
        for v in transpose[u]:
            if v not in visited:
                yield from dfs_transpose(v, component)
    for u in reversed(order):
        if u not in visited:
            component = []
            yield from dfs_transpose(u, component)
            sccs.append(component)
            if visualize:
                yield ("component", list(component), list(sccs))
    if visualize:
        yield ("done", list(sccs))
    return sccs 