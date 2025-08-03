"""
Transitive Closure for directed graphs (Floyd-Warshall, step-by-step visualization)
"""
def transitive_closure(graph, visualize=False):
    vertices = list(graph.get_vertices())
    n = len(vertices)
    idx = {v: i for i, v in enumerate(vertices)}
    closure = [[0]*n for _ in range(n)]
    for u in vertices:
        for v, _ in graph.get_neighbors(u):
            closure[idx[u]][idx[v]] = 1
    for i in range(n):
        closure[i][i] = 1
    if visualize:
        yield ("init", [row[:] for row in closure], vertices)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if closure[i][j] or (closure[i][k] and closure[k][j]):
                    if not closure[i][j]:
                        closure[i][j] = 1
                        if visualize:
                            yield ("update", i, j, k, [row[:] for row in closure])
    if visualize:
        yield ("done", [row[:] for row in closure], vertices)
    return closure 