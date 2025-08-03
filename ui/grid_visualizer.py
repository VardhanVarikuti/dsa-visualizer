"""
Pygame Grid Visualizer for Pathfinding Algorithms (Improved UI & Robustness, Large Window)
"""
import pygame
from core.grid.grid import Grid, Cell
from core.grid.maze_algorithms.bfs import bfs
from core.grid.maze_algorithms.dfs import dfs
from core.grid.maze_algorithms.astar import astar
from core.grid.maze_algorithms.dijkstra import dijkstra
from core.grid.maze_algorithms.bidir_bfs import bidirectional_bfs

# --- Constants ---
CELL_SIZE = 28
ROWS, COLS = 22, 36
WIDTH, HEIGHT = 1200, 800
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (200,200,200)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,165,0)
CYAN = (0,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
ERROR_COLOR = (255, 80, 80)
DARK_BLUE = (0, 60, 180)

# --- Helper Functions ---
def draw_grid(win, grid, start, end, path=None, visited=None):
    grid_width = COLS * CELL_SIZE
    grid_height = ROWS * CELL_SIZE
    offset_x = (WIDTH - grid_width) // 2
    offset_y = (HEIGHT - grid_height) // 2
    # Draw grid border
    pygame.draw.rect(win, (60, 60, 60), (offset_x-2, offset_y-2, grid_width+4, grid_height+4), 3)
    for r in range(grid.rows):
        for c in range(grid.cols):
            cell = grid.grid[r][c]
            color = WHITE
            if cell.is_wall:
                color = BLACK
            elif start and cell == start:
                color = ORANGE
            elif end and cell == end:
                color = CYAN
            elif path and cell in path:
                color = YELLOW
            elif visited and cell in visited:
                color = BLUE
            pygame.draw.rect(win, color, (offset_x + c*CELL_SIZE, offset_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(win, GREY, (offset_x + c*CELL_SIZE, offset_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

def get_cell_from_pos(pos):
    x, y = pos
    grid_width = COLS * CELL_SIZE
    grid_height = ROWS * CELL_SIZE
    offset_x = (WIDTH - grid_width) // 2
    offset_y = (HEIGHT - grid_height) // 2
    col = (x - offset_x) // CELL_SIZE
    row = (y - offset_y) // CELL_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col
    return None, None

def show_message(win, font, msg, color=BLACK, y_offset=0):
    text = font.render(msg, True, color)
    win.blit(text, (10, HEIGHT-30+y_offset))

# --- Main Visualizer ---
def run_grid_visualizer():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT+80))
    pygame.display.set_caption("Grid Pathfinding Visualizer")
    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()
    grid = Grid(ROWS, COLS)
    start = end = None
    running = True
    placing_wall = False
    removing_wall = False
    path = []
    visited = set()
    error_msg = ''
    message = 'Left-click: wall/start/end | Right-click: erase | B/D/A/J/X: Run | R: Reset | Q: Quit | H: Help'
    hovered = None
    show_help = False
    while running:
        win.fill(WHITE)
        draw_grid(win, grid, start, end, path, visited)
        # Highlight hovered cell
        if hovered:
            grid_width = COLS * CELL_SIZE
            grid_height = ROWS * CELL_SIZE
            offset_x = (WIDTH - grid_width) // 2
            offset_y = (HEIGHT - grid_height) // 2
            r, c = hovered
            pygame.draw.rect(win, (120, 200, 255), (offset_x + c*CELL_SIZE, offset_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
        # Help overlay
        if show_help:
            overlay = pygame.Surface((WIDTH, HEIGHT+80), pygame.SRCALPHA)
            overlay.fill((240, 240, 255, 220))
            win.blit(overlay, (0, 0))
            help_lines = [
                "GRID PATHFINDING VISUALIZER - HELP",
                "",
                "CONTROLS:",
                "Left Click: Place wall, start, or end node",
                "Right Click: Erase wall, start, or end node",
                "Mouse Drag: Draw/erase walls",
                "B: Run BFS   |   D: Run DFS   |   A: Run A*",
                "J: Run Dijkstra   |   X: Run Bidirectional BFS",
                "R: Reset grid   |   Q: Quit",
                "H: Toggle this help overlay",
                "",
                "INSTRUCTIONS:",
                "1. Left-click to place the start node (orange), then the end node (cyan).",
                "2. Continue left-clicking/dragging to add walls (black).",
                "3. Right-click to erase walls, start, or end node.",
                "4. Press B, D, A, J, or X to run the selected algorithm.",
                "5. Press R to reset the grid, Q to quit, H to toggle help.",
            ]
            help_font = pygame.font.SysFont(None, 32)
            for i, line in enumerate(help_lines):
                surf = help_font.render(line, True, (30, 30, 80))
                rect = surf.get_rect(center=(WIDTH//2, 60 + i*38))
                win.blit(surf, rect)
        # Draw instructions and error below the grid (drawn even if help is up, but overlay covers it)
        show_message(win, font, message, DARK_BLUE, y_offset=40)
        if error_msg:
            show_message(win, font, error_msg, ERROR_COLOR, y_offset=70)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            try:
                if event.type == pygame.MOUSEMOTION:
                    row, col = get_cell_from_pos(pygame.mouse.get_pos())
                    if row is not None and col is not None:
                        hovered = (row, col)
                    else:
                        hovered = None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    row, col = get_cell_from_pos(pygame.mouse.get_pos())
                    if row is None or col is None:
                        error_msg = "Click inside the grid."
                        continue
                    error_msg = ''
                    if event.button == 1:  # Left click
                        if not start:
                            start = grid.grid[row][col]
                        elif not end and grid.grid[row][col] != start:
                            end = grid.grid[row][col]
                        elif grid.grid[row][col] != start and grid.grid[row][col] != end:
                            grid.grid[row][col].is_wall = True
                            placing_wall = True
                    elif event.button == 3:  # Right click
                        if grid.grid[row][col] == start:
                            start = None
                        elif grid.grid[row][col] == end:
                            end = None
                        else:
                            grid.grid[row][col].is_wall = False
                            removing_wall = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    placing_wall = False
                    removing_wall = False
                elif event.type == pygame.MOUSEMOTION:
                    row, col = get_cell_from_pos(pygame.mouse.get_pos())
                    if row is None or col is None:
                        continue
                    if placing_wall and grid.grid[row][col] != start and grid.grid[row][col] != end:
                        grid.grid[row][col].is_wall = True
                    if removing_wall and grid.grid[row][col] != start and grid.grid[row][col] != end:
                        grid.grid[row][col].is_wall = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        show_help = not show_help
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_r:
                        grid = Grid(ROWS, COLS)
                        start = end = None
                        path = []
                        visited = set()
                        error_msg = ''
                    elif event.key == pygame.K_b and start and end:
                        try:
                            path, visited = run_algo_with_vis(bfs, grid, start, end, win, font)
                            error_msg = ''
                        except Exception as e:
                            error_msg = f"BFS error: {e}"
                    elif event.key == pygame.K_d and start and end:
                        try:
                            path, visited = run_algo_with_vis(dfs, grid, start, end, win, font)
                            error_msg = ''
                        except Exception as e:
                            error_msg = f"DFS error: {e}"
                    elif event.key == pygame.K_a and start and end:
                        try:
                            path, visited = run_algo_with_vis(astar, grid, start, end, win, font)
                            error_msg = ''
                        except Exception as e:
                            error_msg = f"A* error: {e}"
                    elif event.key == pygame.K_j and start and end:
                        try:
                            path, visited = run_algo_with_vis(dijkstra, grid, start, end, win, font)
                            error_msg = ''
                        except Exception as e:
                            error_msg = f"Dijkstra error: {e}"
                    elif event.key == pygame.K_x and start and end:
                        try:
                            path, visited = run_algo_with_vis(bidirectional_bfs, grid, start, end, win, font)
                            error_msg = ''
                        except Exception as e:
                            error_msg = f"Bi-BFS error: {e}"
            except Exception as e:
                error_msg = f"Error: {e}"
        clock.tick(FPS)
    pygame.quit()

def run_algo_with_vis(algo_func, grid, start, end, win, font):
    visited = set()
    path = []
    # Use generator-based visualization for step-by-step animation
    gen = None
    if algo_func == bfs or algo_func == dfs:
        gen = algo_func(grid, start, end, visualize=True)
    elif algo_func == astar or algo_func == dijkstra or algo_func == bidirectional_bfs:
        gen = algo_func(grid, start, end, visualize=True)
    else:
        result = algo_func(grid, start, end)
        return result, set()
    found_path = None
    for step in gen:
        # Process events to keep window responsive during animation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
        if isinstance(step, tuple) and step[0] == 'visit':
            cell = step[1]
            visited.add(cell)
        elif isinstance(step, tuple) and step[0] == 'found':
            found_path = step[1]
            break
        elif isinstance(step, tuple) and step[0] == 'not_found':
            break
        draw_grid(win, grid, start, end, path, visited)
        pygame.display.update()
        pygame.time.delay(30)
    if found_path:
        for cell in found_path:
            path.append(cell)
            draw_grid(win, grid, start, end, path, visited)
            pygame.display.update()
            pygame.time.delay(50)
    return path, visited

if __name__ == "__main__":
    run_grid_visualizer()