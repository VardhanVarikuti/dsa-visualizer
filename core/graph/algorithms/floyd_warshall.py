"""
Floyd-Warshall Algorithm for all-pairs shortest paths (step-by-step visualization)
"""
def floyd_warshall(graph, visualize=False):
    vertices = list(graph.get_vertices())
    n = len(vertices)
    idx = {v: i for i, v in enumerate(vertices)}
    dist = [[float('inf')]*n for _ in range(n)]
    next_hop = [[None]*n for _ in range(n)]
    for u in vertices:
        dist[idx[u]][idx[u]] = 0
        for v, w in graph.get_neighbors(u):
            dist[idx[u]][idx[v]] = w
            next_hop[idx[u]][idx[v]] = v
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_hop[i][j] = next_hop[i][k]
                    if visualize:
                        yield ("update", vertices[i], vertices[j], dist[i][j])
    if visualize:
        yield ("done", dist, next_hop, vertices)
    return dist, next_hop 