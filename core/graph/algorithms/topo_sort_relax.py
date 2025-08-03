"""
Shortest path in DAG using Topological Sort + Relaxation (step-by-step visualization)
"""
def topo_sort_relax(graph, source, visualize=False):
    from collections import deque
    # Calculate in-degrees
    in_degree = {u: 0 for u in graph.get_vertices()}
    for u in graph.get_vertices():
        for v, _ in graph.get_neighbors(u):
            in_degree[v] = in_degree.get(v, 0) + 1
    
    # Topological sort using Kahn's algorithm
    queue = deque([u for u in graph.get_vertices() if in_degree[u] == 0])
    topo_order = []
    
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        # Decrease in-degree of neighbors
        for v, _ in graph.get_neighbors(u):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    # Initialize distances
    dist = {v: float('inf') for v in graph.get_vertices()}
    prev = {v: None for v in graph.get_vertices()}
    dist[source] = 0
    
    # Process vertices in topological order and relax edges
    for u in topo_order:
        if visualize:
            yield ("visit", u, dist[u])
        
        # Relax all edges from u
        for v, w in graph.get_neighbors(u):
            if dist[u] != float('inf') and dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                prev[v] = u
                if visualize:
                    yield ("update", v, dist[v])
    
    if visualize:
        yield ("done", dist, prev)
    return dist, prev 