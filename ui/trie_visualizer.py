"""
Pygame Trie Visualizer (Improved UI & Robustness, Consistent Layout)
"""
import pygame
from core.tree.trie import TrieNode, trie_insert, trie_search, trie_prefix_match

WIDTH, HEIGHT = 1200, 800
NODE_RADIUS = 25
VERTICAL_GAP = 80
FONT_SIZE = 20
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,200,0)
RED = (255,0,0)
GREY = (200,200,200)
ERROR_COLOR = (255, 80, 80)
RESULT_DISPLAY_HEIGHT = 40

# --- Helper Functions ---
def draw_trie(win, node, x, y, dx, font, highlight=None, label=''):
    color = GREEN if highlight and label in highlight else BLUE
    pygame.draw.circle(win, color, (x, y), NODE_RADIUS)
    pygame.draw.circle(win, BLACK, (x, y), NODE_RADIUS, 2)
    text = font.render(label, True, WHITE)
    win.blit(text, (x-text.get_width()//2, y-text.get_height()//2))
    n = len(node.children)
    if n:
        child_dx = max(dx // max(n,1), NODE_RADIUS*2)
        start_x = x - dx//2 + child_dx//2
        for i, (char, child) in enumerate(sorted(node.children.items())):
            child_x = min(max(start_x + i*child_dx, NODE_RADIUS), WIDTH-NODE_RADIUS)
            pygame.draw.line(win, BLACK, (x, y), (child_x, y+VERTICAL_GAP), 2)
            draw_trie(win, child, child_x, y+VERTICAL_GAP, dx//2, font, highlight, char)

def animate_trie_search(win, root, word, font, search_type='search', result_msg=None):
    node = root
    highlight = set()
    for char in word:
        highlight.add(char)
        win.fill(WHITE)
        if result_msg:
            show_message(win, font, result_msg, GREEN, y_abs=10)
        draw_trie(win, root, WIDTH//2, RESULT_DISPLAY_HEIGHT + 20, WIDTH//2, font, highlight)
        pygame.display.update()
        pygame.time.delay(500)
        if char not in node.children:
            return False
        node = node.children[char]
    return node.is_end if search_type == 'search' else True

def show_message(win, font, msg, color=BLACK, y_offset=0, y_abs=None):
    text = font.render(msg, True, color)
    if y_abs is not None:
        win.blit(text, (10, y_abs))
    else:
        win.blit(text, (10, HEIGHT-40+y_offset))

def run_trie_visualizer():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Trie Visualizer")
    font = pygame.font.SysFont(None, FONT_SIZE)
    root = TrieNode()
    input_value = ''
    result_msg = ''
    message = 'Type word, then I=Insert, S=Search, P=Prefix, R=Reset, Q=Quit, H:Help'
    error_msg = ''
    show_help = False
    running = True
    while running:
        win.fill(WHITE)
        if result_msg:
            show_message(win, font, result_msg, GREEN, y_abs=10)
        draw_trie(win, root, WIDTH//2, RESULT_DISPLAY_HEIGHT + 20, WIDTH//2, font)
        show_message(win, font, message, BLACK, 0)
        if error_msg:
            show_message(win, font, error_msg, ERROR_COLOR, -30)
        inp = font.render(f'Word: {input_value}', True, RED)
        win.blit(inp, (10, HEIGHT-70))
        
        # Draw help overlay if needed
        if show_help:
            help_surface = pygame.Surface((WIDTH, HEIGHT))
            help_surface.set_alpha(200)
            help_surface.fill((240, 240, 240))
            win.blit(help_surface, (0, 0))
            
            help_font = pygame.font.SysFont(None, 28)
            help_lines = [
                "TRIE VISUALIZER - HELP",
                "",
                "CONTROLS:",
                "• Type letters/numbers to input words",
                "• I: Insert the input word",
                "• S: Search for the input word",
                "• P: Find all words with the input prefix",
                "• D: Delete the input word",
                "• R: Reset the trie",
                "• Q: Quit the visualizer",
                "• H: Toggle this help overlay",
                "",
                "FEATURES:",
                "• Animated search visualization",
                "• Prefix matching with results",
                "• Real-time trie updates",
                "• Error handling and validation"
            ]
            
            for i, line in enumerate(help_lines):
                color = (50, 50, 150) if i == 0 else (30, 30, 80)
                text = help_font.render(line, True, color)
                win.blit(text, (50, 50 + i * 30))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                error_msg = ''
                try:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_h:
                        show_help = not show_help
                    elif event.key == pygame.K_r:
                        root = TrieNode()
                        input_value = ''
                        result_msg = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_value = input_value[:-1]
                    elif event.key == pygame.K_i:
                        if input_value:
                            try:
                                trie_insert(root, input_value)
                                result_msg = f"Inserted: {input_value}"
                            except Exception as e:
                                error_msg = f"Insert error: {e}"
                            input_value = ''
                        else:
                            error_msg = "Enter a word to insert."
                    elif event.key == pygame.K_s:
                        if input_value:
                            try:
                                found = animate_trie_search(win, root, input_value, font, 'search', f"Search: {input_value}")
                                result_msg = f"Search: {'Found' if found else 'Not found'}"
                            except Exception as e:
                                error_msg = f"Search error: {e}"
                            input_value = ''
                        else:
                            error_msg = "Enter a word to search."
                    elif event.key == pygame.K_p:
                        if input_value:
                            try:
                                found = animate_trie_search(win, root, input_value, font, 'prefix', f"Prefix: {input_value}")
                                matches = trie_prefix_match(root, input_value) if found else []
                                result_msg = f"Prefix: {matches if matches else 'No match'}"
                            except Exception as e:
                                error_msg = f"Prefix error: {e}"
                            input_value = ''
                        else:
                            error_msg = "Enter a prefix."
                    elif event.key == pygame.K_d:
                        if input_value:
                            found = trie_search(root, input_value)
                            if not found:
                                error_msg = f"Word '{input_value}' not found."
                            else:
                                trie_delete(root, input_value)
                                result_msg = f"Deleted: {input_value}"
                            input_value = ''
                        else:
                            error_msg = "Enter a word to delete."
                    elif event.unicode.isalnum():
                        input_value += event.unicode
                except Exception as e:
                    error_msg = f"Error: {e}"
    pygame.quit()

if __name__ == "__main__":
    run_trie_visualizer() 