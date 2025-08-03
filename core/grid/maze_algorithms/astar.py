"""
A* Search for grid/maze pathfinding
"""
import heapq

def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def astar(grid, start, end, visualize=False):
    open_set = []
    heapq.heappush(open_set, (0, start, [start]))
    g_score = {start: 0}
    visited = set()
    while open_set:
        _, current, path = heapq.heappop(open_set)
        if current == end:
            if visualize:
                yield ('found', path)
            else:
                return path
            return
        if current in visited:
            continue
        visited.add(current)
        for neighbor in grid.get_neighbors(current):
            temp_g = g_score[current] + 1
            if neighbor not in g_score or temp_g < g_score[neighbor]:
                g_score[neighbor] = temp_g
                f_score = temp_g + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score, neighbor, path + [neighbor]))
                if visualize:
                    yield ('visit', neighbor)
    if visualize:
        yield ('not_found', None)
    else:
        return []
