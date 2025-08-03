"""
Connected Components for undirected graphs (BFS, step-by-step visualization)
"""
def connected_components(graph, visualize=False):
    visited = set()
    components = []
    color_map = {}
    color_id = 0
    for u in graph.get_vertices():
        if u not in visited:
            comp = []
            queue = [u]
            if visualize:
                yield ("new_component", color_id)
            while queue:
                v = queue.pop(0)
                if v not in visited:
                    visited.add(v)
                    comp.append(v)
                    color_map[v] = color_id
                    if visualize:
                        yield ("visit", v, color_id)
                    for w, _ in graph.get_neighbors(v):
                        if w not in visited:
                            queue.append(w)
            components.append(comp)
            color_id += 1
    if visualize:
        yield ("done", components, color_map)
    return components 