"""
Cycle detection for directed graphs (using DFS, step-by-step visualization)
"""
def has_cycle(graph, visualize=False):
    visited = set()
    rec_stack = set()
    path = []
    found_cycle = []
    def dfs(u):
        visited.add(u)
        rec_stack.add(u)
        path.append(u)
        if visualize:
            yield ("visit", u, list(path), list(rec_stack))
        for v, _ in graph.get_neighbors(u):
            if v not in visited:
                for step in dfs(v):
                    yield step
                if found_cycle:
                    return
            elif v in rec_stack and not found_cycle:
                # Found a cycle
                idx = path.index(v) if v in path else 0
                found_cycle.extend(path[idx:] + [v])
                if visualize:
                    yield ("cycle", list(found_cycle))
                return
        rec_stack.remove(u)
        path.pop()
    for u in graph.get_vertices():
        if u not in visited:
            gen = dfs(u)
            for step in gen:
                yield step
            if found_cycle:
                break
    if visualize:
        yield ("done", bool(found_cycle), found_cycle)
    return bool(found_cycle) 