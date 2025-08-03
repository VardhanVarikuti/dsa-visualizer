import pygame
import sys
import string
import math
from core.graph.graph import Graph
from core.graph.algorithms.bfs import bfs
from core.graph.algorithms.dfs import dfs
from core.graph.algorithms.cycle_detection import has_cycle
from core.graph.algorithms.topo_sort import topo_sort
from core.graph.algorithms.scc import strongly_connected_components
from core.graph.algorithms.transitive_closure import transitive_closure
from .constants import *

ALGO_LIST = [
    ("BFS", "Breadth-First Search"),
    ("DFS", "Depth-First Search"),
    ("Cycle Detection", "Detect cycles (DFS stack)"),
    ("Topological Sort", "Order of execution (Kahn/DFS)"),
    ("SCC", "Strongly Connected Components"),
    ("Transitive Closure", "Reachability (Floyd/BFS)"),
    ("Shortest Path (BFS)", "Shortest path (unweighted)")
]

MODE_EDIT = 'Edit Graph'
MODE_SET_START = 'Set Start Node'

class VisualNode:
    """A visual node in the graph, with label and position."""
    def __init__(self, label, pos):
        self.label = label
        self.pos = pos
        self.selected = False
        self.color_id = None
        self.temp_color = None
        self.is_scc = False
        self.is_conflict = False

class VisualEdge:
    """A visual edge between two VisualNode objects (directed)."""
    def __init__(self, u, v):
        self.u = u
        self.v = v
        self.selected = False

class Button:
    """A clickable UI button."""
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

class DirectedGraphVisualizer:
    """Main class for the directed graph visualizer UI and logic."""
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Directed Graph Visualizer")
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.nodes = []
        self.edges = []
        self.graph = Graph(directed=True)
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
        self.current_mode = MODE_EDIT
        self.active_algo = None
        self.animating = False
        self.animation_steps = []
        self.animation_index = 0
        self.animation_delay = 600  # ms
        self.show_help = False
        self.setup_buttons()

    def setup_buttons(self):
        w, h = 150, 36
        gap = 30
        total_width = len(ALGO_LIST) * w + (len(ALGO_LIST)-1) * gap
        x = (WIDTH - total_width) // 2
        y = 16
        self.buttons = []
        for i, (algo, desc) in enumerate(ALGO_LIST):
            btn = Button((x + i*(w+gap), y, w, h), algo, lambda a=algo: self.select_algo(a))
            self.buttons.append(btn)
        mb_w, mb_h = 140, 32
        mb_x, mb_y = 30, y + h + 30
        self.mode_buttons = [
            Button((mb_x, mb_y, mb_w, mb_h), "Edit Graph", lambda: self.set_mode(MODE_EDIT)),
        ]
        
        # Add Set Start Node button only for algorithms that require it
        start_node_algorithms = ["BFS", "DFS", "Shortest Path (BFS)"]
        if self.active_algo in start_node_algorithms:
            self.mode_buttons.append(Button((mb_x + mb_w + 16, mb_y, mb_w, mb_h), "Set Start Node", lambda: self.set_mode(MODE_SET_START)))
        
        btn_w, btn_h = 150, 36
        btn_x = WIDTH - btn_w - 30
        btn_y1 = y + h + 30
        btn_y2 = btn_y1 + btn_h + 12
        self.example_buttons = [
            Button((btn_x, btn_y1, btn_w, btn_h), "Load Example", self.load_example_graph)
        ]
        self.run_button = Button((btn_x, btn_y2, btn_w, btn_h), "Run", self.run_selected_algorithm)

    def draw(self):
        win_width, win_height = self.win.get_size()
        self.win.fill(BG_COLOR)
        # Draw edges as arrows
        edge_counts = {}
        for edge in self.edges:
            key = (edge.u.label, edge.v.label)
            edge_counts[key] = edge_counts.get(key, 0) + 1
        edge_drawn = {}
        for edge in self.edges:
            color = EDGE_SELECTED_COLOR if edge.selected else EDGE_COLOR
            u, v = edge.u, edge.v
            key = (u.label, v.label)
            count = edge_counts[key]
            idx = edge_drawn.get(key, 0)
            # Draw arrow from u to v
            self._draw_arrow(u.pos, v.pos, color, offset=0 if count == 1 else 20*((idx+1)-(count+1)/2))
            edge_drawn[key] = idx + 1
        # Draw nodes
        for node in self.nodes:
            if node == self.start_node:
                color = (0, 200, 0)
            elif hasattr(node, 'color_id') and node.color_id is not None:
                color = COMPONENT_COLORS[node.color_id % len(COMPONENT_COLORS)]
            elif hasattr(node, 'temp_color') and node.temp_color is not None:
                color = node.temp_color
            elif node.selected:
                color = NODE_SELECTED_COLOR
            else:
                color = NODE_COLOR
            pygame.draw.circle(self.win, color, node.pos, NODE_RADIUS)
            pygame.draw.circle(self.win, (0,0,0), node.pos, NODE_RADIUS, 2)
            label_surf = self.font.render(node.label, True, TEXT_COLOR)
            rect = label_surf.get_rect(center=node.pos)
            self.win.blit(label_surf, rect)
        # Draw dragging edge
        if self.dragging and self.drag_start:
            self._draw_arrow(self.drag_start.pos, pygame.mouse.get_pos(), (120,120,120))
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
        mode_surf = self.font.render(f"Mode: {self.current_mode}", True, (80, 80, 80))
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
                "S: Set start node (for BFS/DFS)",
                "+/-: Adjust animation speed",
                "H: Toggle this help overlay",
                "",
                "ALGORITHMS:",
                "BFS/DFS: Traversal from start node (select node, then Run)",
                "Cycle Detection: Finds cycles (DFS stack)",
                "Topological Sort: Kahn/DFS order",
                "SCC: Kosaraju's algorithm",
                "Transitive Closure: Floyd/BFS reachability",
                "Shortest Path (BFS): Unweighted shortest path",
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

    def _draw_arrow(self, start, end, color, offset=0):
        # Draw a line with an arrowhead from start to end, with optional perpendicular offset
        x1, y1 = start
        x2, y2 = end
        if offset != 0:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = y2 - y1, x1 - x2
            norm = math.hypot(dx, dy)
            if norm == 0:
                norm = 1
            ox, oy = mx + dx / norm * offset, my + dy / norm * offset
            ctrl = (ox, oy)
            points = [start, ctrl, end]
            pygame.draw.aalines(self.win, color, False, points, 2)
            # Arrowhead at end
            self._draw_arrowhead(ctrl, end, color)
        else:
            # Shorten line so arrowhead doesn't overlap node
            dx, dy = x2 - x1, y2 - y1
            dist = math.hypot(dx, dy)
            if dist == 0:
                return
            ux, uy = dx / dist, dy / dist
            sx, sy = x1 + ux * NODE_RADIUS, y1 + uy * NODE_RADIUS
            ex, ey = x2 - ux * NODE_RADIUS, y2 - uy * NODE_RADIUS
            pygame.draw.line(self.win, color, (sx, sy), (ex, ey), 3)
            self._draw_arrowhead((sx, sy), (ex, ey), color)

    def _draw_arrowhead(self, start, end, color):
        # Draw an arrowhead at the end of the line from start to end
        x1, y1 = start
        x2, y2 = end
        angle = math.atan2(y2 - y1, x2 - x1)
        length = 16
        width = 8
        left = (x2 - length * math.cos(angle - math.pi/8), y2 - length * math.sin(angle - math.pi/8))
        right = (x2 - length * math.cos(angle + math.pi/8), y2 - length * math.sin(angle + math.pi/8))
        pygame.draw.polygon(self.win, color, [end, left, right])

    def show_message(self, msg, color, y_abs=None):
        if y_abs is None:
            y_abs = HEIGHT - 60
        font = pygame.font.SysFont(None, 24)
        surf = font.render(msg, True, color)
        rect = surf.get_rect(center=(WIDTH // 2, y_abs))
        self.win.blit(surf, rect)

    def select_node(self, label):
        if self.current_mode == MODE_EDIT:
            node = next((n for n in self.nodes if n.label == label), None)
            if node:
                self.selected_node = node
                self.message = f"Node '{label}' selected. Click to add edge."
            else:
                self.selected_node = VisualNode(label, pygame.mouse.get_pos())
                # Add to graph and UI
                if label not in self.graph.get_vertices():
                    self.graph.adj[label] = []
                self.nodes.append(self.selected_node)
                self.message = f"Node '{label}' added. Click to add edge."
        elif self.current_mode == MODE_SET_START:
            node = next((n for n in self.nodes if n.label == label), None)
            if node:
                self.start_node = node
                self.message = f"Start node set to '{label}'."
            else:
                self.error_msg = f"Node '{label}' not found."

    def add_edge(self, u, v):
        if self.current_mode == MODE_EDIT:
            if u and v:
                self.edges.append(VisualEdge(u, v))
                self.graph.add_edge(u.label, v.label)
                self.message = f"Edge from '{u.label}' to '{v.label}' added."
            else:
                self.error_msg = "Cannot add edge: no node selected or target position is occupied."
        elif self.current_mode == MODE_SET_START:
            if self.start_node and v:
                self.start_node = v
                self.graph.add_node(self.start_node.label)
                self.nodes.append(self.start_node)
                self.message = f"Start node set to '{self.start_node.label}'."
            else:
                self.error_msg = "Cannot set start node: no node selected or target position is occupied."

    def delete_selected(self):
        if self.selected_node:
            self.graph.remove_node(self.selected_node.label)
            self.nodes = [n for n in self.nodes if n != self.selected_node]
            self.selected_node = None
            self.message = "Node deleted."
        elif self.selected_edge:
            self.graph.remove_edge(self.selected_edge.u.label, self.selected_edge.v.label)
            self.edges = [e for e in self.edges if e != self.selected_edge]
            self.selected_edge = None
            self.message = "Edge deleted."
        else:
            self.error_msg = "No node or edge selected for deletion."

    def reset_graph(self):
        self.graph = Graph(directed=True)
        self.nodes = []
        self.edges = []
        self.selected_node = None
        self.start_node = None
        self.message = "Graph reset."

    def select_algo(self, algo_name):
        self.active_algo = algo_name
        self.message = f"Algorithm '{algo_name}' selected. Click 'Run' to execute."
        # Rebuild buttons to show/hide Set Start Node button based on selected algorithm
        self.setup_buttons()

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
            node.color_id = None
            node.temp_color = None
            node.is_scc = False
            node.is_conflict = False
        for edge in self.edges:
            edge.selected = False
        if self.active_algo in ("BFS", "DFS"):
            if not self.start_node:
                self.error_msg = "Select a start node (click a node) before running."
                return
            self.animating = True
            self.animation_steps = list(bfs(self.graph, self.start_node.label)) if self.active_algo == "BFS" else list(dfs(self.graph, self.start_node.label))
            self.animation_index = 0
        elif self.active_algo == "Cycle Detection":
            self.animating = True
            self.animation_steps = list(has_cycle(self.graph, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "Topological Sort":
            self.animating = True
            self.animation_steps = list(topo_sort(self.graph, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "SCC":
            self.animating = True
            self.animation_steps = list(strongly_connected_components(self.graph, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "Transitive Closure":
            self.animating = True
            self.animation_steps = list(transitive_closure(self.graph, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "Shortest Path (BFS)":
            if not self.start_node:
                self.error_msg = "Select a start node (click a node) before running."
                return
            # BFS for shortest path: yield path at end
            from collections import deque
            visited = set()
            parent = {}
            queue = deque([self.start_node.label])
            steps = []
            while queue:
                u = queue.popleft()
                if u not in visited:
                    steps.append(("visit", u))
                    visited.add(u)
                    for v, _ in self.graph.get_neighbors(u):
                        if v not in visited and v not in queue:
                            parent[v] = u
                            queue.append(v)
            # Find farthest node for demo
            if visited:
                end = list(visited)[-1]
                path = []
                cur = end
                while cur != self.start_node.label:
                    path.append(cur)
                    cur = parent.get(cur, self.start_node.label)
                    if cur == self.start_node.label:
                        break
                path.append(self.start_node.label)
                path.reverse()
                steps.append(("path", path))
            self.animating = True
            self.animation_steps = steps
            self.animation_index = 0
        else:
            self.error_msg = f"{self.active_algo} not implemented yet."

    def animate(self):
        if self.animating and self.animation_index < len(self.animation_steps):
            step = self.animation_steps[self.animation_index]
            for node in self.nodes:
                node.selected = False
                node.temp_color = None
                node.is_scc = False
                node.is_conflict = False
            for edge in self.edges:
                edge.selected = False
            msg = ''
            if self.active_algo in ("BFS", "DFS"):
                for node in self.nodes:
                    node.selected = (node.label == step)
                msg = f"{self.active_algo} visiting: {step}"
            elif self.active_algo == "Cycle Detection":
                if step[0] == "visit":
                    label = step[1]
                    path = step[2]
                    rec_stack = step[3]
                    for node in self.nodes:
                        if node.label in path:
                            node.selected = True
                    msg = f"DFS path: {' -> '.join(path)} | RecStack: {', '.join(rec_stack)}"
                elif step[0] == "cycle":
                    cycle_path = step[1]
                    for node in self.nodes:
                        if node.label in cycle_path:
                            node.selected = True
                    msg = f"Cycle found: {' -> '.join(cycle_path)}"
                elif step[0] == "done":
                    has_cycle = step[1]
                    cycle_path = step[2]
                    msg = "Cycle Detected!" if has_cycle else "No Cycles."
            elif self.active_algo == "Topological Sort":
                if step[0] == "init_queue":
                    msg = f"Initial queue: {', '.join(step[1])}"
                elif step[0] == "visit":
                    label = step[1]
                    order = step[2]
                    queue = step[3]
                    for node in self.nodes:
                        if node.label == label:
                            node.selected = True
                    msg = f"TopoSort visiting: {label} | Order: {' -> '.join(order)} | Queue: {', '.join(queue)}"
                elif step[0] == "enqueue":
                    label = step[1]
                    queue = step[2]
                    msg = f"Enqueue: {label} | Queue: {', '.join(queue)}"
                elif step[0] == "cycle":
                    msg = "Cycle detected! No topological order."
                elif step[0] == "done":
                    order = step[1]
                    msg = f"Topological Order: {' -> '.join(order)}"
            elif self.active_algo == "SCC":
                if step[0] == "visit":
                    label = step[1]
                    phase = step[2]
                    for node in self.nodes:
                        if node.label == label:
                            node.selected = True
                    msg = f"SCC {phase} DFS visiting: {label}"
                elif step[0] == "finish":
                    label = step[1]
                    order = step[2]
                    msg = f"Finish: {label} | Order: {', '.join(order)}"
                elif step[0] == "transpose":
                    msg = "Transposing graph..."
                elif step[0] == "component":
                    comp = step[1]
                    sccs = step[2]
                    for node in self.nodes:
                        if node.label in comp:
                            node.temp_color = COMPONENT_COLORS[len(sccs) % len(COMPONENT_COLORS)]
                    msg = f"SCC found: {{{', '.join(comp)}}}"
                elif step[0] == "done":
                    sccs = step[1]
                    msg = f"Total SCCs: {len(sccs)}"
            elif self.active_algo == "Transitive Closure":
                if step[0] == "init":
                    closure = step[1]
                    vertices = step[2]
                    msg = f"Initial closure matrix."
                elif step[0] == "update":
                    i, j, k, closure = step[1], step[2], step[3], step[4]
                    msg = f"Closure[{i},{j}] updated via {k}."
                elif step[0] == "done":
                    closure = step[1]
                    vertices = step[2]
                    msg = f"Transitive closure complete."
            elif self.active_algo == "Shortest Path (BFS)":
                if step[0] == "visit":
                    label = step[1]
                    for node in self.nodes:
                        if node.label == label:
                            node.selected = True
                    msg = f"BFS visiting: {label}"
                elif step[0] == "path":
                    path = step[1]
                    for node in self.nodes:
                        if node.label in path:
                            node.selected = True
                    msg = f"Shortest path: {' -> '.join(path)}"
            self.result_msg = msg
            self.draw()
            pygame.time.delay(self.animation_delay)
            self.animation_index += 1
        else:
            self.animating = False
            # Final result message for each algo
            if self.active_algo == "Topological Sort" and self.animation_steps:
                order = self.animation_steps[-1][1] if self.animation_steps[-1][0] == "done" else []
                self.result_msg = f"Topological Order: {' -> '.join(order)}"
            elif self.active_algo == "Cycle Detection" and self.animation_steps:
                has_cycle = self.animation_steps[-1][1] if self.animation_steps[-1][0] == "done" else False
                self.result_msg = "Cycle Detected!" if has_cycle else "No Cycles."
            elif self.active_algo == "SCC" and self.animation_steps:
                sccs = self.animation_steps[-1][1] if self.animation_steps[-1][0] == "done" else []
                self.result_msg = f"Total SCCs: {len(sccs)}"
            elif self.active_algo == "Transitive Closure" and self.animation_steps:
                self.result_msg = "Transitive closure complete."
            elif self.active_algo == "Shortest Path (BFS)" and self.animation_steps:
                path = self.animation_steps[-1][1] if self.animation_steps[-1][0] == "path" else []
                self.result_msg = f"Shortest path: {' -> '.join(path)}"
            elif self.active_algo in ("BFS", "DFS") and self.animation_steps:
                order = [str(x) for x in self.animation_steps]
                self.result_msg = f"{self.active_algo} order: {' -> '.join(order)}"
            for node in self.nodes:
                node.selected = False
                node.is_scc = False
                node.is_conflict = False
            for edge in self.edges:
                edge.selected = False

    def set_mode(self, mode):
        self.current_mode = mode
        if mode == MODE_EDIT:
            self.message = "Click to add node | Drag to add edge | Del: delete | R: Reset | Q: Quit | H: Help"
        elif mode == MODE_SET_START:
            self.message = "Click to add node | Drag to add edge | Del: delete | R: Reset | Q: Quit | H: Help"

    def _add_node_at(self, pos):
        try:
            label = next(self.node_labels)
        except StopIteration:
            return None
        node = VisualNode(label, pos)
        self.nodes.append(node)
        self.graph.adj[label] = []
        return node

    def _add_edge_by_label(self, l1, l2):
        n1 = next((n for n in self.nodes if n.label == l1), None)
        n2 = next((n for n in self.nodes if n.label == l2), None)
        if n1 and n2:
            self.edges.append(VisualEdge(n1, n2))
            self.graph.add_edge(n1.label, n2.label)

    def load_example_graph(self):
        self.reset_graph()
        self.node_labels = iter(string.ascii_uppercase)
        self.nodes.clear()
        self.edges.clear()
        self.graph = Graph(directed=True)
        self.selected_node = None
        self.selected_edge = None
        self.start_node = None
        # Example layouts for each algorithm
        if self.active_algo == "BFS":
            a = self._add_node_at((200, 200)) # A
            b = self._add_node_at((400, 200)) # B
            c = self._add_node_at((600, 200)) # C
            d = self._add_node_at((300, 400)) # D
            e = self._add_node_at((500, 400)) # E
            f = self._add_node_at((700, 400)) # F
            self._add_edge_by_label('A', 'B')
            self._add_edge_by_label('B', 'C')
            self._add_edge_by_label('A', 'D')
            self._add_edge_by_label('B', 'D')
            self._add_edge_by_label('B', 'E')
            self._add_edge_by_label('C', 'F')
            self._add_edge_by_label('E', 'F')
            self.start_node = a
        elif self.active_algo == "DFS":
            a = self._add_node_at((200, 200))
            b = self._add_node_at((400, 200))
            c = self._add_node_at((600, 200))
            d = self._add_node_at((300, 400))
            e = self._add_node_at((500, 400))
            f = self._add_node_at((700, 400))
            self._add_edge_by_label('A', 'B')
            self._add_edge_by_label('B', 'C')
            self._add_edge_by_label('A', 'D')
            self._add_edge_by_label('B', 'D')
            self._add_edge_by_label('B', 'E')
            self._add_edge_by_label('C', 'F')
            self._add_edge_by_label('E', 'F')
            self.start_node = a
        elif self.active_algo == "Cycle Detection":
            a = self._add_node_at((300, 300))
            b = self._add_node_at((500, 300))
            c = self._add_node_at((400, 500))
            self._add_edge_by_label('A', 'B')
            self._add_edge_by_label('B', 'C')
            self._add_edge_by_label('C', 'A')
        elif self.active_algo == "Topological Sort":
            a = self._add_node_at((200, 200))
            b = self._add_node_at((400, 200))
            c = self._add_node_at((600, 200))
            d = self._add_node_at((300, 400))
            e = self._add_node_at((500, 400))
            self._add_edge_by_label('A', 'B')
            self._add_edge_by_label('A', 'C')
            self._add_edge_by_label('B', 'D')
            self._add_edge_by_label('C', 'D')
            self._add_edge_by_label('D', 'E')
        elif self.active_algo == "SCC":
            a = self._add_node_at((200, 200))
            b = self._add_node_at((400, 200))
            c = self._add_node_at((600, 200))
            d = self._add_node_at((300, 400))
            e = self._add_node_at((500, 400))
            self._add_edge_by_label('A', 'B')
            self._add_edge_by_label('B', 'C')
            self._add_edge_by_label('C', 'A')
            self._add_edge_by_label('B', 'D')
            self._add_edge_by_label('D', 'E')
            self._add_edge_by_label('E', 'D')
        elif self.active_algo == "Transitive Closure":
            a = self._add_node_at((200, 200))
            b = self._add_node_at((400, 200))
            c = self._add_node_at((600, 200))
            d = self._add_node_at((300, 400))
            e = self._add_node_at((500, 400))
            self._add_edge_by_label('A', 'B')
            self._add_edge_by_label('B', 'C')
            self._add_edge_by_label('C', 'D')
            self._add_edge_by_label('D', 'E')
            self._add_edge_by_label('E', 'A')
        elif self.active_algo == "Shortest Path (BFS)":
            a = self._add_node_at((200, 200))
            b = self._add_node_at((400, 200))
            c = self._add_node_at((600, 200))
            d = self._add_node_at((300, 400))
            e = self._add_node_at((500, 400))
            self._add_edge_by_label('A', 'B')
            self._add_edge_by_label('B', 'C')
            self._add_edge_by_label('A', 'D')
            self._add_edge_by_label('B', 'D')
            self._add_edge_by_label('B', 'E')
            self._add_edge_by_label('C', 'E')
            self.start_node = a
        self.message = "Example graph loaded."

    def get_node_at_pos(self, pos):
        """Returns the node at the given position, or None if no node is found."""
        for node in self.nodes:
            if (node.pos[0] - pos[0]) ** 2 + (node.pos[1] - pos[1]) ** 2 < (2 * NODE_RADIUS) ** 2:
                return node
        return None

    def get_edge_at_pos(self, pos):
        """Returns the edge at the given position, or None if no edge is found."""
        for edge in self.edges:
            if edge.u.pos == pos or edge.v.pos == pos:
                return edge
        return None

    def run(self):
        clock = pygame.time.Clock()
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
                        # 1. Check all buttons first
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
                            elif self.current_mode == MODE_EDIT:
                                if node:
                                    self.selected_node = node
                                    node.selected = True
                                    self.dragging = True
                                    self.drag_start = node
                                else:
                                    # Add new node at click position
                                    if any((node.pos[0] - event.pos[0]) ** 2 + (node.pos[1] - event.pos[1]) ** 2 < (2 * NODE_RADIUS) ** 2 for node in self.nodes):
                                        self.error_msg = "Too close to another node. Move further away."
                                    else:
                                        try:
                                            label = next(self.node_labels)
                                        except StopIteration:
                                            self.error_msg = "No more node labels available."
                                            continue
                                        new_node = VisualNode(label, event.pos)
                                        self.nodes.append(new_node)
                                        self.graph.adj[label] = []
                    elif event.button == 3:  # Right click
                        edge = self.get_edge_at_pos(event.pos)
                        if edge:
                            self.selected_edge = edge
                            edge.selected = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.dragging and self.drag_start:
                        node = self.get_node_at_pos(event.pos)
                        if node and node != self.drag_start:
                            self.add_edge(self.drag_start, node)
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
                        self.reset_graph()
                    elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        self.delete_selected()
                    elif event.key == pygame.K_e:
                        self.set_mode(MODE_EDIT)
                    elif event.key == pygame.K_s:
                        self.set_mode(MODE_SET_START)
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        self.animation_delay = max(100, self.animation_delay - 100)
                        self.error_msg = f"Animation speed: {self.animation_delay} ms"
                    elif event.key == pygame.K_MINUS:
                        self.animation_delay = min(2000, self.animation_delay + 100)
                        self.error_msg = f"Animation speed: {self.animation_delay} ms"
                    elif event.key == pygame.K_h:
                        self.show_help = not self.show_help
                        continue
            clock.tick(60)

def run_directed_graph_visualizer():
    DirectedGraphVisualizer().run()

if __name__ == "__main__":
    run_directed_graph_visualizer() 