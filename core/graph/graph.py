"""
Simple Graph class for algorithms (adjacency list)
"""
class Graph:
    def __init__(self, directed=False):
        self.adj = {}
        self.directed = directed

    def add_edge(self, u, v, weight=1):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append((v, weight))
        if not self.directed:
            if v not in self.adj:
                self.adj[v] = []
            self.adj[v].append((u, weight))

    def get_vertices(self):
        return list(self.adj.keys())

    def get_neighbors(self, u):
        return self.adj.get(u, [])
