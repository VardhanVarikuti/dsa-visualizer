"""
Pygame N-ary Tree Visualizer (Improved UI & Robustness, Dynamic Layout)
"""
import pygame
from core.tree.nary_tree import NaryTreeNode, nary_bfs, nary_dfs

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
TRAVERSAL_DISPLAY_HEIGHT = 60

# --- Dynamic Layout Helpers ---
def get_nary_width(root):
    if not root or not root.children:
        return 1
    return sum(get_nary_width(child) for child in root.children)

def assign_nary_positions(root, x, y, x_min, x_max, positions):
    if not root:
        return
    positions[root] = (x, y)
    n = len(root.children)
    if n == 0:
        return
    total_width = sum(get_nary_width(child) for child in root.children)
    cur_x = x_min
    for child in root.children:
        child_width = get_nary_width(child)
        child_span = (x_max - x_min) * child_width // total_width
        child_x = cur_x + child_span // 2
        assign_nary_positions(child, child_x, y + VERTICAL_GAP, cur_x, cur_x + child_span, positions)
        cur_x += child_span

# --- Drawing Function ---
def draw_nary_tree(win, root, font, highlight=None):
    if not root:
        return
    positions = {}
    assign_nary_positions(root, WIDTH // 2, TRAVERSAL_DISPLAY_HEIGHT + 20, NODE_RADIUS, WIDTH - NODE_RADIUS, positions)
    for node, (x, y) in positions.items():
        for child in node.children:
            x2, y2 = positions[child]
            pygame.draw.line(win, BLACK, (x, y), (x2, y2), 2)
    for node, (x, y) in positions.items():
        color = GREEN if highlight and node.value in highlight else BLUE
        pygame.draw.circle(win, color, (x, y), NODE_RADIUS)
        pygame.draw.circle(win, BLACK, (x, y), NODE_RADIUS, 2)
        text = font.render(str(node.value), True, WHITE)
        win.blit(text, (x-text.get_width()//2, y-text.get_height()//2))

def show_message(win, font, msg, color=BLACK, y_offset=0, y_abs=None):
    text = font.render(msg, True, color)
    if y_abs is not None:
        win.blit(text, (10, y_abs))
    else:
        win.blit(text, (10, HEIGHT-40+y_offset))

def show_traversals(win, font, traversals):
    y = HEIGHT - 90
    for name, order in traversals.items():
        msg = f"{name}: {order}"
        show_message(win, font, msg, GREEN, y_abs=y)
        y += 30

def animate_nary_traversal(win, root, order, font, label, traversals=None):
    highlight = set()
    for v in order:
        highlight.add(v)
        win.fill(WHITE)
        if traversals:
            show_traversals(win, font, traversals)
        else:
            show_message(win, font, f"{label}: {order}", GREEN, y_abs=10)
        draw_nary_tree(win, root, font, highlight)
        pygame.display.update()
        pygame.time.delay(500)
    pygame.time.delay(500)

def find_node_by_value(root, value):
    if not root:
        return None
    if root.value == value:
        return root
    for child in root.children:
        found = find_node_by_value(child, value)
        if found:
            return found
    return None

def delete_nary_node(root, value):
    if not root:
        return None, False
    if root.value == value:
        return None, True  # Deleting root
    from collections import deque
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for i, child in enumerate(node.children):
            if child.value == value:
                node.children.pop(i)
                return root, True
            queue.append(child)
    return root, False

def run_nary_tree_visualizer():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("N-ary Tree Visualizer")
    font = pygame.font.SysFont(None, FONT_SIZE)
    root = None
    input_value = ''
    parent_value = ''
    message = 'Type value, optionally parent value, then I=Insert, T=Traverse, R=Reset, Q=Quit, H:Help'
    error_msg = ''
    show_help = False
    running = True
    last_traversals = None
    while running:
        win.fill(WHITE)
        draw_nary_tree(win, root, font)
        if last_traversals:
            show_traversals(win, font, last_traversals)
        show_message(win, font, message, BLACK, 0)
        if error_msg:
            show_message(win, font, error_msg, ERROR_COLOR, -30)
        inp = font.render(f'Value: {input_value}  Parent: {parent_value}', True, RED)
        win.blit(inp, (10, HEIGHT-70))
        
        # Draw help overlay if needed
        if show_help:
            help_surface = pygame.Surface((WIDTH, HEIGHT))
            help_surface.set_alpha(200)
            help_surface.fill((240, 240, 240))
            win.blit(help_surface, (0, 0))
            
            help_font = pygame.font.SysFont(None, 28)
            help_lines = [
                "N-ARY TREE VISUALIZER - HELP",
                "",
                "CONTROLS:",
                "• Type numbers to input values",
                "• I: Insert the input value",
                "• T: Show BFS and DFS traversals",
                "• D: Delete the input value",
                "• R: Reset the tree",
                "• Q: Quit the visualizer",
                "• H: Toggle this help overlay",
                "• TAB: Switch between value and parent input",
                "",
                "FEATURES:",
                "• N-ary tree with unlimited children",
                "• Animated BFS and DFS traversal",
                "• Parent-child relationship building",
                "• Dynamic layout adaptation"
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
                        root = None
                        input_value = ''
                        parent_value = ''
                    elif event.key == pygame.K_BACKSPACE:
                        if parent_value:
                            parent_value = parent_value[:-1]
                        elif input_value:
                            input_value = input_value[:-1]
                    elif event.key == pygame.K_TAB:
                        if not parent_value:
                            parent_value = input_value
                            input_value = ''
                    elif event.key == pygame.K_i:
                        if input_value:
                            if not root:
                                root = NaryTreeNode(input_value)
                            else:
                                parent = root if not parent_value else find_node_by_value(root, parent_value)
                                if parent:
                                    parent.children.append(NaryTreeNode(input_value))
                                else:
                                    error_msg = f"Parent '{parent_value}' not found."
                            input_value = ''
                            parent_value = ''
                        else:
                            error_msg = "Enter a value to insert."
                    elif event.key == pygame.K_t:
                        if root:
                            bfs_order = nary_bfs(root)
                            dfs_order = nary_dfs(root)
                            last_traversals = {"BFS": bfs_order, "DFS": dfs_order}
                            show_traversals(win, font, last_traversals)
                            pygame.display.update()
                            pygame.time.delay(1000)
                            animate_nary_traversal(win, root, bfs_order, font, "BFS", last_traversals)
                            animate_nary_traversal(win, root, dfs_order, font, "DFS", last_traversals)
                        else:
                            error_msg = "Tree is empty."
                    elif event.key == pygame.K_d:
                        if input_value:
                            if not root:
                                error_msg = "Tree is empty."
                            else:
                                root, found = delete_nary_node(root, input_value)
                                if not found:
                                    error_msg = f"Node '{input_value}' not found."
                            input_value = ''
                        else:
                            error_msg = "Enter a value to delete."
                    elif event.unicode.isalnum():
                        input_value += event.unicode
                except Exception as e:
                    error_msg = f"Error: {e}"
    pygame.quit()

if __name__ == "__main__":
    run_nary_tree_visualizer() 