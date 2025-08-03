"""
Cycle detection for undirected graphs (DFS + parent, step-by-step visualization)
"""
def has_cycle_undirected(graph, visualize=False):
    visited = set()
    path = []
    found_cycle = []
    def dfs(u, parent):
        visited.add(u)
        path.append(u)
        if visualize:
            yield ("visit", u, list(path))
        for v, _ in graph.get_neighbors(u):
            if v not in visited:
                for step in dfs(v, u):
                    yield step
                if found_cycle:
                    return
            elif v != parent and not found_cycle:
                # Found a cycle
                idx = path.index(v) if v in path else 0
                found_cycle.extend(path[idx:] + [v])
                if visualize:
                    yield ("cycle", list(found_cycle))
                return
        path.pop()
    for u in graph.get_vertices():
        if u not in visited:
            gen = dfs(u, None)
            for step in gen:
                yield step
            if found_cycle:
                break
    if visualize:
        yield ("done", bool(found_cycle), found_cycle)
    return bool(found_cycle) 