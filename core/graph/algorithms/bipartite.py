"""
Bipartite check for undirected graphs (BFS 2-coloring, step-by-step visualization)
"""
def is_bipartite(graph, visualize=False):
    color = {}
    conflict = None
    for u in graph.get_vertices():
        if u not in color:
            queue = [u]
            color[u] = 0
            if visualize:
                yield ("color", u, 0)
            while queue:
                v = queue.pop(0)
                for w, _ in graph.get_neighbors(v):
                    if w not in color:
                        color[w] = 1 - color[v]
                        if visualize:
                            yield ("color", w, color[w])
                        queue.append(w)
                    elif color[w] == color[v]:
                        conflict = (v, w)
                        if visualize:
                            yield ("conflict", v, w)
                        if visualize:
                            yield ("done", False, color, conflict)
                        return False
    if visualize:
        yield ("done", True, color, None)
    return True 