"""
Simple Grid and Cell classes for pathfinding algorithms
"""
class Cell:
    def __init__(self, row, col, is_wall=False):
        self.row = row
        self.col = col
        self.is_wall = is_wall
        self.visited = False
        self.parent = None

    def __repr__(self):
        return f"Cell({self.row},{self.col})"

    def __eq__(self, other):
        return isinstance(other, Cell) and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

    def __lt__(self, other):
        return (self.row, self.col) < (other.row, other.col)

    # Add a dummy neighbors property for compatibility (will raise if used incorrectly)
    @property
    def neighbors(self):
        raise AttributeError("Use grid.get_neighbors(cell) instead of cell.neighbors")

class Grid:
    def __init__(self, rows, cols, walls=None):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        if walls:
            for (r, c) in walls:
                self.grid[r][c].is_wall = True

    def get_neighbors(self, cell):
        neighbors = []
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = cell.row + dr, cell.col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor = self.grid[nr][nc]
                if not neighbor.is_wall:
                    neighbors.append(neighbor)
        return neighbors
