"""
Dijkstra's Algorithm for grid/maze pathfinding
"""
import heapq

def dijkstra(grid, start, end, visualize=False):
    open_set = []
    heapq.heappush(open_set, (0, start, [start]))
    dist = {start: 0}
    visited = set()
    while open_set:
        cost, current, path = heapq.heappop(open_set)
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
            temp_dist = dist[current] + 1
            if neighbor not in dist or temp_dist < dist[neighbor]:
                dist[neighbor] = temp_dist
                neighbor.parent = current
                heapq.heappush(open_set, (temp_dist, neighbor, path + [neighbor]))
                if visualize:
                    yield ('visit', neighbor)
    if visualize:
        yield ('not_found', None)
    else:
        return []
