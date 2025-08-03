"""
Minimum Spanning Tree (MST) algorithms: Kruskal and Prim (step-by-step visualization)
"""
def kruskal(graph, visualize=False):
    parent = {}
    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u
    def union(u, v):
        pu, pv = find(u), find(v)
        if pu != pv:
            parent[pu] = pv
    edges = []
    for u in graph.get_vertices():
        for v, w in graph.get_neighbors(u):
            if (v, u, w) not in edges:  # avoid double counting
                edges.append((u, v, w))
    edges.sort(key=lambda x: x[2])
    for u in graph.get_vertices():
        parent[u] = u
    mst = []
    for u, v, w in edges:
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, w))
            if visualize:
                yield ("add_edge", u, v, w)
    if visualize:
        yield ("done", mst)
    return mst

def prim(graph, visualize=False):
    import heapq
    vertices = graph.get_vertices()
    if not vertices:
        return []
    start = vertices[0]
    visited = set([start])
    heap = []
    for v, w in graph.get_neighbors(start):
        heapq.heappush(heap, (w, start, v))
    mst = []
    while heap and len(visited) < len(vertices):
        w, u, v = heapq.heappop(heap)
        if v not in visited:
            visited.add(v)
            mst.append((u, v, w))
            if visualize:
                yield ("add_edge", u, v, w)
            for to, weight in graph.get_neighbors(v):
                if to not in visited:
                    heapq.heappush(heap, (weight, v, to))
    if visualize:
        yield ("done", mst)
    return mst
