"""
Bidirectional BFS for grid/maze pathfinding
"""
from collections import deque

def reconstruct_path(meet, parents_start, parents_end):
    # Reconstruct path from start to meet and meet to end
    path = []
    node = meet
    while node:
        path.append(node)
        node = parents_start.get((node.row, node.col))
    path = path[::-1]
    node = parents_end.get((meet.row, meet.col))
    while node:
        path.append(node)
        node = parents_end.get((node.row, node.col))
    return path

def bidirectional_bfs(grid, start, end, visualize=False):
    if start == end:
        if visualize:
            yield ('found', [start])
        else:
            return [start]
        return
    queue_start = deque([start])
    queue_end = deque([end])
    visited_start = {(start.row, start.col)}
    visited_end = {(end.row, end.col)}
    parents_start = {(start.row, start.col): None}
    parents_end = {(end.row, end.col): None}
    while queue_start and queue_end:
        # Expand from start
        current = queue_start.popleft()
        for neighbor in grid.get_neighbors(current):
            key = (neighbor.row, neighbor.col)
            if key not in visited_start:
                parents_start[key] = current
                visited_start.add(key)
                queue_start.append(neighbor)
                if visualize:
                    yield ('visit', neighbor)
                if key in visited_end:
                    path = reconstruct_path(neighbor, parents_start, parents_end)
                    if visualize:
                        yield ('found', path)
                    else:
                        return path
                    return
        # Expand from end
        current = queue_end.popleft()
        for neighbor in grid.get_neighbors(current):
            key = (neighbor.row, neighbor.col)
            if key not in visited_end:
                parents_end[key] = current
                visited_end.add(key)
                queue_end.append(neighbor)
                if visualize:
                    yield ('visit', neighbor)
                if key in visited_start:
                    path = reconstruct_path(neighbor, parents_start, parents_end)
                    if visualize:
                        yield ('found', path)
                    else:
                        return path
                    return
    if visualize:
        yield ('not_found', None)
    else:
        return []
