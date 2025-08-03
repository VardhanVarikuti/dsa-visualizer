import pygame
import sys
import string
import math
from core.graph.graph import Graph
from .constants import *
from core.graph.algorithms.dijkstra import dijkstra
from core.graph.algorithms.bellman_ford import bellman_ford
from core.graph.algorithms.floyd_warshall import floyd_warshall
from core.graph.algorithms.mst import prim, kruskal
from core.graph.algorithms.astar import astar
from core.graph.algorithms.johnson import johnson
from core.graph.algorithms.spfa import spfa
from core.graph.algorithms.topo_sort_relax import topo_sort_relax

ALGO_LIST = [
    ("Dijkstra", "Dijkstra's Shortest Path"),
    ("Bellman-Ford", "Bellman-Ford Shortest Path"),
    ("Floyd-Warshall", "All-Pairs Shortest Path"),
    ("Prim", "Prim's MST (Undirected)"),
    ("Kruskal", "Kruskal's MST (Undirected)"),
    ("A*", "A* Search"),
    ("Johnson", "Johnson's All-Pairs Shortest Path"),
    ("SPFA", "Shortest Path Faster Algorithm"),
    ("TopoSort+Relax", "DAG Shortest Path")
]

MODE_EDIT = 'Edit Graph'
MODE_SET_START = 'Set Start Node'
MODE_SET_TARGET = 'Set Target Node'

class VisualNode:
    def __init__(self, label, pos):
        self.label = label
        self.pos = pos
        self.selected = False

class VisualEdge:
    def __init__(self, u, v, weight=1):
        self.u = u
        self.v = v
        self.weight = weight
        self.selected = False

class Button:
    def __init__(self, rect, text, action):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.active = False
    def draw(self, win, font):
        color = BUTTON_ACTIVE if self.active else BUTTON_COLOR
        pygame.draw.rect(win, color, self.rect, border_radius=8)
        pygame.draw.rect(win, (100,100,100), self.rect, 2, border_radius=8)
        btn_font = pygame.font.SysFont(None, BUTTON_FONT_SIZE)
        surf = btn_font.render(self.text, True, BUTTON_TEXT)
        rect = surf.get_rect(center=self.rect.center)
        win.blit(surf, rect)
    def is_hover(self, pos):
        return self.rect.collidepoint(pos)

class WeightedGraphVisualizer:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Weighted Graph Visualizer")
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.nodes = []
        self.edges = []
        self.graph = Graph(directed=False)
        self.node_labels = iter(string.ascii_uppercase)
        self.selected_node = None
        self.start_node = None
        self.dragging = False
        self.drag_start = None
        self.selected_edge = None
        self.message = "Click to add node | Drag to add edge | Del: delete | R: Reset | Q: Quit | H: Help"
        self.error_msg = ''
        self.result_msg = ''
        self.buttons = []
        self.example_buttons = []
        self.run_button = None
        self.mode_buttons = []
        self.directed = False
        self.current_mode = MODE_EDIT
        self.active_algo = None
        self.animating = False
        self.animation_steps = []
        self.animation_index = 0
        self.animation_delay = 600  # ms
        self.show_help = False
        self.target_node = None # Added for A*
        self.setup_buttons()

    def setup_buttons(self):
        w, h = 150, 36
        gap = 30
        # Arrange buttons in two rows
        n_per_row = (len(ALGO_LIST) + 1) // 2
        total_width = n_per_row * w + (n_per_row-1) * gap
        x = (WIDTH - total_width) // 2
        y1 = 16
        y2 = y1 + h + 10
        self.buttons = []
        for i, (algo, desc) in enumerate(ALGO_LIST):
            row = i // n_per_row
            col = i % n_per_row
            btn_x = x + col * (w + gap)
            btn_y = y1 if row == 0 else y2
            btn = Button((btn_x, btn_y, w, h), algo, lambda a=algo: self.select_algo(a))
            self.buttons.append(btn)
        # Mode buttons (top left)
        mb_w, mb_h = 140, 32
        mb_x, mb_y = 30, y2 + h + 20
        self.mode_buttons = [
            Button((mb_x, mb_y, mb_w, mb_h), "Edit Graph", lambda: self.set_mode(MODE_EDIT)),
        ]
        
        # Add Set Start Node button only for algorithms that require it
        start_node_algorithms = ["Dijkstra", "Bellman-Ford", "A*", "SPFA", "TopoSort+Relax"]
        if self.active_algo in start_node_algorithms:
            self.mode_buttons.append(Button((mb_x + mb_w + 16, mb_y, mb_w, mb_h), "Set Start Node", lambda: self.set_mode(MODE_SET_START)))
        
        # Add Set Target Node button only for A*
        if self.active_algo == "A*":
            self.mode_buttons.append(Button((mb_x, mb_y + 2*mb_h + 16, mb_w, mb_h), "Set Target Node", lambda: self.set_mode(MODE_SET_TARGET)))
        
        self.mode_buttons.append(Button((mb_x, mb_y + mb_h + 16, mb_w, mb_h), "Toggle Directed", self.toggle_directed))
        btn_w, btn_h = 150, 36
        btn_x = WIDTH - btn_w - 30
        btn_y1 = y2 + h + 20
        btn_y2 = btn_y1 + btn_h + 12
        self.example_buttons = [
            Button((btn_x, btn_y1, btn_w, btn_h), "Load Example", self.load_example_graph)
        ]
        self.run_button = Button((btn_x, btn_y2, btn_w, btn_h), "Run", self.run_selected_algorithm)

    def toggle_directed(self):
        self.directed = not self.directed
        self.graph = Graph(directed=self.directed)
        self.message = f"Mode: {'Directed' if self.directed else 'Undirected'} graph."
        # Optionally, clear edges or reload graph

    def draw(self):
        win_width, win_height = self.win.get_size()
        self.win.fill(BG_COLOR)
        # Draw edges (with weights)
        mouse_pos = pygame.mouse.get_pos()
        self.weight_label_rects = []  # For click-to-edit
        for edge in self.edges:
            color = EDGE_SELECTED_COLOR if edge.selected else EDGE_COLOR
            u, v = edge.u, edge.v
            # Draw arrow if directed, else line
            if self.directed:
                self._draw_arrow(u.pos, v.pos, color)
            else:
                pygame.draw.line(self.win, color, u.pos, v.pos, 3)
            # --- Offset weights for bidirectional edges ---
            mx, my = (u.pos[0] + v.pos[0]) // 2, (u.pos[1] + v.pos[1]) // 2
            offset_x, offset_y = 0, 0
            # Check for reverse edge
            has_reverse = any(e.u == v and e.v == u for e in self.edges)
            if has_reverse:
                # Compute perpendicular offset
                dx, dy = v.pos[0] - u.pos[0], v.pos[1] - u.pos[1]
                length = math.hypot(dx, dy)
                if length == 0:
                    length = 1
                perp_x = -dy / length
                perp_y = dx / length
                # Offset one direction for (u,v), other for (v,u)
                offset_amt = 22
                if (u.label < v.label) or (not self.directed and id(u) < id(v)):
                    offset_x = perp_x * offset_amt
                    offset_y = perp_y * offset_amt
                else:
                    offset_x = -perp_x * offset_amt
                    offset_y = -perp_y * offset_amt
            wsurf = self.font.render(str(edge.weight), True, (80,0,0))
            weight_rect = wsurf.get_rect(center=(mx + offset_x, my + offset_y))
            self.win.blit(wsurf, weight_rect)
            self.weight_label_rects.append((weight_rect, edge))
        # Draw nodes
        for node in self.nodes:
            if node.selected:
                color = NODE_SELECTED_COLOR
            elif self.active_algo == "A*" and self.target_node and node == self.target_node:
                color = (255, 80, 80)  # Red for target
            else:
                color = NODE_COLOR
            pygame.draw.circle(self.win, color, node.pos, NODE_RADIUS)
            pygame.draw.circle(self.win, (0,0,0), node.pos, NODE_RADIUS, 2)
            label_surf = self.font.render(node.label, True, TEXT_COLOR)
            rect = label_surf.get_rect(center=node.pos)
            self.win.blit(label_surf, rect)
        # Draw dragging edge
        if self.dragging and self.drag_start:
            if self.directed:
                self._draw_arrow(self.drag_start.pos, pygame.mouse.get_pos(), (120,120,120))
            else:
                pygame.draw.line(self.win, (120,120,120), self.drag_start.pos, pygame.mouse.get_pos(), 2)
        # Draw buttons
        for btn in self.buttons:
            btn.draw(self.win, self.font)
        for btn in self.mode_buttons:
            btn.draw(self.win, self.font)
        if self.active_algo:
            for btn in self.example_buttons:
                btn.draw(self.win, self.font)
            self.run_button.draw(self.win, self.font)
        # Draw current mode
        mode_surf = self.font.render(f"Mode: {self.current_mode} | {'Directed' if self.directed else 'Undirected'}", True, (80, 80, 80))
        self.win.blit(mode_surf, (30, win_height-40))
        # Draw messages
        self.show_message(self.message, INSTR_COLOR, y_abs=win_height-60)
        if self.error_msg:
            self.show_message(self.error_msg, ERROR_COLOR, y_abs=win_height-30)
        if self.result_msg:
            self.show_message(self.result_msg, (0, 120, 0), y_abs=win_height-90)
        if self.animating:
            self.show_message(f"Animation speed: {self.animation_delay} ms (+/-)", (80, 80, 80), y_abs=win_height-120)
        if self.show_help:
            overlay = pygame.Surface((win_width, win_height), pygame.SRCALPHA)
            overlay.fill((240, 240, 255, 230))
            self.win.blit(overlay, (0, 0))
            help_lines = [
                "CONTROLS:",
                "Left Click: Add node / Select node / Drag to add edge",
                "Right Click: Select edge",
                "Del/Backspace: Delete selected node/edge",
                "R: Reset graph",
                "Q: Quit",
                "E: Edit mode",
                "S: Set start node (for SSSP)",
                "+/-: Adjust animation speed",
                "H: Toggle this help overlay",
                "",
                "ALGORITHMS:",
                "Dijkstra: Shortest path (non-negative weights)",
                "Bellman-Ford: Shortest path (negative weights)",
                "Floyd-Warshall: All-pairs shortest path",
                "Prim/Kruskal: MST (undirected)",
                "A*: Heuristic shortest path",
                "Johnson: All-pairs shortest path (sparse)",
                "SPFA: Optimized Bellman-Ford",
                "TopoSort+Relax: DAG shortest path",
                "",
                "Use 'Load Example' for a demo graph for each algorithm!"
            ]
            font = pygame.font.SysFont(None, 28)
            for i, line in enumerate(help_lines):
                surf = font.render(line, True, (30, 30, 80))
                rect = surf.get_rect(center=(win_width//2, 80 + i*32))
                self.win.blit(surf, rect)
            pygame.display.update()
            return
        pygame.display.update()

    def _draw_arrow(self, start, end, color):
        x1, y1 = start
        x2, y2 = end
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        ux, uy = dx / dist, dy / dist
        sx, sy = x1 + ux * NODE_RADIUS, y1 + uy * NODE_RADIUS
        ex, ey = x2 - ux * NODE_RADIUS, y2 - uy * NODE_RADIUS
        pygame.draw.line(self.win, color, (sx, sy), (ex, ey), 3)
        angle = math.atan2(ey - sy, ex - sx)
        length = 16
        width = 8
        left = (ex - length * math.cos(angle - math.pi/8), ey - length * math.sin(angle - math.pi/8))
        right = (ex - length * math.cos(angle + math.pi/8), ey - length * math.sin(angle + math.pi/8))
        pygame.draw.polygon(self.win, color, [(ex, ey), left, right])

    def show_message(self, msg, color, y_abs):
        win_width, _ = self.win.get_size()
        surf = self.font.render(msg, True, color)
        rect = surf.get_rect(center=(win_width//2, y_abs))
        self.win.blit(surf, rect)

    def get_node_at_pos(self, pos):
        for node in self.nodes:
            if (node.pos[0] - pos[0]) ** 2 + (node.pos[1] - pos[1]) ** 2 <= NODE_RADIUS ** 2:
                return node
        return None

    def get_edge_at_pos(self, pos):
        for edge in self.edges:
            ux, uy = edge.u.pos
            vx, vy = edge.v.pos
            mx, my = (ux + vx) / 2, (uy + vy) / 2
            if (mx - pos[0]) ** 2 + (my - pos[1]) ** 2 <= (NODE_RADIUS // 2) ** 2:
                return edge
        return None

    def add_node(self, pos):
        for node in self.nodes:
            if (node.pos[0] - pos[0]) ** 2 + (node.pos[1] - pos[1]) ** 2 < (2 * NODE_RADIUS) ** 2:
                self.error_msg = "Too close to another node. Move further away."
                return None
        try:
            label = next(self.node_labels)
        except StopIteration:
            self.error_msg = "No more node labels available."
            return None
        node = VisualNode(label, pos)
        self.nodes.append(node)
        self.graph.adj[label] = []
        return node

    def add_edge(self, u, v, weight=1):
        # u and v can be VisualNode or label; always use label for graph
        u_label = u.label if hasattr(u, 'label') else u
        v_label = v.label if hasattr(v, 'label') else v
        if u_label == v_label:
            self.error_msg = "No self-loops allowed."
            return
        for edge in self.edges:
            if (edge.u.label == u_label and edge.v.label == v_label) or (not self.directed and edge.u.label == v_label and edge.v.label == u_label):
                self.error_msg = "Edge already exists."
                return
        # Find VisualNode objects for u and v
        u_node = next((n for n in self.nodes if n.label == u_label), None)
        v_node = next((n for n in self.nodes if n.label == v_label), None)
        if not u_node or not v_node:
            self.error_msg = "Invalid node(s) for edge."
            return
        self.edges.append(VisualEdge(u_node, v_node, weight))
        self.graph.add_edge(u_label, v_label, weight)
        if not self.directed:
            self.graph.add_edge(v_label, u_label, weight)

    def delete_selected(self):
        if self.selected_node:
            self.edges = [e for e in self.edges if e.u != self.selected_node and e.v != self.selected_node]
            if self.selected_node.label in self.graph.adj:
                del self.graph.adj[self.selected_node.label]
            for adj in self.graph.adj.values():
                adj[:] = [pair for pair in adj if pair[0] != self.selected_node.label]
            self.nodes.remove(self.selected_node)
            self.selected_node = None
        elif self.selected_edge:
            self.edges.remove(self.selected_edge)
            u, v = self.selected_edge.u.label, self.selected_edge.v.label
            self.graph.adj[u] = [pair for pair in self.graph.adj[u] if pair[0] != v]
            if not self.directed:
                self.graph.adj[v] = [pair for pair in self.graph.adj[v] if pair[0] != u]
            self.selected_edge = None

    def reset(self):
        self.nodes = []
        self.edges = []
        self.graph = Graph(directed=self.directed)
        self.node_labels = iter(string.ascii_uppercase)
        self.selected_node = None
        self.selected_edge = None
        self.dragging = False
        self.drag_start = None
        self.message = "Click to add node | Drag to add edge | Del: delete | R: Reset | Q: Quit | H: Help"
        self.error_msg = ''
        self.result_msg = ''
        self.start_node = None
        self.target_node = None # Reset target node
        self.animating = False
        self.animation_steps = []
        self.animation_index = 0
        self.set_mode(MODE_EDIT)

    def set_mode(self, mode):
        self.current_mode = mode
        if mode == MODE_EDIT:
            self.message = "Click to add node | Drag to add edge | Del: delete | R: Reset | Q: Quit | H: Help"
        elif mode == MODE_SET_START:
            self.message = "Set Start Node: Click a node to select as start for SSSP."
        elif mode == MODE_SET_TARGET:
            self.message = "Set Target Node: Click a node to select as target for A*."

    def select_algo(self, algo):
        self.active_algo = algo
        self.result_msg = ''
        self.error_msg = f"Selected: {algo}. Click 'Load Example' for a demo, or build your own graph."
        self.start_node = None
        self.target_node = None # Reset target node
        self.animating = False
        self.animation_steps = []
        self.animation_index = 0
        # Force directed mode for A* but don't recreate graph
        if algo == "A*":
            self.directed = True
            # Only recreate graph if it's not already directed
            if not hasattr(self, 'graph') or not self.graph.directed:
                self.graph = Graph(directed=True)
            self.message = "A* requires a directed graph. Directed mode enabled."
        self.set_mode(MODE_EDIT)
        self.setup_buttons()  # Ensure buttons are updated for the selected algorithm

    def prompt_weight(self, initial_value=''):
        # Pygame-based input box for edge weight (now allows negative weights)
        weight = str(initial_value) if initial_value else ''
        prompt = "Enter edge weight (-999 to 999): "
        input_active = True
        clock = pygame.time.Clock()
        while input_active:
            self.draw()
            win_width, win_height = self.win.get_size()
            font = pygame.font.SysFont(None, 24)
            box_rect = pygame.Rect(win_width//2 - 120, win_height//2 - 44, 240, 88)
            pygame.draw.rect(self.win, (240,240,255), box_rect, border_radius=10)
            pygame.draw.rect(self.win, (80,80,120), box_rect, 2, border_radius=10)
            prompt_surf = font.render(prompt, True, (30,30,80))
            input_surf = font.render(weight, True, (30,30,80))
            prompt_rect = prompt_surf.get_rect(center=(box_rect.centerx, box_rect.y + 28))
            input_rect = input_surf.get_rect(center=(box_rect.centerx, box_rect.y + 60))
            self.win.blit(prompt_surf, prompt_rect)
            self.win.blit(input_surf, input_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            val = int(weight)
                            if -999 <= val <= 999 and val != 0:
                                return val
                        except Exception:
                            pass
                        self.error_msg = "Invalid weight. Using 1."
                        return 1
                    elif event.key == pygame.K_BACKSPACE:
                        weight = weight[:-1]
                    elif event.unicode.isdigit() and len(weight.lstrip('-')) < 3:
                        weight += event.unicode
                    elif event.unicode == '-' and len(weight) == 0:
                        weight = '-'
                    elif event.key == pygame.K_ESCAPE:
                        return 1
            clock.tick(30)
        return 1

    def _add_node_at(self, pos):
        node = self.add_node(pos)
        return node

    def _add_edge_by_label(self, l1, l2, weight=1):
        u = next((n for n in self.nodes if n.label == l1), None)
        v = next((n for n in self.nodes if n.label == l2), None)
        if u and v:
            self.add_edge(u, v, weight)

    def load_example_graph(self):
        # Set directed/undirected mode as appropriate for each algorithm BEFORE reset
        if self.active_algo in ("Prim", "Kruskal"):
            self.directed = False
            self.graph = Graph(directed=False)
        elif self.active_algo in ("Dijkstra", "Bellman-Ford", "Floyd-Warshall", "A*", "Johnson", "SPFA", "TopoSort+Relax"):
            self.directed = True if self.active_algo not in ("Prim", "Kruskal") else False
            self.graph = Graph(directed=self.directed)
        self.reset()  # This clears nodes/edges and sets up the graph
        self.node_labels = iter(string.ascii_uppercase)
        self.selected_node = None
        self.selected_edge = None
        self.start_node = None
        self.target_node = None
        # Example layouts for each algorithm (mirroring directed/undirected visualizer, but with weights)
        if self.active_algo == "Dijkstra":
            a = self.add_node((200, 200))
            b = self.add_node((400, 200))
            c = self.add_node((600, 200))
            d = self.add_node((300, 400))
            e = self.add_node((500, 400))
            f = self.add_node((700, 400))
            self.add_edge(a.label, b.label, 4)
            self.add_edge(b.label, c.label, 3)
            self.add_edge(a.label, d.label, 2)
            self.add_edge(b.label, d.label, 1)
            self.add_edge(b.label, e.label, 2)
            self.add_edge(c.label, f.label, 5)
            self.add_edge(e.label, f.label, 1)
            self.start_node = a
            self.message = "Example loaded. Click 'Run' to see Dijkstra's algorithm."
        elif self.active_algo == "Bellman-Ford":
            a = self.add_node((200, 200))
            b = self.add_node((400, 200))
            c = self.add_node((600, 200))
            d = self.add_node((300, 400))
            e = self.add_node((500, 400))
            f = self.add_node((700, 400))
            self._add_edge_by_label('A', 'B', 6)
            self._add_edge_by_label('A', 'D', 7)
            self._add_edge_by_label('B', 'C', 5)
            self._add_edge_by_label('B', 'E', -4)
            self._add_edge_by_label('B', 'D', 8)
            self._add_edge_by_label('C', 'B', -2)
            self._add_edge_by_label('D', 'E', 9)
            self._add_edge_by_label('D', 'C', -3)
            self._add_edge_by_label('E', 'A', 2)
            self._add_edge_by_label('E', 'C', 7)
            self.start_node = a
            self.message = "Example loaded. Click 'Run' to see Bellman-Ford."
        elif self.active_algo == "Floyd-Warshall":
            a = self.add_node((200, 200))
            b = self.add_node((400, 200))
            c = self.add_node((600, 200))
            d = self.add_node((300, 400))
            e = self.add_node((500, 400))
            self._add_edge_by_label('A', 'B', 3)
            self._add_edge_by_label('A', 'D', 8)
            self._add_edge_by_label('B', 'C', 1)
            self._add_edge_by_label('B', 'E', 4)
            self._add_edge_by_label('C', 'D', -4)
            self._add_edge_by_label('D', 'E', 2)
            self._add_edge_by_label('E', 'C', -1)
            self.message = "Example loaded. Click 'Run' to see Floyd-Warshall."
        elif self.active_algo == "Prim":
            a = self.add_node((200, 200))
            b = self.add_node((400, 200))
            c = self.add_node((600, 200))
            d = self.add_node((300, 400))
            e = self.add_node((500, 400))
            f = self.add_node((700, 400))
            self._add_edge_by_label('A', 'B', 2)
            self._add_edge_by_label('A', 'D', 3)
            self._add_edge_by_label('B', 'C', 1)
            self._add_edge_by_label('B', 'D', 2)
            self._add_edge_by_label('B', 'E', 3)
            self._add_edge_by_label('C', 'F', 5)
            self._add_edge_by_label('D', 'E', 4)
            self._add_edge_by_label('E', 'F', 1)
            self.message = "Example loaded. Click 'Run' to see Prim's MST."
        elif self.active_algo == "Kruskal":
            a = self.add_node((200, 200))
            b = self.add_node((400, 200))
            c = self.add_node((600, 200))
            d = self.add_node((300, 400))
            e = self.add_node((500, 400))
            f = self.add_node((700, 400))
            self._add_edge_by_label('A', 'B', 1)
            self._add_edge_by_label('A', 'D', 3)
            self._add_edge_by_label('B', 'C', 3)
            self._add_edge_by_label('B', 'D', 1)
            self._add_edge_by_label('B', 'E', 4)
            self._add_edge_by_label('C', 'F', 2)
            self._add_edge_by_label('D', 'E', 2)
            self._add_edge_by_label('E', 'F', 2)
            self.message = "Example loaded. Click 'Run' to see Kruskal's MST."
        elif self.active_algo == "Johnson":
            a = self.add_node((200, 200))
            b = self.add_node((400, 200))
            c = self.add_node((600, 200))
            d = self.add_node((300, 400))
            e = self.add_node((500, 400))
            f = self.add_node((700, 400))
            self._add_edge_by_label('A', 'B', 1)
            self._add_edge_by_label('B', 'C', 2)
            self._add_edge_by_label('C', 'D', 3)
            self._add_edge_by_label('D', 'E', 4)
            self._add_edge_by_label('E', 'A', -5)
            self._add_edge_by_label('B', 'D', 2)
            self._add_edge_by_label('C', 'E', 1)
            self._add_edge_by_label('E', 'F', 2)
            self.message = "Example loaded. Click 'Run' to see Johnson's algorithm."
        elif self.active_algo == "SPFA":
            a = self.add_node((200, 200))
            b = self.add_node((400, 200))
            c = self.add_node((600, 200))
            d = self.add_node((300, 400))
            e = self.add_node((500, 400))
            f = self.add_node((700, 400))
            self._add_edge_by_label('A', 'B', 2)
            self._add_edge_by_label('A', 'D', 4)
            self._add_edge_by_label('B', 'C', 3)
            self._add_edge_by_label('B', 'E', -2)
            self._add_edge_by_label('C', 'F', 2)
            self._add_edge_by_label('D', 'E', 1)
            self._add_edge_by_label('E', 'F', 2)
            self.start_node = a
            self.message = "Example loaded. Click 'Run' to see SPFA."
        elif self.active_algo == "TopoSort+Relax":
            a = self.add_node((200, 200))
            b = self.add_node((400, 200))
            c = self.add_node((600, 200))
            d = self.add_node((300, 400))
            e = self.add_node((500, 400))
            f = self.add_node((700, 400))
            self._add_edge_by_label('A', 'B', 5)
            self._add_edge_by_label('A', 'C', 2)
            self._add_edge_by_label('A', 'D', 3)
            self._add_edge_by_label('B', 'E', 2)
            self._add_edge_by_label('C', 'F', 4)
            self._add_edge_by_label('D', 'B', 1)
            self._add_edge_by_label('D', 'E', 8)
            self._add_edge_by_label('E', 'C', 7)
            self._add_edge_by_label('E', 'F', 4)
            self.start_node = a
            self.message = "Example loaded. Click 'Run' to see TopoSort+Relax."
        elif self.active_algo == "A*":
            a = self.add_node((200, 200))
            b = self.add_node((400, 200))
            c = self.add_node((600, 200))
            d = self.add_node((300, 400))
            e = self.add_node((500, 400))
            f = self.add_node((700, 400))
            self.add_edge(a.label, b.label, 4)
            self.add_edge(b.label, c.label, 3)
            self.add_edge(a.label, d.label, 2)
            self.add_edge(b.label, d.label, 1)
            self.add_edge(b.label, e.label, 2)
            self.add_edge(c.label, f.label, 5)
            self.add_edge(e.label, f.label, 1)
            self.start_node = None # User must set start manually
            self.target_node = None # User must set target manually
            self.message = "A* example loaded. Set start and target nodes, then click 'Run'."
        else:
            self.message = "Example loaded."
        self.setup_buttons()  # Ensure buttons are updated after loading example
        self.draw() # Force a redraw so the user sees the example immediately

    def run_selected_algorithm(self):
        if not self.active_algo:
            self.error_msg = "Select an algorithm first."
            return
        self.result_msg = ''
        self.error_msg = ''
        self.animation_steps = []
        self.animation_index = 0
        self.animating = False
        for node in self.nodes:
            node.selected = False
        for edge in self.edges:
            edge.selected = False
        # Debug: Print adjacency list before running A*
        if self.active_algo == "A*":
            print(f"Start node: {self.start_node.label if self.start_node else 'None'}")
            print(f"Target node: {self.target_node.label if self.target_node else 'None'}")
            print("Adjacency list before running A*:")
            for k, v in self.graph.adj.items():
                print(f"  {k}: {v}")
        # Error handling for unsupported modes
        if self.active_algo == "A*" and not self.directed:
            self.error_msg = "A* requires a directed graph. Please enable directed mode."
            return
        if self.active_algo in ("Prim", "Kruskal") and self.directed:
            self.error_msg = f"{self.active_algo} only works on undirected graphs."
            return
        if self.active_algo == "Dijkstra":
            # Check for negative weights
            for edge in self.edges:
                if edge.weight < 0:
                    self.error_msg = "Dijkstra does not support negative weights. Use Bellman-Ford or SPFA."
                    return
        if self.active_algo == "Prim":
            for edge in self.edges:
                if edge.weight < 0:
                    self.error_msg = "Prim's algorithm does not support negative weights."
                    return
        if self.active_algo == "A*":
            if not self.start_node:
                self.error_msg = "Select a start node (click a node) before running."
                return
            if not self.target_node:
                self.error_msg = "Select a target node (click a node) before running."
                return
            node_pos = {n.label: n.pos for n in self.nodes}
            self.animating = True
            self.animation_steps = list(astar(self.graph, self.start_node.label, self.target_node.label, node_pos, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "Dijkstra":
            if not self.start_node:
                self.error_msg = "Select a start node (click a node) before running."
                return
            self.animating = True
            self.animation_steps = list(dijkstra(self.graph, self.start_node.label, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "Bellman-Ford":
            if not self.start_node:
                self.error_msg = "Select a start node (click a node) before running."
                return
            self.animating = True
            self.animation_steps = list(bellman_ford(self.graph, self.start_node.label, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "Floyd-Warshall":
            self.animating = True
            self.animation_steps = list(floyd_warshall(self.graph, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "Prim":
            self.animating = True
            self.animation_steps = list(prim(self.graph, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "Kruskal":
            self.animating = True
            self.animation_steps = list(kruskal(self.graph, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "Johnson":
            self.animating = True
            self.animation_steps = list(johnson(self.graph, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "SPFA":
            if not self.start_node:
                self.error_msg = "Select a start node (click a node) before running."
                return
            self.animating = True
            self.animation_steps = list(spfa(self.graph, self.start_node.label, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "TopoSort+Relax":
            if not self.start_node:
                self.error_msg = "Select a start node (click a node) before running."
                return
            self.animating = True
            self.animation_steps = list(topo_sort_relax(self.graph, self.start_node.label, visualize=True))
            self.animation_index = 0
        else:
            self.error_msg = f"{self.active_algo} not implemented yet."

    def animate(self):
        msg = ''  # Always define msg at the top
        try:
            if self.animating and self.animation_index < len(self.animation_steps):
                step = self.animation_steps[self.animation_index]
                for node in self.nodes:
                    node.selected = False
                for edge in self.edges:
                    edge.selected = False
                    if self.active_algo == "Dijkstra":
                        if step[0] == "visit":
                            label = step[1]
                            node = next((n for n in self.nodes if n.label == label), None)
                            if node:
                                node.selected = True
                            msg = f"Visiting: {label}"
                        elif step[0] == "found":
                            path = step[1]
                            for label in path:
                                node = next((n for n in self.nodes if n.label == label), None)
                                if node:
                                    node.selected = True
                            msg = f"Path found: {' → '.join(path)}"
                        elif step[0] == "not_found":
                            msg = "No path found."
                        elif step[0] == "update":
                            label = step[1]
                            new_dist = step[2]
                            msg = f"Update: {label}, New Distance: {new_dist}"
                        elif step[0] == "done":
                            dist = step[1]
                            prev = step[2]
                            # Find shortest path to all nodes from start
                            paths = []
                            for node in self.nodes:
                                if node.label == self.start_node.label:
                                    continue
                                path = []
                                cur = node.label
                                while cur is not None:
                                    path.append(cur)
                                    cur = prev.get(cur, None)
                                path.reverse()
                                if len(path) > 1 and dist[path[-1]] < float('inf'):
                                    paths.append(f"{self.start_node.label}→{path[-1]}: {'->'.join(path)} (d={dist[path[-1]]})")
                            msg = "Dijkstra complete. " + (" | ".join(paths) if paths else "No reachable nodes.")
                    elif self.active_algo == "Bellman-Ford":
                        if step[0] == "update":
                            label = step[1]
                            new_dist = step[2]
                            msg = f"Update: {label}, New Distance: {new_dist}"
                        elif step[0] == "negative_cycle":
                            msg = "Negative weight cycle detected!"
                        elif step[0] == "done":
                            dist = step[1]
                            prev = step[2]
                            paths = []
                            for node in self.nodes:
                                if node.label == self.start_node.label:
                                    continue
                                path = []
                                cur = node.label
                                while cur is not None:
                                    path.append(cur)
                                    cur = prev.get(cur, None)
                                path.reverse()
                                if len(path) > 1 and dist[path[-1]] < float('inf'):
                                    paths.append(f"{self.start_node.label}→{path[-1]}: {'->'.join(path)} (d={dist[path[-1]]})")
                            msg = "Bellman-Ford complete. " + (" | ".join(paths) if paths else "No reachable nodes.")
                    elif self.active_algo == "SPFA":
                        if step[0] == "visit":
                            label = step[1]
                            dist = step[2]
                            for node in self.nodes:
                                if node.label == label:
                                    node.selected = True
                            msg = f"SPFA visiting: {label}, Distance: {dist}"
                        elif step[0] == "update":
                            label = step[1]
                            new_dist = step[2]
                            msg = f"SPFA update: {label}, New Distance: {new_dist}"
                        elif step[0] == "negative_cycle":
                            msg = "Negative weight cycle detected!"
                        elif step[0] == "done":
                            dist = step[1]
                            prev = step[2]
                            paths = []
                            for node in self.nodes:
                                if node.label == self.start_node.label:
                                    continue
                                path = []
                                cur = node.label
                                while cur is not None:
                                    path.append(cur)
                                    cur = prev.get(cur, None)
                                path.reverse()
                                if len(path) > 1 and dist[path[-1]] < float('inf'):
                                    paths.append(f"{self.start_node.label}→{path[-1]}: {'->'.join(path)} (d={dist[path[-1]]})")
                            msg = "SPFA complete. " + (" | ".join(paths) if paths else "No reachable nodes.")
                    elif self.active_algo == "A*":
                        if step[0] == "visit":
                            label = step[1]
                            dist = step[2]
                            for node in self.nodes:
                                if node.label == label:
                                    node.selected = True
                            msg = f"A* visiting: {label}, Distance: {dist}"
                        elif step[0] == "update":
                            label = step[1]
                            new_dist = step[2]
                            msg = f"A* update: {label}, New Distance: {new_dist}"
                        elif step[0] == "done":
                            dist = step[1]
                            prev = step[2]
                            path = step[3]
                            if len(path) > 1 and dist[path[-1]] < float('inf'):
                                msg = f"A* path: {' → '.join(path)} (cost={dist[path[-1]]})"
                            else:
                                msg = "A*: No path found."
                    elif self.active_algo == "Prim":
                        if step[0] == "add_edge":
                            u, v, w = step[1], step[2], step[3]
                            for edge in self.edges:
                                if (edge.u.label, edge.v.label) == (u, v) or (edge.u.label, edge.v.label) == (v, u):
                                    edge.selected = True
                            msg = f"MST add edge: {u}-{v} (w={w})"
                        elif step[0] == "done":
                            mst = [s for s in self.animation_steps if s[0] == "add_edge"]
                            edges = [f"{u}-{v}(w={w})" for _, u, v, w in mst]
                            msg = "Prim's MST: " + (", ".join(edges) if edges else "No MST found.")
                    elif self.active_algo == "Kruskal":
                        if step[0] == "add_edge":
                            u, v, w = step[1], step[2], step[3]
                            for edge in self.edges:
                                if (edge.u.label, edge.v.label) == (u, v) or (edge.u.label, edge.v.label) == (v, u):
                                    edge.selected = True
                            msg = f"MST add edge: {u}-{v} (w={w})"
                        elif step[0] == "done":
                            mst = [s for s in self.animation_steps if s[0] == "add_edge"]
                            edges = [f"{u}-{v}(w={w})" for _, u, v, w in mst]
                            msg = "Kruskal's MST: " + (", ".join(edges) if edges else "No MST found.")
                    elif self.active_algo == "Floyd-Warshall":
                        if step[0] == "update":
                            i, j, new_dist = step[1], step[2], step[3]
                            msg = f"Update: {i} → {j}, New Distance: {new_dist}"
                        elif step[0] == "done":
                            dist = step[1]
                            vertices = step[3]
                            matrix = []
                            for i, u in enumerate(vertices):
                                row = []
                                for j, v in enumerate(vertices):
                                    d = dist[i][j]
                                    row.append(f"{d if d < float('inf') else '∞'}")
                                matrix.append(f"{u}: " + ", ".join(row))
                            msg = "Floyd-Warshall complete.\n" + "\n".join(matrix)
                    elif self.active_algo == "Johnson":
                        if step[0] == "update":
                            if len(step) >= 4:
                                u, v, d = step[1], step[2], step[3]
                                msg = f"Johnson update: {u} → {v}, Distance: {d}"
                            elif len(step) == 2 and isinstance(step[1], str):
                                msg = f"Johnson error: {step[1]}"
                            else:
                                msg = "Johnson: Unexpected step format."
                        elif step[0] == "negative_cycle":
                            msg = "Negative weight cycle detected!"
                        elif step[0] == "done":
                            dist = step[1]
                            matrix = {}
                            if not isinstance(dist, dict) or not dist:
                                msg = "Johnson's algorithm complete. (Result unavailable)"
                            else:
                                # Use sorted list of vertices for consistent matrix
                                vertices = sorted(dist.keys())
                                lines = []
                                for u in vertices:
                                    row = []
                                    for v in vertices:
                                        d = dist[u][v]
                                        row.append(f"{d if d < float('inf') else '∞'}")
                                    lines.append(f"{u}: " + ", ".join(row))
                                msg = "Johnson's algorithm complete.\n" + "\n".join(lines)
                    elif self.active_algo == "TopoSort+Relax":
                        if step[0] == "visit":
                            label = step[1]
                            dist = step[2]
                            for node in self.nodes:
                                if node.label == label:
                                    node.selected = True
                            msg = f"TopoSort+Relax visiting: {label}, Distance: {dist}"
                        elif step[0] == "update":
                            label = step[1]
                            new_dist = step[2]
                            msg = f"TopoSort+Relax update: {label}, New Distance: {new_dist}"
                        elif step[0] == "done":
                            dist = step[1]
                            prev = step[2]
                            paths = []
                            for node in self.nodes:
                                if node.label == self.start_node.label:
                                    continue
                                path = []
                                cur = node.label
                                while cur is not None:
                                    path.append(cur)
                                    cur = prev.get(cur, None)
                                path.reverse()
                                if len(path) > 1 and dist[path[-1]] < float('inf'):
                                    paths.append(f"{self.start_node.label}→{path[-1]}: {'->'.join(path)} (d={dist[path[-1]]})")
                            msg = "TopoSort+Relax complete. " + (" | ".join(paths) if paths else "No reachable nodes.")
                self.last_msg = msg # Store the last message
                self.result_msg = msg
                self.draw()
                pygame.time.delay(self.animation_delay)
                self.animation_index += 1
            else:
                self.animating = False
                # Use the last message from the animation loop, or a default
                msg = getattr(self, 'last_msg', '')
                if self.active_algo == "Dijkstra" and self.animation_steps:
                    self.result_msg = msg if msg else "Dijkstra complete."
                elif self.active_algo == "Bellman-Ford" and self.animation_steps:
                    self.result_msg = msg if msg else "Bellman-Ford complete."
                elif self.active_algo == "SPFA" and self.animation_steps:
                    self.result_msg = msg if msg else "SPFA complete."
                elif self.active_algo == "A*" and self.animation_steps:
                    self.result_msg = msg if msg else "A* complete."
                elif self.active_algo == "Prim" and self.animation_steps:
                    self.result_msg = msg if msg else "Prim's MST complete."
                elif self.active_algo == "Kruskal" and self.animation_steps:
                    self.result_msg = msg if msg else "Kruskal's MST complete."
                elif self.active_algo == "Floyd-Warshall" and self.animation_steps:
                    self.result_msg = msg if msg else "Floyd-Warshall complete."
                elif self.active_algo == "Johnson" and self.animation_steps:
                    self.result_msg = msg if msg else "Johnson's algorithm complete."
                elif self.active_algo == "TopoSort+Relax" and self.animation_steps:
                    self.result_msg = msg if msg else "TopoSort+Relax complete."
                for node in self.nodes:
                    node.selected = False
                for edge in self.edges:
                    edge.selected = False
        except Exception as e:
            self.error_msg = f"An error occurred during animation: {e}. You can try again or reset the graph."
            self.animating = False
            self.draw()

    def run(self):
        clock = pygame.time.Clock()
        try:
            while True:
                self.draw()
                if self.animating:
                    self.animate()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    elif event.type == pygame.VIDEORESIZE:
                        self.win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                        self.setup_buttons()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.show_help:
                            self.show_help = False
                            continue
                        if event.button == 1:  # Left click
                            # Click-to-edit weight
                            for rect, edge in getattr(self, 'weight_label_rects', []):
                                if rect.collidepoint(event.pos):
                                    new_weight = self.prompt_weight(str(edge.weight))
                                    edge.weight = new_weight
                                    # Remove old edge from graph data structure
                                    u_label, v_label = edge.u.label, edge.v.label
                                    # Remove all (v, *) from adj[u] and (u, *) from adj[v] if undirected
                                    self.graph.adj[u_label] = [pair for pair in self.graph.adj.get(u_label, []) if pair[0] != v_label]
                                    if not self.directed:
                                        self.graph.adj[v_label] = [pair for pair in self.graph.adj.get(v_label, []) if pair[0] != u_label]
                                    # Add new edge with updated weight
                                    self.graph.add_edge(u_label, v_label, new_weight)
                                    if not self.directed:
                                        self.graph.add_edge(v_label, u_label, new_weight)
                                    break
                            else:
                                for btn in self.mode_buttons + self.buttons + self.example_buttons + [self.run_button]:
                                    if btn.is_hover(event.pos):
                                        btn.active = True
                                        btn.action()
                                        break
                                else:
                                    node = self.get_node_at_pos(event.pos)
                                    if self.current_mode == MODE_SET_START and node:
                                        self.start_node = node
                                        self.error_msg = f"Start node: {node.label}. Click 'Run' to start {self.active_algo}."
                                    elif self.current_mode == MODE_SET_TARGET and node and self.active_algo == "A*":
                                        self.target_node = node
                                        self.error_msg = f"Target node: {node.label}. Click 'Run' to start {self.active_algo}."
                                    elif self.current_mode == MODE_EDIT:
                                        if node:
                                            self.selected_node = node
                                            node.selected = True
                                            self.dragging = True
                                            self.drag_start = node
                                        else:
                                            self.add_node(event.pos)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1 and self.dragging and self.drag_start:
                            node = self.get_node_at_pos(event.pos)
                            if node and node != self.drag_start:
                                weight = self.prompt_weight()
                                self.add_edge(self.drag_start.label, node.label, weight)
                            self.dragging = False
                            self.drag_start = None
                            if self.selected_node:
                                self.selected_node.selected = False
                                self.selected_node = None
                        for btn in self.buttons + self.example_buttons + [self.run_button] + self.mode_buttons:
                            btn.active = False
                    elif event.type == pygame.KEYDOWN:
                        self.error_msg = ''
                        if event.key == pygame.K_q:
                            pygame.quit(); sys.exit()
                        elif event.key == pygame.K_r:
                            self.reset()
                        elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                            self.delete_selected()
                        elif event.key == pygame.K_e:
                            self.set_mode(MODE_EDIT)
                        elif event.key == pygame.K_s:
                            self.set_mode(MODE_SET_START)
                        elif event.key == pygame.K_t: # Changed from K_PLUS/K_EQUALS to K_T for Set Target
                            self.set_mode(MODE_SET_TARGET)
                        elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                            self.animation_delay = max(50, self.animation_delay - 50)
                        elif event.key == pygame.K_MINUS:
                            self.animation_delay = min(2000, self.animation_delay + 50)
                        elif event.key == pygame.K_h:
                            self.show_help = not self.show_help
                        elif event.key == pygame.K_RETURN and not self.animating:
                            self.run_selected_algorithm()
            clock.tick(60)
        except KeyboardInterrupt:
            print("\nExiting gracefully...")
            pygame.quit()
            sys.exit(0)
        except Exception as e:
            print(f"An error occurred: {e}")
            pygame.quit()
            sys.exit(1)

def run_weighted_graph_visualizer():
    WeightedGraphVisualizer().run()

if __name__ == "__main__":
    run_weighted_graph_visualizer() 