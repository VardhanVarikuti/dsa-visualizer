"""
Depth-First Search (DFS) for grid/maze pathfinding
"""
def dfs(grid, start, end, visualize=False):
    stack = [(start, [start])]
    visited = set()
    visited.add(start)
    while stack:
        current, path = stack.pop()
        if current == end:
            if visualize:
                yield ('found', path)
            else:
                return path
            return
        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited and not neighbor.is_wall:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))
                if visualize:
                    yield ('visit', neighbor)
    if visualize:
        yield ('not_found', None)
    else:
        return []
