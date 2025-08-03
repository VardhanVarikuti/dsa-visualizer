"""
Pygame Generic Binary Tree Visualizer (Dynamic Layout, No Out-of-Bounds)
"""
import pygame
from core.tree.operations import TreeNode, tree_insert, tree_delete, tree_lca

WIDTH, HEIGHT = 1200, 800
NODE_RADIUS = 25
VERTICAL_GAP = 80
FONT_SIZE = 22
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,200,0)
RED = (255,0,0)
GREY = (200,200,200)
ERROR_COLOR = (255, 80, 80)

# --- Dynamic Layout Helpers ---
def get_subtree_widths(root):
    if not root:
        return 0
    left = get_subtree_widths(root.left)
    right = get_subtree_widths(root.right)
    # Minimum width for a node is 1
    return max(1, left) + max(1, right)

LCA_DISPLAY_HEIGHT = 40  # Reserve space at the top for LCA result

def assign_positions(root, x, y, x_min, x_max, positions, level=0):
    if not root:
        return
    positions[root] = (x, y)
    # Compute width for left and right subtrees
    left_count = get_subtree_widths(root.left)
    right_count = get_subtree_widths(root.right)
    total = max(1, left_count) + max(1, right_count)
    # Horizontal space for each subtree
    if root.left:
        left_x = x_min + (x - x_min) // 2
        assign_positions(root.left, left_x, y + VERTICAL_GAP, x_min, x, positions, level+1)
    if root.right:
        right_x = x + (x_max - x) // 2
        assign_positions(root.right, right_x, y + VERTICAL_GAP, x, x_max, positions, level+1)

# --- Drawing Function ---
def draw_generic_tree(win, root, font, highlight=None):
    if not root:
        return
    positions = {}
    assign_positions(root, WIDTH // 2, LCA_DISPLAY_HEIGHT + 20, NODE_RADIUS, WIDTH - NODE_RADIUS, positions)
    # Draw edges first
    for node, (x, y) in positions.items():
        if node.left:
            x2, y2 = positions[node.left]
            pygame.draw.line(win, BLACK, (x, y), (x2, y2), 2)
        if node.right:
            x2, y2 = positions[node.right]
            pygame.draw.line(win, BLACK, (x, y), (x2, y2), 2)
    # Draw nodes
    for node, (x, y) in positions.items():
        color = GREEN if highlight and node.value in highlight else BLUE
        pygame.draw.circle(win, color, (x, y), NODE_RADIUS)
        pygame.draw.circle(win, BLACK, (x, y), NODE_RADIUS, 2)
        text = font.render(str(node.value), True, WHITE)
        win.blit(text, (x-text.get_width()//2, y-text.get_height()//2))

# --- Other unchanged helpers ---
def find_path(root, value, path=None):
    if root is None:
        return None
    if path is None:
        path = []
    path.append(root)
    if root.value == value:
        return path[:]
    left = find_path(root.left, value, path)
    if left:
        return left
    right = find_path(root.right, value, path)
    if right:
        return right
    path.pop()
    return None

def animate_lca(win, root, v1, v2, lca_value, font):
    path1 = find_path(root, v1)
    path2 = find_path(root, v2)
    highlight = set()
    if path1:
        for node in path1:
            highlight.add(node.value)
            win.fill(WHITE)
            draw_generic_tree(win, root, font, highlight)
            pygame.display.update()
            pygame.time.delay(300)
    if path2:
        for node in path2:
            highlight.add(node.value)
            win.fill(WHITE)
            draw_generic_tree(win, root, font, highlight)
            pygame.display.update()
            pygame.time.delay(300)
    if lca_value is not None:
        highlight.add(lca_value)
        win.fill(WHITE)
        draw_generic_tree(win, root, font, highlight)
        pygame.display.update()
        pygame.time.delay(800)

def show_message(win, font, msg, color=BLACK, y_offset=0, y_abs=None):
    text = font.render(msg, True, color)
    if y_abs is not None:
        win.blit(text, (10, y_abs))
    else:
        win.blit(text, (10, HEIGHT-40+y_offset))

# --- Main Visualizer (unchanged except draw_generic_tree call) ---
def run_generic_tree_visualizer():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Generic Binary Tree Visualizer")
    font = pygame.font.SysFont(None, FONT_SIZE)
    root = None
    input_value = ''
    parent_value = ''
    side = 'left'
    lca_input = ''
    lca_value1 = ''
    lca_value2 = ''
    lca_collecting_second = False
    message = 'I:Insert  D:Delete  L:LCA  R:Reset  Q:Quit  H:Help  (Insert: value, parent, side [L/R], ENTER)'
    error_msg = ''
    lca_result = ''
    show_help = False
    running = True
    lca_mode = False
    insert_mode = False
    insert_stage = 0  # 0: value, 1: parent, 2: side
    while running:
        win.fill(WHITE)
        if lca_result:
            show_message(win, font, lca_result, GREEN, y_abs=10)
        draw_generic_tree(win, root, font)
        show_message(win, font, message, BLACK, 0)
        if error_msg:
            show_message(win, font, error_msg, ERROR_COLOR, -30)
        if lca_mode:
            prompt = 'LCA: '
            if lca_value1:
                prompt += lca_value1
            if lca_collecting_second:
                prompt += ', '
                if lca_value2:
                    prompt += lca_value2
                elif lca_input:
                    prompt += lca_input
            elif lca_input:
                prompt += lca_input
            inp = font.render(prompt, True, RED)
            win.blit(inp, (10, HEIGHT-70))
        elif insert_mode:
            prompt = ['Value', 'Parent (blank=root/auto)', 'Side (L/R)']
            vals = [input_value, parent_value, side.upper()]
            inp = font.render(f'Insert: {prompt[insert_stage]}: {vals[insert_stage]}', True, RED)
            win.blit(inp, (10, HEIGHT-70))
            inp2 = font.render(f'Current: Value={input_value}  Parent={parent_value}  Side={side.upper()}', True, GREY)
            win.blit(inp2, (10, HEIGHT-100))
        else:
            inp = font.render(f'Value: {input_value}', True, RED)
            win.blit(inp, (10, HEIGHT-70))
        
        # Draw help overlay if needed
        if show_help:
            help_surface = pygame.Surface((WIDTH, HEIGHT))
            help_surface.set_alpha(200)
            help_surface.fill((240, 240, 240))
            win.blit(help_surface, (0, 0))
            
            help_font = pygame.font.SysFont(None, 28)
            help_lines = [
                "GENERIC BINARY TREE VISUALIZER - HELP",
                "",
                "CONTROLS:",
                "• Type numbers to input values",
                "• I: Enter insert mode",
                "• D: Delete the input value",
                "• L: Enter LCA (Lowest Common Ancestor) mode",
                "• R: Reset the tree",
                "• Q: Quit the visualizer",
                "• H: Toggle this help overlay",
                "",
                "INSERT MODE:",
                "• TAB: Switch between value, parent, side",
                "• ENTER: Complete insertion",
                "• L/R: Set left or right side",
                "",
                "LCA MODE:",
                "• Type two values separated by comma/space",
                "• ENTER: Calculate LCA",
                "",
                "FEATURES:",
                "• Generic binary tree operations",
                "• Animated LCA path visualization",
                "• Flexible parent-child relationships",
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
                        side = 'left'
                        lca_input = ''
                        lca_value1 = ''
                        lca_value2 = ''
                        lca_collecting_second = False
                        lca_mode = False
                        insert_mode = False
                        insert_stage = 0
                        lca_result = ''
                    elif event.key == pygame.K_BACKSPACE:
                        if lca_mode:
                            if lca_collecting_second:
                                if lca_input:
                                    lca_input = lca_input[:-1]
                                elif lca_value2:
                                    lca_value2 = lca_value2[:-1]
                                else:
                                    lca_collecting_second = False
                            elif lca_input:
                                lca_input = lca_input[:-1]
                            elif lca_value1:
                                lca_value1 = lca_value1[:-1]
                        elif insert_mode:
                            if insert_stage == 0 and input_value:
                                input_value = input_value[:-1]
                            elif insert_stage == 1 and parent_value:
                                parent_value = parent_value[:-1]
                            elif insert_stage == 2 and side:
                                side = side[:-1]
                        else:
                            input_value = input_value[:-1]
                    elif event.key == pygame.K_i and not insert_mode:
                        insert_mode = True
                        insert_stage = 0
                        input_value = ''
                        parent_value = ''
                        side = 'left'
                    elif insert_mode:
                        if event.key == pygame.K_TAB:
                            insert_stage = (insert_stage + 1) % 3
                        elif event.key == pygame.K_RETURN:
                            if input_value:
                                try:
                                    val = int(input_value)
                                    pval = parent_value if parent_value else None
                                    s = 'left' if side.lower().startswith('l') else 'right'
                                    root = tree_insert(root, val, pval, s)
                                except Exception as e:
                                    error_msg = f"Insert error: {e}"
                                input_value = ''
                                parent_value = ''
                                side = 'left'
                                insert_mode = False
                                insert_stage = 0
                            else:
                                error_msg = "Enter a value to insert."
                        elif insert_stage == 0 and event.unicode.isdigit():
                            input_value += event.unicode
                        elif insert_stage == 1 and (event.unicode.isalnum() or event.unicode == ' '):
                            parent_value += event.unicode
                        elif insert_stage == 2 and event.key in (pygame.K_l, pygame.K_r):
                            side = 'left' if event.key == pygame.K_l else 'right'
                    elif event.key == pygame.K_d and not insert_mode:
                        if input_value:
                            try:
                                val = int(input_value)
                                root = tree_delete(root, val)
                            except Exception as e:
                                error_msg = f"Delete error: {e}"
                            input_value = ''
                        else:
                            error_msg = "Enter a value to delete."
                    elif event.key == pygame.K_l and not insert_mode:
                        lca_mode = True
                        lca_input = ''
                        lca_value1 = ''
                        lca_value2 = ''
                        lca_collecting_second = False
                    elif event.key == pygame.K_RETURN and lca_mode:
                        if lca_value1 and lca_value2:
                            try:
                                v1, v2 = int(lca_value1), int(lca_value2)
                                lca = tree_lca(root, v1, v2)
                                if lca is not None:
                                    lca_result = f'LCA({lca_value1},{lca_value2}) = {lca}'
                                    animate_lca(win, root, v1, v2, lca, font)
                                else:
                                    lca_result = ''
                                    error_msg = f"LCA not found."
                            except Exception as e:
                                lca_result = ''
                                error_msg = f"LCA error: {e}"
                            lca_mode = False
                            lca_input = ''
                            lca_collecting_second = False
                        else:
                            error_msg = "Enter two values for LCA."
                    elif lca_mode:
                        # Accept input for lca_value1 until separator, then lca_value2
                        if not lca_collecting_second:
                            if event.unicode.isdigit():
                                lca_input += event.unicode
                            elif event.key in (pygame.K_COMMA, pygame.K_SPACE, pygame.K_SEMICOLON) and lca_input:
                                lca_value1 = lca_input
                                lca_input = ''
                                lca_collecting_second = True
                        else:
                            if event.unicode.isdigit():
                                lca_input += event.unicode
                            elif event.key in (pygame.K_COMMA, pygame.K_SPACE, pygame.K_SEMICOLON) and lca_input:
                                lca_value2 = lca_input
                                lca_input = ''
                    elif not insert_mode and not lca_mode and event.unicode.isdigit():
                        input_value += event.unicode
                except Exception as e:
                    error_msg = f"Error: {e}"
    pygame.quit()

if __name__ == "__main__":
    run_generic_tree_visualizer() 