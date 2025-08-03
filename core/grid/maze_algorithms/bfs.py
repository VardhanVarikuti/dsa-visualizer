"""
Breadth-First Search (BFS) for grid/maze pathfinding
"""
from collections import deque

def bfs(grid, start, end, visualize=False):
    queue = deque()
    queue.append((start, [start]))
    visited = set()
    visited.add(start)
    while queue:
        current, path = queue.popleft()
        if current == end:
            if visualize:
                yield ('found', path)
            else:
                return path
            return
        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited and not neighbor.is_wall:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
                if visualize:
                    yield ('visit', neighbor)
    if visualize:
        yield ('not_found', None)
    else:
        return []
