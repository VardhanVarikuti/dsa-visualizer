import pygame
import sys

WIDTH, HEIGHT = 1200, 800
BOARD_TOP = 60
BOARD_MARGIN = 40
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (200,200,200)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,200,0)
DARK_BLUE = (0, 60, 180)
ERROR_COLOR = (255, 80, 80)

FONT_SIZE = 32

# --- N-Queens Backtracking Generator ---
def nqueens_solver(N):
    board = [-1] * N
    def is_safe(row, col):
        for r in range(row):
            c = board[r]
            if c == col or abs(row - r) == abs(col - c):
                return False
        return True
    def solve(row):
        if row == N:
            yield ('solution', list(board))
            return
        for col in range(N):
            if is_safe(row, col):
                board[row] = col
                yield ('place', row, col, list(board))
                yield from solve(row+1)
                board[row] = -1
                yield ('remove', row, col, list(board))
    return solve(0)

# --- Drawing Functions ---
def draw_board(win, N, board, highlight=None):
    # Make the board responsive to window dimensions
    drawable_width = WIDTH - 2*BOARD_MARGIN
    drawable_height = HEIGHT - BOARD_TOP - 100  # Reserve 100px for messages
    board_size = min(drawable_width, drawable_height)
    cell_size = board_size // N

    start_x = (WIDTH - (cell_size * N)) // 2
    start_y = BOARD_TOP

    # Draw chessboard cells
    for r in range(N):
        for c in range(N):
            color = WHITE if (r+c)%2==0 else GREY
            pygame.draw.rect(win, color, (start_x + c*cell_size, start_y + r*cell_size, cell_size, cell_size))
            if highlight and (r, c) in highlight:
                pygame.draw.rect(win, RED, (start_x + c*cell_size, start_y + r*cell_size, cell_size, cell_size), 4)
    # Draw queens
    for r in range(N):
        c = board[r]
        if c != -1:
            center = (start_x + c*cell_size + cell_size//2, start_y + r*cell_size + cell_size//2)
            pygame.draw.circle(win, BLUE, center, cell_size//3)
            pygame.draw.circle(win, BLACK, center, cell_size//3, 2)
    # Draw border around the chessboard
    border_rect = pygame.Rect(start_x, start_y, cell_size*N, cell_size*N)
    pygame.draw.rect(win, BLACK, border_rect, 5)

def show_message(win, font, msg, color=BLACK, y_offset=0, y_abs=None):
    text = font.render(msg, True, color)
    if y_abs is not None:
        win.blit(text, (10, y_abs))
    else:
        win.blit(text, (10, HEIGHT-40+y_offset))

# --- Main Visualizer ---
def run_nqueens_visualizer():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("N-Queens Visualizer")
    font = pygame.font.SysFont(None, FONT_SIZE)
    N = None
    input_value = ''
    error_msg = ''
    message = 'N: Set board size | S: Step | A: Auto-solve | R: Reset | Q: Quit'
    board = []
    gen = None
    highlight = set()
    running = True
    prompt_n = True
    auto_solving = False
    
    while running:
        win.fill(WHITE)
        if N:
            draw_board(win, N, board if board else [-1]*N, highlight)
        if prompt_n:
            show_message(win, font, f"Enter N (4-16): {input_value}", DARK_BLUE, y_abs=HEIGHT-80)
        else:
            show_message(win, font, message, DARK_BLUE, y_abs=HEIGHT-80)
        if error_msg:
            show_message(win, font, error_msg, ERROR_COLOR, y_abs=HEIGHT-50)
        
        pygame.display.update()

        # Auto-solve logic
        if auto_solving and gen:
            try:
                step = next(gen)
                if step[0] == 'place':
                    _, r, c, b = step
                    board = b
                    highlight = {(r, c)}
                elif step[0] == 'remove':
                    _, r, c, b = step
                    board = b
                    highlight = {(r, c)}
                elif step[0] == 'solution':
                    board = step[1]
                    highlight = set((i, board[i]) for i in range(N))
                    error_msg = 'Solution found! Press R to reset or N for new N.'
                    gen = None
                    auto_solving = False
            except StopIteration:
                error_msg = 'No more solutions.'
                gen = None
                auto_solving = False
            pygame.time.delay(50) # Animation speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                error_msg = ''
                if prompt_n:
                    if event.key == pygame.K_RETURN:
                        try:
                            n_val = int(input_value)
                            if n_val < 4 or n_val > 16:
                                error_msg = 'N must be between 4 and 16.'
                            else:
                                N = n_val
                                board = [-1]*N
                                gen = None
                                highlight = set()
                                prompt_n = False
                                input_value = ''
                        except Exception:
                            error_msg = 'Invalid N.'
                            input_value = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_value = input_value[:-1]
                    elif event.unicode.isdigit():
                        input_value += event.unicode
                else:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_r:
                        board = [-1]*N
                        gen = None
                        highlight = set()
                        auto_solving = False
                    elif event.key == pygame.K_n:
                        prompt_n = True
                        input_value = ''
                        board = []
                        gen = None
                        highlight = set()
                        auto_solving = False
                    elif event.key == pygame.K_a:
                        auto_solving = not auto_solving
                        if auto_solving and not gen:
                            board = [-1]*N
                            highlight = set()
                            gen = nqueens_solver(N)
                    elif event.key == pygame.K_s:
                        auto_solving = False # Manual step stops auto-solve
                        if not gen:
                            gen = nqueens_solver(N)
                        try:
                            step = next(gen)
                            if step[0] == 'place':
                                _, r, c, b = step
                                board = b
                                highlight = {(r, c)}
                            elif step[0] == 'remove':
                                _, r, c, b = step
                                board = b
                                highlight = {(r, c)}
                            elif step[0] == 'solution':
                                board = step[1]
                                highlight = set((i, board[i]) for i in range(N))
                                error_msg = 'Solution found! Press R to reset or N for new N.'
                                gen = None
                        except StopIteration:
                            error_msg = 'No more solutions.'
                            gen = None
    pygame.quit()

if __name__ == "__main__":
    run_nqueens_visualizer() 