import pygame
import ui.constants as _c

def set_window_icon():
    """Sets the window icon for the current Pygame display."""
    try:
        icon = pygame.image.load(_c.ICON_PATH)
        pygame.display.set_icon(icon)
    except Exception:
        # Fallback if icon is missing
        pass

def draw_wrapped_messages(win, font, messages, max_width, start_y, line_height=22):
    """
    Draws a list of (text, color) tuples with text wrapping.
    Draws from bottom up starting at start_y.
    """
    y = start_y
    for msg, color in reversed(messages):
        # Handle manual newlines first
        raw_lines = msg.split('\n')
        for raw_line in reversed(raw_lines):
            words = raw_line.split(' ')
            lines = []
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                w, _ = font.size(test_line)
                if w <= max_width:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            lines.append(' '.join(current_line))
            
            for line in reversed(lines):
                surf = font.render(line, True, color)
                rect = surf.get_rect(center=(win.get_width() // 2, y))
                win.blit(surf, rect)
                y -= line_height
    return y
