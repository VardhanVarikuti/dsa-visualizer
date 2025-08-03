"""
Pygame Tree Visualizer for BST/AVL (Improved UI & Robustness)
"""
import pygame
from core.tree.bst import BSTNode, bst_insert, bst_delete, bst_traversals
from core.tree.avl import AVLNode, avl_insert, avl_delete

WIDTH, HEIGHT = 1200, 800  # Increased size
NODE_RADIUS = 25  
VERTICAL_GAP = 75  
LCA_DISPLAY_HEIGHT = 40  
FONT_SIZE = 22  
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,200,0)
RED = (255,0,0)
GREY = (200,200,200)
ERROR_COLOR = (255, 80, 80)

# --- Helper Functions ---
def draw_tree(win, root, font, highlight=None):
    if not root:
        return
    positions = {}
    assign_positions(root, WIDTH // 2, LCA_DISPLAY_HEIGHT + 20, NODE_RADIUS, WIDTH - NODE_RADIUS, positions)
    for node, (x, y) in positions.items():
        if node.left:
            x2, y2 = positions[node.left]
            pygame.draw.line(win, BLACK, (x, y), (x2, y2), 2)  # Thicker lines
        if node.right:
            x2, y2 = positions[node.right]
            pygame.draw.line(win, BLACK, (x, y), (x2, y2), 2)
    for node, (x, y) in positions.items():
        color = GREEN if highlight and node.value in highlight else BLUE
        pygame.draw.circle(win, color, (x, y), NODE_RADIUS)
        pygame.draw.circle(win, BLACK, (x, y), NODE_RADIUS, 2)
        # Use anti-aliased text
        text = font.render(str(node.value), True, WHITE)
        win.blit(text, (x-text.get_width()//2, y-text.get_height()//2))

def get_all_node_values(root):
    if not root:
        return set()
    return {root.value} | get_all_node_values(root.left) | get_all_node_values(root.right)

def show_traversals(win, font, traversals):
    y = HEIGHT - 120  # Start 3 lines above the bottom
    for name in ["Inorder", "Preorder", "Postorder"]:
        order = traversals.get(name.lower(), [])
        msg = f"{name}: {order}"
        show_message(win, font, msg, GREEN, y_abs=y)
        y += 30

def animate_traversal(win, root, order, font, label, traversals=None):
    highlight = set()
    valid_values = get_all_node_values(root)
    for v in order:
        if v in valid_values:
            highlight.add(v)
        win.fill(WHITE)
        if traversals:
            show_traversals(win, font, traversals)
        else:
            show_message(win, font, f"{label}: {order}", GREEN, y_abs=10)
        draw_tree(win, root, font, highlight)
        pygame.display.update()
        pygame.time.delay(500)
    pygame.time.delay(500)

def show_message(win, font, msg, color=BLACK, y_offset=0, y_abs=None):
    text = font.render(msg, True, color)
    if y_abs is not None:
        win.blit(text, (10, y_abs))
    else:
        win.blit(text, (10, HEIGHT-40+y_offset))

def value_in_tree(root, value):
    if not root:
        return False
    if root.value == value:
        return True
    return value_in_tree(root.left, value) or value_in_tree(root.right, value)

# --- Dynamic Layout Helpers ---
def get_subtree_widths(root):
    if not root:
        return 0
    left = get_subtree_widths(root.left)
    right = get_subtree_widths(root.right)
    return max(1, left) + max(1, right)

def assign_positions(root, x, y, x_min, x_max, positions, level=0):
    if not root:
        return
    positions[root] = (x, y)
    left_count = get_subtree_widths(root.left)
    right_count = get_subtree_widths(root.right)
    if root.left:
        left_x = x_min + (x - x_min) // 2
        assign_positions(root.left, left_x, y + VERTICAL_GAP, x_min, x, positions, level+1)
    if root.right:
        right_x = x + (x_max - x) // 2
        assign_positions(root.right, right_x, y + VERTICAL_GAP, x, x_max, positions, level+1)

def run_tree_visualizer(mode='BST'):
    """
    mode: 'BST' or 'AVL'
    To launch from CLI, import and call run_tree_visualizer('BST') or run_tree_visualizer('AVL')
    """
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Tree Visualizer ({mode})")
    font = pygame.font.SysFont(None, FONT_SIZE)
    root = None
    input_value = ''
    message = f'Type number and press I=Insert, D=Delete, T=Traverse, R=Reset, Q=Quit ({mode})'
    error_msg = ''
    running = True
    while running:
        win.fill(WHITE)
        draw_tree(win, root, font)
        show_message(win, font, message, BLACK, 0)
        if error_msg:
            show_message(win, font, error_msg, ERROR_COLOR, -30)
        inp = font.render('Input: ' + input_value, True, RED)
        win.blit(inp, (10, HEIGHT-70))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                error_msg = ''
                try:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_r:
                        root = None
                        input_value = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_value = input_value[:-1]
                    elif event.key == pygame.K_i:
                        if input_value:
                            try:
                                val = int(input_value)
                                if mode == 'BST':
                                    root = bst_insert(root, val)
                                elif mode == 'AVL':
                                    root = avl_insert(root, val)
                            except Exception as e:
                                error_msg = f"Insert error: {e}"
                            input_value = ''
                        else:
                            error_msg = "Enter a value to insert."
                    elif event.key == pygame.K_d:
                        if input_value:
                            try:
                                val = int(input_value)
                                if not value_in_tree(root, val):
                                    error_msg = f"Value {val} not found."
                                else:
                                    if mode == 'BST':
                                        root = bst_delete(root, val)
                                    elif mode == 'AVL':
                                        root = avl_delete(root, val)
                            except Exception as e:
                                error_msg = f"Delete error: {e}"
                            input_value = ''
                        else:
                            error_msg = "Enter a value to delete."
                    elif event.key == pygame.K_t:
                        if root:
                            traversals = bst_traversals(root)
                            show_traversals(win, font, traversals)
                            pygame.display.update()
                            pygame.time.delay(1000)
                            for name in ["inorder", "preorder", "postorder"]:
                                order = traversals.get(name, [])
                                animate_traversal(win, root, order, font, name.capitalize(), traversals)
                        else:
                            error_msg = "Tree is empty."
                    elif event.unicode.isdigit():
                        input_value += event.unicode
                except Exception as e:
                    error_msg = f"Error: {e}"
    pygame.quit()

if __name__ == "__main__":
    run_tree_visualizer('BST') 